import logging
import time
from typing import Any

from google.cloud import bigquery

from app.config.settings import settings


logger = logging.getLogger("SupplyChainAI")


class BigQueryAIService:
    """
    Executes read-only BigQuery queries and returns JSON-compatible rows.

    Timing logs are included temporarily so we can identify where
    backend latency is occurring.
    """

    def __init__(self):
        client_start = time.perf_counter()

        self.client = bigquery.Client(
            project=settings.gcp_project_id
        )

        client_duration = time.perf_counter() - client_start

        logger.info(
            "BigQuery client initialized | time_ms=%.2f",
            client_duration * 1000,
        )

    def execute_query(
        self,
        query: str,
    ) -> list[dict[str, Any]]:
        """
        Execute a BigQuery SQL statement and return rows as dictionaries.

        Args:
            query:
                The approved GoogleSQL query to execute.

        Returns:
            Query rows converted into dictionaries.
        """

        total_start = time.perf_counter()

        logger.info(
            "BigQuery query started"
        )

        submission_start = time.perf_counter()

        query_job = self.client.query(
            query=query
        )

        submission_duration = (
            time.perf_counter() - submission_start
        )

        logger.info(
            "BigQuery query submitted | "
            "job_id=%s | submission_ms=%.2f",
            query_job.job_id,
            submission_duration * 1000,
        )

        result_wait_start = time.perf_counter()

        results = query_job.result()

        result_wait_duration = (
            time.perf_counter() - result_wait_start
        )

        logger.info(
            "BigQuery results received | "
            "job_id=%s | wait_ms=%.2f | "
            "bytes_processed=%s | cache_hit=%s",
            query_job.job_id,
            result_wait_duration * 1000,
            query_job.total_bytes_processed,
            query_job.cache_hit,
        )

        conversion_start = time.perf_counter()

        rows = [
            dict(row)
            for row in results
        ]

        conversion_duration = (
            time.perf_counter() - conversion_start
        )

        total_duration = (
            time.perf_counter() - total_start
        )

        logger.info(
            "BigQuery query completed | "
            "job_id=%s | rows=%s | "
            "conversion_ms=%.2f | total_ms=%.2f",
            query_job.job_id,
            len(rows),
            conversion_duration * 1000,
            total_duration * 1000,
        )

        return rows