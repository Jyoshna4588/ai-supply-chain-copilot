from google.cloud import bigquery

from app.config.settings import settings


class InventoryBigQueryRepository:
    def __init__(self):
        self.client = bigquery.Client(project=settings.gcp_project_id)
        self.dataset_id = f"{settings.gcp_project_id}.{settings.bigquery_dataset}"

    def get_low_stock_inventory(self, limit: int = 20):
        query = f"""
            SELECT
                i.product_id,
                p.product_name,
                p.category,
                p.brand,
                i.warehouse_id,
                i.available_stock,
                i.safety_stock,
                i.reorder_point,
                i.inventory_status
            FROM `{self.dataset_id}.inventory` i
            LEFT JOIN `{self.dataset_id}.products` p
                ON i.product_id = p.product_id
            WHERE i.available_stock < i.safety_stock
            LIMIT {limit}
        """

        query_job = self.client.query(query)
        results = query_job.result()

        return [dict(row) for row in results]

    def get_low_stock_count(self):
        query = f"""
            SELECT COUNT(*) AS total_count
            FROM `{self.dataset_id}.inventory`
            WHERE available_stock < safety_stock
        """

        query_job = self.client.query(query)
        results = query_job.result()

        for row in results:
            return row["total_count"]

        return 0