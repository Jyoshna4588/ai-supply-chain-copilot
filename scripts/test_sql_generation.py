import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
BACKEND_DIR = PROJECT_ROOT / "backend"

sys.path.append(str(BACKEND_DIR))


from app.services.sql_generator_service import SQLGeneratorService
from app.services.sql_validator_service import SQLValidatorService


def main():
    question = "Which supplier has the longest average lead time?"

    sql_generator = SQLGeneratorService()
    sql_validator = SQLValidatorService()

    print("\nUser question:\n")
    print(question)

    print("\nGenerating SQL with Gemini...\n")

    generated_sql = sql_generator.generate_sql(
        question=question
    )

    print("Generated SQL:\n")
    print(generated_sql)

    validation_result = sql_validator.validate(
        sql_query=generated_sql
    )

    print("\nValidation result:\n")
    print(validation_result)

    if validation_result["is_valid"]:
        print("\nThe generated SQL passed validation.")
    else:
        print("\nThe generated SQL was rejected.")
        print(
            "Reason:",
            validation_result["error"],
        )


if __name__ == "__main__":
    main()