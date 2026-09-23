from google.cloud import bigquery

from app.config.settings import settings


class BigQuerySchemaService:
    """
    Loads and caches the current BigQuery dataset schema for Gemini.

    The first call reads the approved table schemas from BigQuery.
    Later calls reuse the cached text instead of requesting the
    same metadata repeatedly.
    """

    ALLOWED_TABLES = {
        "products",
        "inventory",
        "warehouses",
        "suppliers",
        "supplier_performance",
        "purchase_orders",
        "sales_orders",
        "demand_forecast",
        "shipments",
        "returns",
    }

    _schema_cache: str | None = None

    def __init__(self):
        self.client = bigquery.Client(
            project=settings.gcp_project_id
        )

        self.dataset_id = (
            f"{settings.gcp_project_id}."
            f"{settings.bigquery_dataset}"
        )

    def get_schema_context(
        self,
        force_refresh: bool = False,
    ) -> str:
        """
        Return the approved BigQuery schema as readable prompt text.

        Args:
            force_refresh:
                When True, ignore the cached schema and reload it
                from BigQuery.

        Returns:
            Formatted schema text for Gemini.
        """

        if (
            self.__class__._schema_cache is not None
            and not force_refresh
        ):
            return self.__class__._schema_cache

        schema_context = self._load_schema_context()

        self.__class__._schema_cache = schema_context

        return schema_context

    def refresh_schema_context(self) -> str:
        """
        Reload the schema from BigQuery and update the cache.
        """

        return self.get_schema_context(
            force_refresh=True
        )

    def clear_schema_cache(self) -> None:
        """
        Remove the cached schema.

        The next call to get_schema_context() will reload it from
        BigQuery.
        """

        self.__class__._schema_cache = None

    def _load_schema_context(self) -> str:
        """
        Read approved tables and columns from BigQuery.
        """

        schema_sections = []

        tables = self.client.list_tables(
            self.dataset_id
        )

        approved_tables = [
            table
            for table in tables
            if table.table_id in self.ALLOWED_TABLES
        ]

        approved_tables.sort(
            key=lambda table: table.table_id
        )

        for table_item in approved_tables:
            full_table_id = (
                f"{settings.gcp_project_id}."
                f"{settings.bigquery_dataset}."
                f"{table_item.table_id}"
            )

            table = self.client.get_table(
                full_table_id
            )

            schema_sections.append(
                self._format_table_schema(
                    table_name=table_item.table_id,
                    full_table_id=full_table_id,
                    schema=table.schema,
                )
            )

        if not schema_sections:
            return (
                "No approved supply-chain tables were found "
                "in the configured BigQuery dataset."
            )

        header = f"""
APPROVED BIGQUERY DATASET
=========================
Project:
{settings.gcp_project_id}

Dataset:
{settings.bigquery_dataset}

Only the tables and columns listed below may be used.
"""

        sql_rules = """
BIGQUERY SQL RULES
==================
- Use GoogleSQL syntax.
- Generate only SELECT statements or WITH queries ending in SELECT.
- Never generate INSERT, UPDATE, DELETE, MERGE, DROP, ALTER,
  CREATE, TRUNCATE, GRANT, REVOKE, CALL, EXECUTE, or EXPORT.
- Use only the approved tables and columns listed above.
- Fully qualify every table using backticks.
- Use explicit column names instead of SELECT *.
- Add LIMIT 100 to non-aggregate detail queries.
- Use SAFE_DIVIDE when division could involve zero.
- Use meaningful aliases for calculated columns.
- Do not access tables outside the configured project and dataset.
"""

        return (
            header.strip()
            + "\n\n"
            + "\n\n".join(schema_sections)
            + "\n\n"
            + sql_rules.strip()
        )

    @staticmethod
    def _format_table_schema(
        table_name: str,
        full_table_id: str,
        schema,
    ) -> str:
        """
        Convert one BigQuery table schema into readable prompt text.
        """

        column_lines = []

        for field in schema:
            column_lines.extend(
                BigQuerySchemaService._format_field(
                    field=field,
                    prefix="",
                )
            )

        formatted_columns = "\n".join(column_lines)

        return f"""
TABLE: {table_name}
FULL TABLE ID: `{full_table_id}`

COLUMNS:
{formatted_columns}
""".strip()

    @staticmethod
    def _format_field(
        field,
        prefix: str,
    ) -> list[str]:
        """
        Format standard and nested BigQuery fields.
        """

        field_name = (
            f"{prefix}.{field.name}"
            if prefix
            else field.name
        )

        mode = field.mode or "NULLABLE"

        lines = [
            (
                f"- {field_name}: "
                f"type={field.field_type}, "
                f"mode={mode}"
            )
        ]

        if field.fields:
            for nested_field in field.fields:
                lines.extend(
                    BigQuerySchemaService._format_field(
                        field=nested_field,
                        prefix=field_name,
                    )
                )

        return lines