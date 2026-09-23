import sys
import time
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
BACKEND_DIR = PROJECT_ROOT / "backend"

sys.path.append(str(BACKEND_DIR))


from app.services.bigquery_schema_service import BigQuerySchemaService


def main():
    schema_service = BigQuerySchemaService()

    print("\nTesting BigQuery schema cache...\n")

    first_start = time.perf_counter()

    first_schema = schema_service.get_schema_context()

    first_duration = time.perf_counter() - first_start

    print(
        "First schema load "
        f"(BigQuery metadata request): {first_duration:.4f} seconds"
    )

    second_start = time.perf_counter()

    second_schema = schema_service.get_schema_context()

    second_duration = time.perf_counter() - second_start

    print(
        "Second schema load "
        f"(cached): {second_duration:.6f} seconds"
    )

    schemas_match = first_schema == second_schema

    print("\nCache verification:")
    print("Schemas match:", schemas_match)
    print("Schema characters:", len(first_schema))

    if not schemas_match:
        print(
            "\nWarning: The cached schema does not match "
            "the original schema."
        )
        return

    if second_duration < first_duration:
        print("\nSchema caching is working successfully.")
    else:
        print(
            "\nThe schemas match, but the timing difference was "
            "not clearly measurable."
        )


if __name__ == "__main__":
    main()