from app.services.bigquery_schema_service import BigQuerySchemaService
from app.services.gemini_service import GeminiService


class SQLGeneratorService:
    """
    Converts natural-language supply-chain questions into GoogleSQL.

    The service reads the current approved BigQuery schema dynamically,
    gives that schema to Gemini, and returns generated SQL.

    This service does not execute SQL.
    """

    def __init__(self):
        self.gemini_service = GeminiService()
        self.schema_service = BigQuerySchemaService()

    def generate_sql(self, question: str) -> str:
        """
        Generate a read-only BigQuery SQL query for a user question.

        Args:
            question:
                Natural-language supply-chain question.

        Returns:
            A cleaned GoogleSQL SELECT statement, or CANNOT_ANSWER.
        """

        cleaned_question = question.strip()

        if not cleaned_question:
            return "CANNOT_ANSWER"

        schema_context = self.schema_service.get_schema_context()

        prompt = f"""
You are an expert supply-chain data analyst and Google BigQuery SQL developer.

Your task is to convert the user's business question into one valid,
read-only GoogleSQL query.

CURRENT APPROVED BIGQUERY SCHEMA
================================
{schema_context}

USER QUESTION
=============
{cleaned_question}

MANDATORY INSTRUCTIONS
======================
1. Return only the SQL query.
2. Do not include explanations before or after the SQL.
3. Do not wrap the SQL in Markdown code fences.
4. Generate only:
   - a SELECT statement, or
   - a WITH query ending in SELECT.
5. Never generate:
   INSERT, UPDATE, DELETE, MERGE, DROP, ALTER, CREATE, TRUNCATE,
   GRANT, REVOKE, CALL, EXECUTE, or EXPORT.
6. Use only the approved tables and columns included in the schema.
7. Fully qualify every table using the exact FULL TABLE ID shown
   in the schema and wrap it in backticks.
8. Use explicit column names instead of SELECT *.
9. Add LIMIT 100 for non-aggregate detail queries.
10. Use GoogleSQL syntax.
11. Use SAFE_DIVIDE when division could involve zero.
12. Use meaningful aliases for calculated columns.
13. Do not guess or invent table names or column names.
14. If the question cannot be answered from the supplied schema,
    return exactly:

CANNOT_ANSWER
"""

        generated_text = self.gemini_service.generate_response(
            prompt=prompt
        )

        return self._clean_generated_sql(
            generated_text=generated_text
        )

    @staticmethod
    def _clean_generated_sql(generated_text: str) -> str:
        """
        Remove accidental Markdown code fences and extra whitespace.
        """

        if not generated_text:
            return ""

        cleaned_sql = generated_text.strip()

        if cleaned_sql.startswith("```sql"):
            cleaned_sql = cleaned_sql[len("```sql"):].strip()
        elif cleaned_sql.startswith("```"):
            cleaned_sql = cleaned_sql[len("```"):].strip()

        if cleaned_sql.endswith("```"):
            cleaned_sql = cleaned_sql[:-3].strip()

        return cleaned_sql