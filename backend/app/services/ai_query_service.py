import logging
from typing import Any
from uuid import uuid4

from langchain_core.messages import HumanMessage
from langchain_core.runnables import RunnableConfig

from app.graph.graph import get_supply_chain_agent
from app.graph.nodes import build_api_response
from app.models.ai_response import AIQueryResponse


logger = logging.getLogger("SupplyChainAI")


class AIQueryService:
    """
    Answer questions through the LangGraph-powered supply-chain agent.

    A thread_id is used to associate multiple requests with the same
    conversation history.
    """

    def __init__(self):
        self.agent = get_supply_chain_agent()

    def answer_question(
        self,
        question: str,
        thread_id: str | None = None,
    ) -> dict[str, Any]:
        """
        Answer a question and preserve conversation history.

        Args:
            question:
                The user's current natural-language question.

            thread_id:
                Optional conversation identifier. When the same value is
                reused, LangGraph loads the previous conversation state.

        Returns:
            A dictionary matching the API response model.
        """
        cleaned_question = question.strip()

        conversation_id = (
            thread_id.strip()
            if thread_id and thread_id.strip()
            else str(uuid4())
        )

        if not cleaned_question:
            response = AIQueryResponse(
                question=question,
                thread_id=conversation_id,
                intent="invalid_question",
                generated_sql=None,
                data=[],
                answer="Please enter a question.",
                answer_source="python",
                status="invalid_question",
            )

            return response.model_dump()

        try:
            logger.info(
                "Supply-chain agent started | thread_id=%s",
                conversation_id,
            )

            config: RunnableConfig = {
                "configurable": {
                    "thread_id": conversation_id,
                }
            }

            result = self.agent.invoke(
                {
                    "messages": [
                        HumanMessage(
                            content=cleaned_question
                        )
                    ]
                },
                config=config,
            )

            messages = result.get(
                "messages",
                [],
            )

            raw_response = build_api_response(
                question=cleaned_question,
                thread_id=conversation_id,
                messages=messages,
            )

            validated_response = (
                AIQueryResponse.model_validate(
                    raw_response
                )
            )

            logger.info(
                "Supply-chain agent completed | "
                "thread_id=%s | intent=%s | status=%s | "
                "used_company_data=%s",
                conversation_id,
                validated_response.intent,
                validated_response.status,
                (
                    validated_response.generated_sql
                    is not None
                ),
            )

            return validated_response.model_dump()

        except Exception:
            logger.exception(
                "Supply-chain agent execution failed | "
                "thread_id=%s",
                conversation_id,
            )

            response = AIQueryResponse(
                question=cleaned_question,
                thread_id=conversation_id,
                intent="agent_error",
                generated_sql=None,
                data=[],
                answer=(
                    "The AI Copilot could not process the "
                    "question at this time."
                ),
                answer_source="python",
                status="error",
            )

            return response.model_dump()