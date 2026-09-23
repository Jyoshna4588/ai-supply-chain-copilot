from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class SupplyChainAnalysisResult(BaseModel):
    """
    Validated result produced by a supply-chain analytics workflow.

    This model is used internally by LangChain tools and the graph
    response-building layer.
    """

    model_config = ConfigDict(
        extra="ignore",
        arbitrary_types_allowed=True,
    )

    question: str
    intent: str = "unknown"
    generated_sql: str | None = None
    data: list[dict[str, Any]] = Field(default_factory=list)
    answer: str
    answer_source: str = "python"
    status: str = "success"


class AIQueryRequest(BaseModel):
    """
    Request body accepted by POST /ai/query.

    thread_id identifies one conversation. Reusing the same thread_id
    allows the agent to remember earlier messages.
    """

    model_config = ConfigDict(
        extra="ignore",
    )

    question: str = Field(
        min_length=1,
        description="Natural-language question for the AI Copilot.",
    )

    thread_id: str | None = Field(
        default=None,
        description=(
            "Conversation identifier. Reuse the same value for "
            "follow-up questions."
        ),
    )


class AIQueryResponse(BaseModel):
    """
    Standard response returned by POST /ai/query.

    The original fields remain compatible with the frontend.
    thread_id is added so the client can continue the conversation.
    """

    model_config = ConfigDict(
        extra="ignore",
        arbitrary_types_allowed=True,
    )

    question: str
    thread_id: str
    intent: str
    generated_sql: str | None = None
    data: list[dict[str, Any]] = Field(default_factory=list)
    answer: str
    answer_source: str
    status: str