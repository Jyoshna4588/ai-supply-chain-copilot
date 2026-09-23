import json
import logging
import re
from datetime import date, datetime
from decimal import Decimal
from functools import lru_cache
from typing import Any

from langchain.tools import tool

from app.models.ai_response import SupplyChainAnalysisResult
from app.services.ai_analytics_service import AIAnalyticsService
from app.services.bigquery_ai_service import BigQueryAIService
from app.services.question_router_service import QuestionRouterService
from app.services.rag_retrieval_service import (
    RAGRetrievalService,
    get_rag_retrieval_service,
)
from app.services.supply_chain_ai_service import SupplyChainAIService


logger = logging.getLogger("SupplyChainAI")


BLOCKED_SQL_PATTERN = re.compile(
    r"\b("
    r"INSERT|UPDATE|DELETE|MERGE|DROP|ALTER|TRUNCATE|CREATE|REPLACE|"
    r"GRANT|REVOKE|CALL|EXPORT|LOAD"
    r")\b",
    flags=re.IGNORECASE,
)


@lru_cache(maxsize=1)
def get_bigquery_service() -> BigQueryAIService:
    """
    Return one shared BigQuery service instance.
    """
    return BigQueryAIService()


@lru_cache(maxsize=1)
def get_ai_analytics_service() -> AIAnalyticsService:
    """
    Return one shared analytics service instance.
    """
    return AIAnalyticsService()


@lru_cache(maxsize=1)
def get_question_router() -> QuestionRouterService:
    """
    Return one shared question-router instance.
    """
    return QuestionRouterService()


@lru_cache(maxsize=1)
def get_supply_chain_service() -> SupplyChainAIService:
    """
    Return one shared predefined-workflow service.
    """
    return SupplyChainAIService()


def validate_read_only_sql(query: str) -> str:
    """
    Validate and normalize SQL before sending it to BigQuery.

    Only a single SELECT query or WITH query is permitted.
    """
    normalized_query = query.strip().rstrip(";").strip()

    if not normalized_query:
        raise ValueError("The SQL query cannot be empty.")

    first_keyword = normalized_query.split(
        maxsplit=1
    )[0].upper()

    if first_keyword not in {"SELECT", "WITH"}:
        raise ValueError(
            "Only read-only SELECT queries are allowed."
        )

    if BLOCKED_SQL_PATTERN.search(normalized_query):
        raise ValueError(
            "The query contains a prohibited SQL operation."
        )

    if ";" in normalized_query:
        raise ValueError(
            "Multiple SQL statements are not allowed."
        )

    return normalized_query


def make_json_safe(value: Any) -> Any:
    """
    Convert common BigQuery values into JSON-safe Python values.

    This handles values such as Decimal, date, and datetime while
    preserving normal dictionaries and lists.
    """
    if isinstance(value, dict):
        return {
            str(key): make_json_safe(item)
            for key, item in value.items()
        }

    if isinstance(value, list):
        return [
            make_json_safe(item)
            for item in value
        ]

    if isinstance(value, tuple):
        return [
            make_json_safe(item)
            for item in value
        ]

    if isinstance(value, Decimal):
        return float(value)

    if isinstance(value, (datetime, date)):
        return value.isoformat()

    return value


def build_tool_content(
    result: SupplyChainAnalysisResult,
) -> str:
    """
    Build concise, model-readable analytics tool content.

    The model receives this JSON text. The application receives the
    original structured result separately through ToolMessage.artifact.
    """
    model_payload = {
        "question": result.question,
        "intent": result.intent,
        "generated_sql": result.generated_sql,
        "data": result.data,
        "answer": result.answer,
        "answer_source": result.answer_source,
        "status": result.status,
    }

    return json.dumps(
        make_json_safe(model_payload),
        default=str,
    )


def build_rag_tool_content(
    question: str,
    results: list[dict[str, Any]],
) -> str:
    """
    Build model-readable content from retrieved documents.
    """
    model_payload = {
        "question": question,
        "retrieval_type": "rag",
        "result_count": len(results),
        "documents": [
            {
                "rank": item.get("rank"),
                "source": item.get("source"),
                "page": item.get("page"),
                "chunk_number": item.get("chunk_number"),
                "text": item.get("text", ""),
            }
            for item in results
        ],
    }

    return json.dumps(
        make_json_safe(model_payload),
        default=str,
    )


