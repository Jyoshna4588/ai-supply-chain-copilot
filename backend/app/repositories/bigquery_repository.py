from google.cloud import bigquery

from app.config.settings import settings


class BigQueryRepository:
    def __init__(self):
        self.client = bigquery.Client(project=settings.gcp_project_id)
        self.dataset_id = f"{settings.gcp_project_id}.{settings.bigquery_dataset}"

    def load_csv_to_table(self, csv_path, table_name: str):
        table_id = f"{self.dataset_id}.{table_name}"

        job_config = bigquery.LoadJobConfig(
            source_format=bigquery.SourceFormat.CSV,
            skip_leading_rows=1,
            autodetect=True,
            write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
        )

        with open(csv_path, "rb") as file:
            load_job = self.client.load_table_from_file(
                file,
                table_id,
                job_config=job_config,
            )

        load_job.result()

        table = self.client.get_table(table_id)

        return {
            "table_id": table_id,
            "rows": table.num_rows,
        }