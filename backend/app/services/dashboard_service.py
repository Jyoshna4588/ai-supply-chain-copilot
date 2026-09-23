from typing import Any

from app.config.settings import settings
from app.services.bigquery_ai_service import BigQueryAIService


class DashboardService:
    """
    Provides executive KPI, chart, and recommendation data
    for the supply-chain dashboard.
    """

    def __init__(self):
        self.bigquery_service = BigQueryAIService()

    def get_summary(self) -> dict[str, Any]:
        """
        Return the complete executive dashboard payload.

        All dashboard data is collected using one BigQuery query
        so the frontend only needs one API request.
        """

        project_id = settings.gcp_project_id
        dataset = settings.bigquery_dataset

        query = f"""
            WITH dashboard_kpis AS (
                SELECT
                    (
                        SELECT COUNT(DISTINCT product_id)
                        FROM
                            `{project_id}.{dataset}.inventory`
                        WHERE
                            LOWER(inventory_status) IN (
                                'low stock',
                                'low_stock',
                                'critical',
                                'below reorder point'
                            )
                            OR available_stock < reorder_point
                    ) AS low_stock_products,

                    (
                        SELECT COUNT(DISTINCT supplier_id)
                        FROM
                            `{project_id}.{dataset}.supplier_performance`
                    ) AS total_suppliers,

                    (
                        SELECT COUNT(*)
                        FROM
                            `{project_id}.{dataset}.purchase_orders`
                        WHERE
                            LOWER(status) = 'delayed'
                            OR (
                                expected_delivery_date < CURRENT_DATE()
                                AND actual_delivery_date IS NULL
                            )
                    ) AS delayed_purchase_orders,

                    (
                        SELECT COUNT(*)
                        FROM
                            `{project_id}.{dataset}.purchase_orders`
                        WHERE
                            LOWER(status) IN (
                                'open',
                                'pending',
                                'processing',
                                'in progress',
                                'approved'
                            )
                            OR actual_delivery_date IS NULL
                    ) AS open_purchase_orders,

                    (
                        SELECT ROUND(
                            SUM(COALESCE(order_value, 0)),
                            2
                        )
                        FROM
                            `{project_id}.{dataset}.purchase_orders`
                        WHERE
                            order_date >= DATE_TRUNC(
                                CURRENT_DATE(),
                                MONTH
                            )
                    ) AS current_month_purchase_value,

                    (
                        SELECT COUNT(*)
                        FROM
                            `{project_id}.{dataset}.shipments`
                        WHERE
                            LOWER(status) NOT IN (
                                'delivered',
                                'completed'
                            )
                    ) AS active_shipments
            ),

            supplier_delay_rates AS (
                SELECT
                    supplier_name,
                    ROUND(delay_rate, 2) AS delay_rate
                FROM
                    `{project_id}.{dataset}.supplier_performance`
                WHERE
                    supplier_name IS NOT NULL
                    AND delay_rate IS NOT NULL
                ORDER BY
                    delay_rate DESC
                LIMIT 5
            ),

            inventory_status_distribution AS (
                SELECT
                    CASE
                        WHEN inventory_status IS NULL
                            OR TRIM(inventory_status) = ''
                            THEN 'Unknown'

                        ELSE INITCAP(
                            REPLACE(
                                inventory_status,
                                '_',
                                ' '
                            )
                        )
                    END AS inventory_status,

                    COUNT(*) AS product_count,

                    SUM(
                        COALESCE(
                            available_stock,
                            0
                        )
                    ) AS available_units

                FROM
                    `{project_id}.{dataset}.inventory`

                GROUP BY
                    inventory_status
            ),

            purchase_order_trend AS (
                SELECT
                    DATE_TRUNC(
                        order_date,
                        MONTH
                    ) AS month,

                    COUNT(*) AS total_orders,

                    COUNTIF(
                        LOWER(status) = 'delayed'
                        OR (
                            expected_delivery_date < CURRENT_DATE()
                            AND actual_delivery_date IS NULL
                        )
                    ) AS delayed_orders,

                    ROUND(
                        SUM(
                            COALESCE(
                                order_value,
                                0
                            )
                        ),
                        2
                    ) AS purchase_value

                FROM
                    `{project_id}.{dataset}.purchase_orders`

                WHERE
                    order_date IS NOT NULL
                    AND order_date >= DATE_SUB(
                        DATE_TRUNC(
                            CURRENT_DATE(),
                            MONTH
                        ),
                        INTERVAL 11 MONTH
                    )

                GROUP BY
                    month

                ORDER BY
                    month
            ),

            warehouse_utilization AS (
                SELECT
                    COALESCE(
                        warehouse_name,
                        warehouse_id,
                        'Unknown Warehouse'
                    ) AS warehouse_name,

                    capacity,

                    ROUND(
                        CASE
                            WHEN current_utilization IS NULL
                                THEN 0

                            WHEN current_utilization <= 1
                                THEN current_utilization * 100

                            ELSE current_utilization
                        END,
                        2
                    ) AS utilization_percent

                FROM
                    `{project_id}.{dataset}.warehouses`

                WHERE
                    warehouse_id IS NOT NULL

                ORDER BY
                    utilization_percent DESC

                LIMIT 6
            ),

            shipment_status_distribution AS (
                SELECT
                    CASE
                        WHEN status IS NULL
                            OR TRIM(status) = ''
                            THEN 'Unknown'

                        ELSE INITCAP(
                            REPLACE(
                                status,
                                '_',
                                ' '
                            )
                        )
                    END AS shipment_status,

                    COUNT(*) AS shipment_count

                FROM
                    `{project_id}.{dataset}.shipments`

                GROUP BY
                    shipment_status

                ORDER BY
                    shipment_count DESC
            ),

            forecast_accuracy_distribution AS (
                SELECT
                    CASE
                        WHEN forecast_accuracy_status IS NULL
                            OR TRIM(forecast_accuracy_status) = ''
                            THEN 'Unknown'

                        ELSE INITCAP(
                            REPLACE(
                                forecast_accuracy_status,
                                '_',
                                ' '
                            )
                        )
                    END AS accuracy_status,

                    COUNT(*) AS forecast_count,

                    ROUND(
                        AVG(
                            CASE
                                WHEN mape IS NULL
                                    THEN NULL

                                WHEN mape <= 1
                                    THEN mape * 100

                                ELSE mape
                            END
                        ),
                        2
                    ) AS average_mape

                FROM
                    `{project_id}.{dataset}.demand_forecast`

                GROUP BY
                    accuracy_status

                ORDER BY
                    forecast_count DESC
            ),

            forecast_summary AS (
                SELECT
                    ROUND(
                        AVG(
                            CASE
                                WHEN mape IS NULL
                                    THEN NULL

                                WHEN mape <= 1
                                    THEN mape * 100

                                ELSE mape
                            END
                        ),
                        2
                    ) AS overall_average_mape,

                    SUM(
                        COALESCE(
                            forecast_quantity,
                            0
                        )
                    ) AS total_forecast_quantity,

                    SUM(
                        COALESCE(
                            actual_quantity,
                            0
                        )
                    ) AS total_actual_quantity

                FROM
                    `{project_id}.{dataset}.demand_forecast`
            )

            SELECT
                dashboard_kpis.low_stock_products,
                dashboard_kpis.total_suppliers,
                dashboard_kpis.delayed_purchase_orders,
                dashboard_kpis.open_purchase_orders,
                dashboard_kpis.current_month_purchase_value,
                dashboard_kpis.active_shipments,

                forecast_summary.overall_average_mape,
                forecast_summary.total_forecast_quantity,
                forecast_summary.total_actual_quantity,

                ARRAY(
                    SELECT AS STRUCT
                        supplier_name,
                        delay_rate

                    FROM
                        supplier_delay_rates

                    ORDER BY
                        delay_rate DESC
                ) AS supplier_delay_rates,

                ARRAY(
                    SELECT AS STRUCT
                        inventory_status,
                        product_count,
                        available_units

                    FROM
                        inventory_status_distribution

                    ORDER BY
                        product_count DESC
                ) AS inventory_status_distribution,

                ARRAY(
                    SELECT AS STRUCT
                        FORMAT_DATE(
                            '%b %Y',
                            month
                        ) AS month,

                        total_orders,
                        delayed_orders,
                        purchase_value

                    FROM
                        purchase_order_trend

                    ORDER BY
                        month
                ) AS purchase_order_trend,

                ARRAY(
                    SELECT AS STRUCT
                        warehouse_name,
                        capacity,
                        utilization_percent

                    FROM
                        warehouse_utilization

                    ORDER BY
                        utilization_percent DESC
                ) AS warehouse_utilization,

                ARRAY(
                    SELECT AS STRUCT
                        shipment_status,
                        shipment_count

                    FROM
                        shipment_status_distribution

                    ORDER BY
                        shipment_count DESC
                ) AS shipment_status_distribution,

                ARRAY(
                    SELECT AS STRUCT
                        accuracy_status,
                        forecast_count,
                        average_mape

                    FROM
                        forecast_accuracy_distribution

                    ORDER BY
                        forecast_count DESC
                ) AS forecast_accuracy_distribution

            FROM
                dashboard_kpis

            CROSS JOIN
                forecast_summary
        """

        query_results = self.bigquery_service.execute_query(
            query=query
        )

        if not query_results:
            return self._empty_summary()

        row = query_results[0]

        summary = {
            "low_stock_products": int(
                row.get("low_stock_products") or 0
            ),
            "total_suppliers": int(
                row.get("total_suppliers") or 0
            ),
            "delayed_purchase_orders": int(
                row.get("delayed_purchase_orders") or 0
            ),
            "open_purchase_orders": int(
                row.get("open_purchase_orders") or 0
            ),
            "current_month_purchase_value": float(
                row.get("current_month_purchase_value") or 0
            ),
            "active_shipments": int(
                row.get("active_shipments") or 0
            ),
            "overall_average_mape": float(
                row.get("overall_average_mape") or 0
            ),
            "total_forecast_quantity": int(
                row.get("total_forecast_quantity") or 0
            ),
            "total_actual_quantity": int(
                row.get("total_actual_quantity") or 0
            ),
            "supplier_delay_rates": self._format_rows(
                row.get("supplier_delay_rates"),
                {
                    "supplier_name": str,
                    "delay_rate": float,
                },
            ),
            "inventory_status_distribution": self._format_rows(
                row.get("inventory_status_distribution"),
                {
                    "inventory_status": str,
                    "product_count": int,
                    "available_units": int,
                },
            ),
            "purchase_order_trend": self._format_rows(
                row.get("purchase_order_trend"),
                {
                    "month": str,
                    "total_orders": int,
                    "delayed_orders": int,
                    "purchase_value": float,
                },
            ),
            "warehouse_utilization": self._format_rows(
                row.get("warehouse_utilization"),
                {
                    "warehouse_name": str,
                    "capacity": int,
                    "utilization_percent": float,
                },
            ),
            "shipment_status_distribution": self._format_rows(
                row.get("shipment_status_distribution"),
                {
                    "shipment_status": str,
                    "shipment_count": int,
                },
            ),
            "forecast_accuracy_distribution": self._format_rows(
                row.get("forecast_accuracy_distribution"),
                {
                    "accuracy_status": str,
                    "forecast_count": int,
                    "average_mape": float,
                },
            ),
        }

        summary["recommendations"] = (
            self._build_recommendations(
                summary
            )
        )

        return summary

    def _format_rows(
        self,
        nested_rows: Any,
        field_types: dict[str, type],
    ) -> list[dict[str, Any]]:
        """
        Convert nested BigQuery rows into JSON-safe dictionaries.
        """

        if not nested_rows:
            return []

        formatted_rows = []

        for nested_row in nested_rows:
            formatted_row = {}

            for field_name, field_type in (
                field_types.items()
            ):
                value = self._get_nested_value(
                    nested_row,
                    field_name,
                )

                if value is None:
                    if field_type is str:
                        value = ""
                    elif field_type is float:
                        value = 0.0
                    else:
                        value = 0

                formatted_row[field_name] = (
                    field_type(value)
                )

            formatted_rows.append(
                formatted_row
            )

        return formatted_rows

    def _build_recommendations(
        self,
        summary: dict[str, Any],
    ) -> list[dict[str, str]]:
        """
        Build fast dashboard recommendations using current metrics.

        LangChain and LangGraph can later convert these deterministic
        insights into richer AI-generated recommendations.
        """

        recommendations: list[dict[str, str]] = []

        low_stock_products = (
            summary["low_stock_products"]
        )

        delayed_orders = (
            summary["delayed_purchase_orders"]
        )

        supplier_rows = (
            summary["supplier_delay_rates"]
        )

        warehouse_rows = (
            summary["warehouse_utilization"]
        )

        average_mape = (
            summary["overall_average_mape"]
        )

        if low_stock_products > 0:
            recommendations.append(
                {
                    "severity": "warning",
                    "title": "Replenish low-stock products",
                    "message": (
                        f"{low_stock_products:,} products are below "
                        "their expected inventory threshold. Prioritize "
                        "high-demand and business-critical products."
                    ),
                }
            )

        if delayed_orders > 0:
            recommendations.append(
                {
                    "severity": "danger",
                    "title": "Escalate delayed purchase orders",
                    "message": (
                        f"{delayed_orders:,} purchase orders are delayed "
                        "or overdue. Review expected delivery dates and "
                        "supplier commitments."
                    ),
                }
            )

        if supplier_rows:
            highest_risk_supplier = supplier_rows[0]

            supplier_name = (
                highest_risk_supplier.get(
                    "supplier_name"
                )
                or "The highest-risk supplier"
            )

            delay_rate = float(
                highest_risk_supplier.get(
                    "delay_rate",
                    0,
                )
            )

            recommendations.append(
                {
                    "severity": "warning",
                    "title": "Review supplier reliability",
                    "message": (
                        f"{supplier_name} has the highest listed delay "
                        f"rate at {delay_rate:.2f}%. Consider corrective "
                        "actions or backup sourcing options."
                    ),
                }
            )

        if warehouse_rows:
            highest_utilization = warehouse_rows[0]

            warehouse_name = (
                highest_utilization.get(
                    "warehouse_name"
                )
                or "The busiest warehouse"
            )

            utilization_percent = float(
                highest_utilization.get(
                    "utilization_percent",
                    0,
                )
            )

            if utilization_percent >= 85:
                recommendations.append(
                    {
                        "severity": "danger",
                        "title": "Warehouse capacity risk",
                        "message": (
                            f"{warehouse_name} is operating at "
                            f"{utilization_percent:.2f}% utilization. "
                            "Review inbound allocation and overflow capacity."
                        ),
                    }
                )

        if average_mape >= 20:
            recommendations.append(
                {
                    "severity": "info",
                    "title": "Improve forecast accuracy",
                    "message": (
                        f"Average forecast error is {average_mape:.2f}%. "
                        "Review products with consistently high forecast "
                        "variance before the next planning cycle."
                    ),
                }
            )

        if not recommendations:
            recommendations.append(
                {
                    "severity": "success",
                    "title": "Operations are within normal ranges",
                    "message": (
                        "No urgent inventory, supplier, warehouse, "
                        "or forecasting exceptions were detected."
                    ),
                }
            )

        return recommendations[:5]

    def _get_nested_value(
        self,
        row: Any,
        field_name: str,
    ) -> Any:
        """
        Safely read a field from a BigQuery nested row.
        """

        if isinstance(row, dict):
            return row.get(field_name)

        if hasattr(row, "get"):
            return row.get(field_name)

        return getattr(
            row,
            field_name,
            None,
        )

    def _empty_summary(self) -> dict[str, Any]:
        """
        Return a complete empty dashboard response.
        """

        return {
            "low_stock_products": 0,
            "total_suppliers": 0,
            "delayed_purchase_orders": 0,
            "open_purchase_orders": 0,
            "current_month_purchase_value": 0,
            "active_shipments": 0,
            "overall_average_mape": 0,
            "total_forecast_quantity": 0,
            "total_actual_quantity": 0,
            "supplier_delay_rates": [],
            "inventory_status_distribution": [],
            "purchase_order_trend": [],
            "warehouse_utilization": [],
            "shipment_status_distribution": [],
            "forecast_accuracy_distribution": [],
            "recommendations": [],
        }