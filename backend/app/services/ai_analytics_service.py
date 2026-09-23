import json
from typing import Any

from app.services.bigquery_ai_service import BigQueryAIService
from app.services.gemini_service import GeminiService
from app.services.result_formatter_service import ResultFormatterService
from app.services.sql_generator_service import SQLGeneratorService
from app.services.sql_validator_service import SQLValidatorService


class AIAnalyticsService:
    """
    Answers supply-chain questions using Gemini and BigQuery.

    Workflow:
    1. Convert the natural-language question into GoogleSQL.
    2. Validate the generated SQL.
    3. Execute the approved query in BigQuery.
    4. Format simple results directly in Python.
    5. Use Gemini only when a richer explanation is needed.
    """

    def __init__(self):
        self.sql_generator = SQLGeneratorService()
        self.sql_validator = SQLValidatorService()
        self.bigquery_service = BigQueryAIService()
        self.result_formatter = ResultFormatterService()
        self.gemini_service = GeminiService()

    def answer_question(
        self,
        question: str,
    ) -> dict[str, Any]:
        cleaned_question = question.strip()

        if not cleaned_question:
            return {
                "question": question,
                "generated_sql": None,
                "data": [],
                "answer": "Please enter a supply-chain question.",
                "answer_source": "python",
                "status": "invalid_question",
            }

        generated_sql = self.sql_generator.generate_sql(
            question=cleaned_question
        )

        validation_result = self.sql_validator.validate(
            sql_query=generated_sql
        )

        if not validation_result["is_valid"]:
            return {
                "question": cleaned_question,
                "generated_sql": generated_sql,
                "data": [],
                "answer": validation_result["error"],
                "answer_source": "validator",
                "status": "sql_rejected",
            }

        approved_sql = validation_result["sql"]

        query_results = self.bigquery_service.execute_query(
            query=approved_sql
        )

        if not query_results:
            return {
                "question": cleaned_question,
                "generated_sql": approved_sql,
                "data": [],
                "answer": (
                    "The query ran successfully, but no matching "
                    "supply-chain records were found."
                ),
                "answer_source": "python",
                "status": "no_results",
            }

        if self.result_formatter.can_format(
            question=cleaned_question,
            query_results=query_results,
        ):
            answer = self.result_formatter.format_result(
                question=cleaned_question,
                query_results=query_results,
            )

            return {
                "question": cleaned_question,
                "generated_sql": approved_sql,
                "data": query_results,
                "answer": answer,
                "answer_source": "python",
                "status": "success",
            }

        explanation_prompt = self._build_explanation_prompt(
            question=cleaned_question,
            sql_query=approved_sql,
            query_results=query_results,
        )

        answer = self.gemini_service.generate_response(
            prompt=explanation_prompt
        )

        return {
            "question": cleaned_question,
            "generated_sql": approved_sql,
            "data": query_results,
            "answer": answer,
            "answer_source": "gemini",
            "status": "success",
        }

    @staticmethod
    def _build_explanation_prompt(
        question: str,
        sql_query: str,
        query_results: list[dict[str, Any]],
    ) -> str:
        results_json = json.dumps(
            query_results,
            indent=2,
            default=str,
        )

        return f"""
You are an experienced supply-chain analyst.

A user asked the following business question:

{question}

The approved BigQuery SQL used to answer the question was:

{sql_query}

The query returned the following data:

{results_json}

INSTRUCTIONS
============
1. Answer the user's question directly.
2. Use only the supplied query results.
3. Do not invent suppliers, products, warehouses, dates, metrics,
   causes, or recommendations that are not supported by the data.
4. Clearly mention the most important value or result.
5. Briefly compare relevant records when multiple rows are returned.
6. Give practical supply-chain actions only when they are logically
   supported by the returned data.
7. If the data is insufficient for a conclusion, clearly say so.
8. Keep the response concise and business-friendly.
"""