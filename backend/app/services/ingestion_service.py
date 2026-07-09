from pathlib import Path

from app.config.settings import settings
from app.core.logger import logger
from app.repositories.bigquery_repository import BigQueryRepository


BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
DATA_DIR = BASE_DIR / settings.data_dir


class IngestionService:
    def __init__(self):
        self.bigquery_repository = BigQueryRepository()

    def load_all_csv_files(self):
        csv_files = list(DATA_DIR.glob("*.csv"))

        results = []

        for csv_file in csv_files:
            table_name = csv_file.stem

            logger.info(f"Uploading {csv_file.name} to BigQuery table {table_name}")

            result = self.bigquery_repository.load_csv_to_table(
                csv_path=csv_file,
                table_name=table_name,
            )

            logger.info(f"Uploaded {result['rows']} rows to {result['table_id']}")

            results.append(result)

        return results