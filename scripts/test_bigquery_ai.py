import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
BACKEND_DIR = PROJECT_ROOT / "backend"

sys.path.append(str(BACKEND_DIR))


from app.config.settings import settings
from app.services.bigquery_ai_service import BigQueryAIService


def main():
    service = BigQueryAIService()

    query = f"""
        SELECT
            warehouse_id,
            COUNT(*) AS low_stock_count
        FROM `{settings.gcp_project_id}.{settings.bigquery_dataset}.inventory`
        WHERE available_stock < safety_stock
        GROUP BY warehouse_id
        ORDER BY low_stock_count DESC
        LIMIT 5
    """

    results = service.execute_query(query)

    print("\nTop warehouses by low-stock products:\n")

    for row in results:
        print(row)


if __name__ == "__main__":
    main()