@tool
def execute_bigquery_sql(
    query: str,
) -> dict[str, Any]:
    """
    Execute an approved, read-only GoogleSQL query against BigQuery.

    This low-level tool accepts only one SELECT query or one query
    beginning with a WITH clause. It rejects data-changing SQL.

    Args:
        query:
            A complete GoogleSQL query using fully qualified table names.

    Returns:
        Query status, row count, and returned rows.
    """
    try:
        approved_query = validate_read_only_sql(
            query
        )

        logger.info(
            "LangChain BigQuery tool invoked"
        )

        rows = get_bigquery_service().execute_query(
            query=approved_query
        )

        safe_rows = make_json_safe(rows)

        return {
            "status": "success",
            "row_count": len(safe_rows),
            "rows": safe_rows,
        }

    except ValueError as exc:
        logger.warning(
            "LangChain BigQuery tool rejected query | reason=%s",
            exc,
        )

        return {
            "status": "rejected",
            "error": str(exc),
            "row_count": 0,
            "rows": [],
        }

    except Exception:
        logger.exception(
            "LangChain BigQuery tool execution failed"
        )

        return {
            "status": "error",
            "error": (
                "The BigQuery query could not be completed."
            ),
            "row_count": 0,
            "rows": [],
        }


@tool(
    response_format="content_and_artifact"
)
def analyze_supply_chain_data(
    question: str,
) -> tuple[str, dict[str, Any]]:
    """
    Answer a question using the company's structured supply-chain data.

    Use this tool whenever the user asks about actual company suppliers,
    warehouses, products, inventory, orders, shipments, lead times,
    delays, stock levels, performance metrics, rankings, totals, or
    other operational records.

    Do not use this tool for contracts, policies, SOPs, procurement
    documents, or other unstructured company documents. Use the
    document retrieval tool for those questions.

    Do not use this tool for general conceptual questions, definitions,
    generic examples, or industry best practices that do not require
    company data.

    Args:
        question:
            The user's complete supply-chain analytics question.

    Returns:
        A two-item tuple:

        1. Model-readable content.
        2. A structured artifact used by the application.
    """
    cleaned_question = question.strip()

    if not cleaned_question:
        result = SupplyChainAnalysisResult(
            question=question,
            intent="invalid_question",
            generated_sql=None,
            data=[],
            answer="Please enter a question.",
            answer_source="python",
            status="invalid_question",
        )

        return (
            build_tool_content(result),
            result.model_dump(),
        )

    try:
        logger.info(
            "Supply-chain analytics tool started"
        )

        intent = get_question_router().detect_intent(
            question=cleaned_question
        )

        supply_chain_service = (
            get_supply_chain_service()
        )

        predefined_workflows = {
            "supplier_lead_time": (
                supply_chain_service
                .get_supplier_longest_lead_time
            ),
            "supplier_delay_rate": (
                supply_chain_service
                .get_supplier_highest_delay_rate
            ),
            "low_stock_warehouses": (
                supply_chain_service
                .get_low_stock_warehouse_insight
            ),
            "supplier_performance": (
                supply_chain_service
                .get_supplier_performance_insight
            ),
        }

        workflow = predefined_workflows.get(
            intent
        )

        if workflow is not None:
            workflow_result = workflow()

            result = SupplyChainAnalysisResult(
                question=cleaned_question,
                intent=intent,
                generated_sql=workflow_result.get(
                    "generated_sql"
                ),
                data=make_json_safe(
                    workflow_result.get(
                        "data",
                        [],
                    )
                ),
                answer=workflow_result.get(
                    "answer",
                    "No answer was generated.",
                ),
                answer_source=workflow_result.get(
                    "answer_source",
                    "workflow",
                ),
                status=workflow_result.get(
                    "status",
                    "success",
                ),
            )

            logger.info(
                "Predefined workflow completed | "
                "intent=%s | status=%s",
                result.intent,
                result.status,
            )

            return (
                build_tool_content(result),
                result.model_dump(),
            )

        analytics_result = (
            get_ai_analytics_service().answer_question(
                question=cleaned_question
            )
        )

        result = SupplyChainAnalysisResult(
            question=cleaned_question,
            intent=intent,
            generated_sql=analytics_result.get(
                "generated_sql"
            ),
            data=make_json_safe(
                analytics_result.get(
                    "data",
                    [],
                )
            ),
            answer=analytics_result.get(
                "answer",
                "No answer was generated.",
            ),
            answer_source=analytics_result.get(
                "answer_source",
                "gemini",
            ),
            status=analytics_result.get(
                "status",
                "failed",
            ),
        )

        logger.info(
            "Generic analytics workflow completed | "
            "intent=%s | status=%s",
            result.intent,
            result.status,
        )

        return (
            build_tool_content(result),
            result.model_dump(),
        )

    except Exception:
        logger.exception(
            "Supply-chain analytics tool failed"
        )

        result = SupplyChainAnalysisResult(
            question=cleaned_question,
            intent="unknown",
            generated_sql=None,
            data=[],
            answer=(
                "The supply-chain analysis could not be "
                "completed."
            ),
            answer_source="python",
            status="error",
        )

        return (
            build_tool_content(result),
            result.model_dump(),
        )


