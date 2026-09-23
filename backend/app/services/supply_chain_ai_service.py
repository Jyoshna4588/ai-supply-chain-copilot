import json
from typing import Any

from app.config.settings import settings
from app.services.bigquery_ai_service import BigQueryAIService
from app.services.gemini_service import GeminiService


class SupplyChainAIService:
    """
    Provides predefined supply-chain analytics workflows.

    These workflows use fixed, tested BigQuery SQL for common business
    questions. This avoids asking Gemini to generate SQL every time.

    Gemini is still used for broader analytical explanations where it
    adds value.
    """

    def __init__(self):
        self.bigquery_service = BigQueryAIService()
        self.gemini_service = GeminiService()

    def get_supplier_longest_lead_time(self) -> dict[str, Any]:
        """
        Return the supplier with the longest average lead time.

        This is a fast path:
        - predefined SQL
        - one BigQuery query
        - Python-formatted answer
        - no Gemini call
        """

        query = f"""
            SELECT
                supplier_id,
                supplier_name,
                average_lead_time
            FROM
                `{settings.gcp_project_id}.{settings.bigquery_dataset}.supplier_performance`
            WHERE
                average_lead_time IS NOT NULL
            ORDER BY
                average_lead_time DESC
            LIMIT 1
        """

        query_results = self.bigquery_service.execute_query(
            query=query
        )

        if not query_results:
            return {
                "question": (
                    "Which supplier has the longest average lead time?"
                ),
                "generated_sql": query.strip(),
                "data": [],
                "answer": (
                    "No supplier lead-time records were found."
                ),
                "answer_source": "python",
                "status": "no_results",
            }

        supplier = query_results[0]

        supplier_name = supplier.get(
            "supplier_name",
            "The supplier",
        )

        average_lead_time = supplier.get(
            "average_lead_time"
        )

        answer = (
            f"{supplier_name} has the longest average lead time "
            f"at {average_lead_time} days."
        )

        return {
            "question": (
                "Which supplier has the longest average lead time?"
            ),
            "generated_sql": query.strip(),
            "data": query_results,
            "answer": answer,
            "answer_source": "python",
            "status": "success",
        }

    def get_supplier_highest_delay_rate(self) -> dict[str, Any]:
        """
        Return the supplier with the highest delivery delay rate.

        This is also a fast path and does not call Gemini.
        """

        query = f"""
            SELECT
                supplier_id,
                supplier_name,
                delayed_orders,
                total_orders,
                delay_rate
            FROM
                `{settings.gcp_project_id}.{settings.bigquery_dataset}.supplier_performance`
            WHERE
                delay_rate IS NOT NULL
            ORDER BY
                delay_rate DESC
            LIMIT 1
        """

        query_results = self.bigquery_service.execute_query(
            query=query
        )

        if not query_results:
            return {
                "question": (
                    "Which supplier has the highest delay rate?"
                ),
                "generated_sql": query.strip(),
                "data": [],
                "answer": (
                    "No supplier delay-rate records were found."
                ),
                "answer_source": "python",
                "status": "no_results",
            }

        supplier = query_results[0]

        supplier_name = supplier.get(
            "supplier_name",
            "The supplier",
        )

        delay_rate = supplier.get(
            "delay_rate"
        )

        answer = (
            f"{supplier_name} has the highest delay rate "
            f"at {delay_rate}%."
        )

        return {
            "question": (
                "Which supplier has the highest delay rate?"
            ),
            "generated_sql": query.strip(),
            "data": query_results,
            "answer": answer,
            "answer_source": "python",
            "status": "success",
        }

    def get_low_stock_warehouse_insight(self) -> dict[str, Any]:
        """
        Analyze warehouses with the greatest low-stock exposure.

        This broader comparison still uses Gemini because it requests
        comparison and recommendations across multiple warehouses.
        """

        query = f"""
            SELECT
                inventory.warehouse_id,
                warehouses.warehouse_name,
                COUNT(DISTINCT inventory.product_id)
                    AS low_stock_count
            FROM
                `{settings.gcp_project_id}.{settings.bigquery_dataset}.inventory`
                    AS inventory
            LEFT JOIN
                `{settings.gcp_project_id}.{settings.bigquery_dataset}.warehouses`
                    AS warehouses
                ON inventory.warehouse_id = warehouses.warehouse_id
            WHERE
                inventory.available_stock
                    < inventory.reorder_point
            GROUP BY
                inventory.warehouse_id,
                warehouses.warehouse_name
            ORDER BY
                low_stock_count DESC
            LIMIT 5
        """

        query_results = self.bigquery_service.execute_query(
            query=query
        )

        if not query_results:
            return {
                "question": (
                    "Which warehouse has the highest low-stock risk?"
                ),
                "generated_sql": query.strip(),
                "data": [],
                "answer": (
                    "No low-stock warehouse records were found."
                ),
                "answer_source": "python",
                "status": "no_results",
            }

        prompt = f"""
You are a supply-chain inventory analyst.

The following data shows the five warehouses with the highest number
of products below their reorder point:

{json.dumps(query_results, indent=2, default=str)}

Provide:
1. The warehouse with the highest stockout risk.
2. A brief comparison with the other warehouses.
3. Two practical actions the supply-chain team should take.

Use only the supplied data.
Do not invent facts.
Keep the answer clear and concise.
"""

        answer = self.gemini_service.generate_response(
            prompt=prompt
        )

        return {
            "question": (
                "Which warehouse has the highest low-stock risk?"
            ),
            "generated_sql": query.strip(),
            "data": query_results,
            "answer": answer,
            "answer_source": "gemini",
            "status": "success",
        }

    def get_supplier_performance_insight(self) -> dict[str, Any]:
        """
        Return a broader supplier-risk analysis.

        Gemini is used here because the answer compares several metrics
        and suppliers rather than returning one deterministic value.
        """

        query = f"""
            SELECT
                supplier_id,
                supplier_name,
                risk_profile,
                total_orders,
                delayed_orders,
                delay_rate,
                otif_rate,
                average_lead_time,
                quality_rating,
                defect_rate,
                cost_score
            FROM
                `{settings.gcp_project_id}.{settings.bigquery_dataset}.supplier_performance`
            ORDER BY
                delay_rate DESC,
                otif_rate ASC,
                defect_rate DESC
            LIMIT 5
        """

        query_results = self.bigquery_service.execute_query(
            query=query
        )

        if not query_results:
            return {
                "question": (
                    "Which suppliers have the highest delivery risk?"
                ),
                "generated_sql": query.strip(),
                "data": [],
                "answer": (
                    "No supplier-performance records were found."
                ),
                "answer_source": "python",
                "status": "no_results",
            }

        prompt = f"""
You are a supply-chain procurement analyst.

The following data shows suppliers with the greatest delivery risk:

{json.dumps(query_results, indent=2, default=str)}

Interpret the metrics as follows:
- Higher delay_rate means more delivery risk.
- Lower otif_rate means poorer on-time and in-full performance.
- Higher defect_rate means greater quality risk.
- Higher average_lead_time means slower replenishment.

Provide:
1. The supplier with the highest overall delivery risk.
2. A short comparison with the other suppliers.
3. Two practical procurement actions.

Use only the supplied data.
Do not invent facts.
Keep the answer clear and concise.
"""

        answer = self.gemini_service.generate_response(
            prompt=prompt
        )

        return {
            "question": (
                "Which suppliers have the highest delivery risk?"
            ),
            "generated_sql": query.strip(),
            "data": query_results,
            "answer": answer,
            "answer_source": "gemini",
            "status": "success",
        }