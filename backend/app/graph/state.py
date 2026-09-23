from typing import Any, TypedDict


class SupplyChainAgentResponse(TypedDict):
    """
    Standard response returned to the FastAPI layer.
    """

    question: str
    thread_id: str
    intent: str
    generated_sql: str | None
    data: list[dict[str, Any]]
    answer: str
    answer_source: str
    status: str