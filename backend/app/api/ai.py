from typing import Any

from fastapi import APIRouter

from app.models.ai_response import (
    AIQueryRequest,
    AIQueryResponse,
)
from app.services.ai_query_service import AIQueryService
from app.services.gemini_service import GeminiService


router = APIRouter(
    prefix="/ai",
    tags=["AI"],
)


ai_query_service = AIQueryService()
gemini_service = GeminiService()


@router.post(
    "/chat",
    response_model=dict[str, Any],
)
def chat(
    request: AIQueryRequest,
) -> dict[str, Any]:
    """
    Send a general message to Gemini.

    This endpoint does not query company data.
    """
    answer = gemini_service.generate_response(
        prompt=request.question
    )

    return {
        "question": request.question,
        "answer": answer,
        "status": "success",
    }


@router.post(
    "/query",
    response_model=AIQueryResponse,
)
def query_ai(
    request: AIQueryRequest,
) -> dict[str, Any]:
    """
    Ask the AI Supply Chain Copilot a question.

    Reuse thread_id across requests to preserve conversation memory.
    When thread_id is omitted, a new conversation is created.
    """
    return ai_query_service.answer_question(
        question=request.question,
        thread_id=request.thread_id,
    )