from typing import Any

from langchain_core.messages import (
    AIMessage,
    BaseMessage,
    ToolMessage,
)

from app.graph.state import SupplyChainAgentResponse
from app.models.ai_response import SupplyChainAnalysisResult


SPECIALIST_TOOL_NAMES = {
    "inventory_agent",
    "supplier_agent",
    "demand_forecast_agent",
    "procurement_agent",
    "document_retrieval_agent",
}


def extract_text_content(
    message: BaseMessage | None,
) -> str:
    """
    Extract plain text from a LangChain message.
    """
    if message is None:
        return ""

    content = message.content

    if isinstance(content, str):
        return content.strip()

    if isinstance(content, list):
        text_parts: list[str] = []

        for block in content:
            if isinstance(block, str):
                text_parts.append(block)
                continue

            if isinstance(block, dict):
                text = block.get("text")

                if isinstance(text, str):
                    text_parts.append(text)

        return "\n".join(text_parts).strip()

    return str(content).strip()


def find_final_ai_message(
    messages: list[BaseMessage],
) -> AIMessage | None:
    """
    Return the final AI message from supervisor execution.
    """
    for message in reversed(messages):
        if isinstance(message, AIMessage):
            return message

    return None


def extract_specialist_artifact(
    messages: list[BaseMessage],
) -> dict[str, Any] | None:
    """
    Find the most recent specialist-agent artifact.
    """
    for message in reversed(messages):
        if not isinstance(message, ToolMessage):
            continue

        if message.name not in SPECIALIST_TOOL_NAMES:
            continue

        artifact = message.artifact

        if isinstance(artifact, dict):
            return artifact

    return None


def extract_legacy_analytics_artifact(
    messages: list[BaseMessage],
) -> SupplyChainAnalysisResult | None:
    """
    Preserve compatibility with the previous single-agent architecture.
    """
    for message in reversed(messages):
        if not isinstance(message, ToolMessage):
            continue

        if message.name != "analyze_supply_chain_data":
            continue

        artifact: Any = message.artifact

        if artifact is None:
            continue

        try:
            return (
                SupplyChainAnalysisResult
                .model_validate(artifact)
            )

        except Exception:
            continue

    return None


def build_api_response(
    question: str,
    thread_id: str,
    messages: list[BaseMessage],
) -> SupplyChainAgentResponse:
    """
    Convert supervisor execution into the existing FastAPI response
    contract without requiring frontend changes.
    """
    final_ai_message = find_final_ai_message(
        messages
    )

    final_answer = extract_text_content(
        final_ai_message
    )

    specialist_artifact = extract_specialist_artifact(
        messages
    )

    if specialist_artifact is not None:
        specialist = specialist_artifact.get(
            "specialist",
            "specialist",
        )

        data = specialist_artifact.get(
            "data",
            [],
        )

        if not isinstance(data, list):
            data = []

        return {
            "question": question,
            "thread_id": thread_id,
            "intent": str(specialist),
            "generated_sql": specialist_artifact.get(
                "generated_sql"
            ),
            "data": data,
            "answer": (
                final_answer
                or specialist_artifact.get(
                    "answer"
                )
                or "No answer was generated."
            ),
            "answer_source": "multi_agent",
            "status": specialist_artifact.get(
                "status",
                "success",
            ),
        }

    legacy_result = extract_legacy_analytics_artifact(
        messages
    )

    if legacy_result is not None:
        return {
            "question": question,
            "thread_id": thread_id,
            "intent": legacy_result.intent,
            "generated_sql": (
                legacy_result.generated_sql
            ),
            "data": legacy_result.data,
            "answer": (
                final_answer
                or legacy_result.answer
            ),
            "answer_source": (
                legacy_result.answer_source
            ),
            "status": legacy_result.status,
        }

    return {
        "question": question,
        "thread_id": thread_id,
        "intent": "general",
        "generated_sql": None,
        "data": [],
        "answer": (
            final_answer
            or "No answer was generated."
        ),
        "answer_source": "agent",
        "status": "general_answer",
    }