@tool(
    response_format="content_and_artifact"
)
def retrieve_supply_chain_documents(
    question: str,
) -> tuple[str, dict[str, Any]]:
    """
    Search the company's supply-chain documents using semantic retrieval.

    Use this tool when the user asks about information contained in
    supplier contracts, procurement policies, supplier-management
    policies, inventory SOPs, warehouse SOPs, or other internal
    supply-chain documents.

    This tool searches the Vertex AI Vector Search knowledge base and
    returns the most relevant document chunks with their source file,
    page, and chunk information.

    Use this tool together with analyze_supply_chain_data when a
    question requires both operational data and document guidance.

    Args:
        question:
            The user's complete document or policy question.

    Returns:
        A two-item tuple:

        1. Retrieved document context for the model.
        2. Structured retrieval metadata for the application.
    """
    cleaned_question = question.strip()

    if not cleaned_question:
        artifact = {
            "question": question,
            "intent": "document_retrieval",
            "status": "invalid_question",
            "answer_source": "rag",
            "data": [],
            "sources": [],
        }

        return (
            json.dumps(artifact),
            artifact,
        )

    try:
        logger.info(
            "Supply-chain document retrieval started"
        )

        rag_service: RAGRetrievalService = (
            get_rag_retrieval_service()
        )

        results = rag_service.search(
            query=cleaned_question,
        )

        sources = []

        for item in results:
            source_entry = {
                "source": item.get("source"),
                "page": item.get("page"),
                "chunk_number": item.get(
                    "chunk_number"
                ),
                "rank": item.get("rank"),
            }

            if source_entry not in sources:
                sources.append(source_entry)

        artifact = {
            "question": cleaned_question,
            "intent": "document_retrieval",
            "status": (
                "success"
                if results
                else "no_results"
            ),
            "answer_source": "rag",
            "data": make_json_safe(results),
            "sources": sources,
        }

        logger.info(
            "Supply-chain document retrieval completed | "
            "results=%s",
            len(results),
        )

        return (
            build_rag_tool_content(
                question=cleaned_question,
                results=results,
            ),
            artifact,
        )

    except Exception:
        logger.exception(
            "Supply-chain document retrieval failed"
        )

        artifact = {
            "question": cleaned_question,
            "intent": "document_retrieval",
            "status": "error",
            "answer_source": "rag",
            "data": [],
            "sources": [],
        }

        content = json.dumps(
            {
                "question": cleaned_question,
                "retrieval_type": "rag",
                "status": "error",
                "message": (
                    "The supply-chain documents could "
                    "not be retrieved."
                ),
            }
        )

        return (
            content,
            artifact,
        )


# The agent receives the two high-level enterprise capabilities:
#
# 1. Structured operational analytics through BigQuery.
# 2. Unstructured document retrieval through Vertex AI Vector Search.
#
# The raw SQL tool remains available for controlled internal use,
# testing, or a future schema-aware database agent.
SUPPLY_CHAIN_TOOLS = [
    analyze_supply_chain_data,
    retrieve_supply_chain_documents,
]