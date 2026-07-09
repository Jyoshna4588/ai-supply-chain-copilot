import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
BACKEND_DIR = BASE_DIR / "backend"

sys.path.append(str(BACKEND_DIR))

from app.services.ingestion_service import IngestionService


def main():
    service = IngestionService()
    results = service.load_all_csv_files()

    print("\nBigQuery upload completed successfully!\n")

    for result in results:
        print(f"{result['table_id']} -> {result['rows']} rows")


if __name__ == "__main__":
    main()