import json
import sys
import time
from pathlib import Path

from google.genai.errors import ClientError


PROJECT_ROOT = Path(__file__).resolve().parent.parent
BACKEND_DIR = PROJECT_ROOT / "backend"

sys.path.append(str(BACKEND_DIR))


from app.services.ai_analytics_service import AIAnalyticsService


QUESTIONS = [
    "Which warehouse has the highest low stock products?",
    "Which products are low in stock?",
    "Show inventory health.",
    "Which supplier has the longest average lead time?",
    "Which supplier has the highest delay rate?",
    "Show supplier performance.",
    "Which purchase orders are delayed?",
    "Show open purchase orders.",
    "Which shipments are delayed?",
    "Show shipment delays.",
    "Which products have the highest forecast error?",
    "Which products have the highest return quantity?",
]


MAX_RETRIES = 3
INITIAL_RETRY_DELAY_SECONDS = 10
DELAY_BETWEEN_QUESTIONS_SECONDS = 8


def run_question_with_retry(
    analytics: AIAnalyticsService,
    question: str,
) -> dict:
    retry_delay = INITIAL_RETRY_DELAY_SECONDS

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            return analytics.answer_question(question)

        except ClientError as exc:
            error_text = str(exc)

            is_resource_exhausted = (
                "429" in error_text
                or "RESOURCE_EXHAUSTED" in error_text
            )

            if not is_resource_exhausted:
                raise

            if attempt == MAX_RETRIES:
                return {
                    "question": question,
                    "generated_sql": None,
                    "data": [],
                    "answer": (
                        "Vertex AI remained temporarily unavailable "
                        "after multiple retries."
                    ),
                    "status": "resource_exhausted",
                }

            print(
                f"Vertex AI returned 429. "
                f"Retrying in {retry_delay} seconds..."
            )

            time.sleep(retry_delay)
            retry_delay *= 2

    return {
        "question": question,
        "generated_sql": None,
        "data": [],
        "answer": "The question could not be processed.",
        "status": "failed",
    }


def main():
    analytics = AIAnalyticsService()

    for index, question in enumerate(QUESTIONS, start=1):
        print("=" * 80)
        print(f"Question {index}")
        print("=" * 80)
        print(question)
        print()

        result = run_question_with_retry(
            analytics=analytics,
            question=question,
        )

        print("Status:")
        print(result["status"])
        print()

        print("Generated SQL:")
        print(result.get("generated_sql"))
        print()

        print("Rows Returned:")
        print(len(result.get("data", [])))
        print()

        print("Answer:")
        print(result.get("answer"))
        print()

        if index < len(QUESTIONS):
            print(
                f"Waiting {DELAY_BETWEEN_QUESTIONS_SECONDS} seconds "
                "before the next question..."
            )
            print()

            time.sleep(DELAY_BETWEEN_QUESTIONS_SECONDS)


if __name__ == "__main__":
    main()   