import json
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
BACKEND_DIR = PROJECT_ROOT / "backend"

sys.path.append(str(BACKEND_DIR))


from app.services.ai_analytics_service import AIAnalyticsService


def main():
    question = "Which supplier has the longest average lead time?"

    analytics_service = AIAnalyticsService()

    print("\nUser question:\n")
    print(question)

    print("\nRunning the AI analytics pipeline...\n")

    result = analytics_service.answer_question(
        question=question
    )

    print("Pipeline result:\n")

    print(
        json.dumps(
            result,
            indent=2,
            default=str,
        )
    )

    print("\nSummary:\n")
    print("Status:", result["status"])
    print("Generated SQL:", result["generated_sql"])
    print("Rows returned:", len(result["data"]))
    print("AI answer:", result["answer"])


if __name__ == "__main__":
    main()