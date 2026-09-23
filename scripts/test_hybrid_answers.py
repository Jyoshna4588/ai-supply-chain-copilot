import json
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
BACKEND_DIR = PROJECT_ROOT / "backend"

sys.path.append(str(BACKEND_DIR))


from app.services.ai_analytics_service import AIAnalyticsService


QUESTIONS = [
    "Which supplier has the longest average lead time?",
    "Show inventory health.",
]


def main():
    analytics_service = AIAnalyticsService()

    for index, question in enumerate(QUESTIONS, start=1):
        print("=" * 80)
        print(f"Question {index}")
        print("=" * 80)
        print(question)
        print()

        result = analytics_service.answer_question(
            question=question
        )

        print(
            json.dumps(
                result,
                indent=2,
                default=str,
            )
        )

        print()
        print("Answer source:", result.get("answer_source"))
        print("Status:", result.get("status"))
        print()


if __name__ == "__main__":
    main()