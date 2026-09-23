from typing import Any


class ResultFormatterService:
    """
    Formats simple BigQuery results into clear business answers.

    This reduces the need for a second Gemini call when the result is
    straightforward and deterministic.
    """

    def can_format(
        self,
        question: str,
        query_results: list[dict[str, Any]],
    ) -> bool:
        """
        Return True when the result can be safely formatted in Python.
        """

        if not query_results:
            return False

        if len(query_results) != 1:
            return False

        row = query_results[0]
        columns = set(row.keys())

        supported_column_sets = [
            {"supplier_name", "average_lead_time"},
            {"supplier_name", "delay_rate"},
            {
                "warehouse_id",
                "warehouse_name",
                "low_stock_product_count",
            },
            {
                "warehouse_id",
                "low_stock_product_count",
            },
        ]

        return any(
            required_columns.issubset(columns)
            for required_columns in supported_column_sets
        )

    def format_result(
        self,
        question: str,
        query_results: list[dict[str, Any]],
    ) -> str:
        """
        Format a supported one-row query result.
        """

        if not query_results:
            return "No matching supply-chain records were found."

        row = query_results[0]

        if {
            "supplier_name",
            "average_lead_time",
        }.issubset(row):
            return (
                f"{row['supplier_name']} has the longest average "
                f"lead time at {row['average_lead_time']} days."
            )

        if {
            "supplier_name",
            "delay_rate",
        }.issubset(row):
            return (
                f"{row['supplier_name']} has the highest delay rate "
                f"at {row['delay_rate']}%."
            )

        if {
            "warehouse_id",
            "warehouse_name",
            "low_stock_product_count",
        }.issubset(row):
            return (
                f"{row['warehouse_name']} ({row['warehouse_id']}) has "
                f"the highest number of low-stock products, with "
                f"{row['low_stock_product_count']} products."
            )

        if {
            "warehouse_id",
            "low_stock_product_count",
        }.issubset(row):
            return (
                f"Warehouse {row['warehouse_id']} has the highest "
                f"number of low-stock products, with "
                f"{row['low_stock_product_count']} products."
            )

        return (
            "The query completed successfully, but this result requires "
            "a richer explanation."
        )