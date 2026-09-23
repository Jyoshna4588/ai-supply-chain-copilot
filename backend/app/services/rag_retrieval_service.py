from __future__ import annotations

import json
import logging
import random
import time
from functools import lru_cache
from pathlib import Path
from typing import Any

import vertexai
from google.api_core.exceptions import ResourceExhausted
from google.cloud import aiplatform
from vertexai.language_models import (
    TextEmbeddingInput,
    TextEmbeddingModel,
)

from app.config.settings import settings


logger = logging.getLogger("SupplyChainAI")


class RAGRetrievalService:
    """
    Retrieval service for the Supply Chain Copilot knowledge base.

    Responsibilities:
    1. Load local chunk metadata.
    2. Generate semantic query embeddings.
    3. Query the deployed Vertex AI Vector Search index.
    4. Map nearest-neighbor IDs back to document text.
    """

    def __init__(self) -> None:
        self.project_root = self._get_project_root()

        self.metadata_path = self._resolve_metadata_path(
            settings.rag_metadata_path
        )

        self.metadata_records = self._load_metadata()

        self.metadata_by_id = self._build_metadata_lookup(
            self.metadata_records
        )

        self._embedding_model: TextEmbeddingModel | None = None
        self._index_endpoint = None

        logger.info(
            "RAG retrieval service initialized | "
            "metadata_records=%s | metadata_path=%s",
            len(self.metadata_records),
            self.metadata_path,
        )

    # ============================================================
    # PATHS
    # ============================================================

    @staticmethod
    def _get_project_root() -> Path:
        return Path(__file__).resolve().parents[3]

    def _resolve_metadata_path(
        self,
        configured_path: str,
    ) -> Path:
        path = Path(configured_path)

        if path.is_absolute():
            return path

        return self.project_root / path

    # ============================================================
    # METADATA
    # ============================================================

    def _load_metadata(self) -> list[dict[str, Any]]:
        if not self.metadata_path.exists():
            raise FileNotFoundError(
                "RAG metadata file was not found at: "
                f"{self.metadata_path}"
            )

        try:
            with self.metadata_path.open(
                "r",
                encoding="utf-8",
            ) as file:
                payload = json.load(file)

        except json.JSONDecodeError as exc:
            raise ValueError(
                "RAG metadata.json contains invalid JSON."
            ) from exc

        if isinstance(payload, list):
            records = payload

        elif isinstance(payload, dict):
            records = self._extract_records_from_dict(
                payload
            )

        else:
            raise ValueError(
                "RAG metadata must contain either a JSON "
                "array or a JSON object containing chunk records."
            )

        if not records:
            raise ValueError(
                "RAG metadata file contains no chunk records."
            )

        valid_records = [
            record
            for record in records
            if isinstance(record, dict)
        ]

        if not valid_records:
            raise ValueError(
                "RAG metadata does not contain valid records."
            )

        return valid_records

    @staticmethod
    def _extract_records_from_dict(
        payload: dict[str, Any],
    ) -> list[dict[str, Any]]:
        possible_keys = (
            "chunks",
            "records",
            "documents",
            "metadata",
            "items",
        )

        for key in possible_keys:
            value = payload.get(key)

            if isinstance(value, list):
                return value

        if payload and all(
            isinstance(value, dict)
            for value in payload.values()
        ):
            records: list[dict[str, Any]] = []

            for key, value in payload.items():
                record = dict(value)

                if not any(
                    id_key in record
                    for id_key in (
                        "id",
                        "chunk_id",
                        "vector_id",
                        "datapoint_id",
                    )
                ):
                    record["id"] = key

                records.append(record)

            return records

        return []

    def _build_metadata_lookup(
        self,
        records: list[dict[str, Any]],
    ) -> dict[str, dict[str, Any]]:
        lookup: dict[str, dict[str, Any]] = {}

        for record in records:
            record_id = self._extract_record_id(
                record
            )

            if record_id is None:
                continue

            lookup[str(record_id)] = record

        if not lookup:
            raise ValueError(
                "No vector/chunk IDs could be found in "
                "RAG metadata."
            )

        return lookup

    @staticmethod
    def _extract_record_id(
        record: dict[str, Any],
    ) -> str | None:
        possible_keys = (
            "id",
            "chunk_id",
            "vector_id",
            "datapoint_id",
        )

        for key in possible_keys:
            value = record.get(key)

            if value is not None:
                return str(value)

        return None

    def get_chunk_by_id(
        self,
        chunk_id: str,
    ) -> dict[str, Any] | None:
        return self.metadata_by_id.get(
            str(chunk_id)
        )

    def get_chunks_by_ids(
        self,
        chunk_ids: list[str],
    ) -> list[dict[str, Any]]:
        results: list[dict[str, Any]] = []

        for chunk_id in chunk_ids:
            record = self.get_chunk_by_id(
                chunk_id
            )

            if record is not None:
                results.append(record)

        return results

    # ============================================================
    # QUERY EMBEDDINGS
    # ============================================================

    def _get_embedding_model(
        self,
    ) -> TextEmbeddingModel:
        if self._embedding_model is not None:
            return self._embedding_model

        if not settings.gcp_project_id:
            raise RuntimeError(
                "GCP_PROJECT_ID is not configured."
            )

        if not settings.vertex_region:
            raise RuntimeError(
                "VERTEX_REGION is not configured."
            )

        logger.info(
            "Initializing Vertex AI embedding model | "
            "project=%s | region=%s | model=%s",
            settings.gcp_project_id,
            settings.vertex_region,
            settings.rag_embedding_model,
        )

        vertexai.init(
            project=settings.gcp_project_id,
            location=settings.vertex_region,
        )

        self._embedding_model = (
            TextEmbeddingModel.from_pretrained(
                settings.rag_embedding_model
            )
        )

        return self._embedding_model

    def create_query_embedding(
        self,
        query: str,
    ) -> list[float]:
        cleaned_query = query.strip()

        if not cleaned_query:
            raise ValueError(
                "The RAG retrieval query cannot be empty."
            )

        model = self._get_embedding_model()

        embedding_input = TextEmbeddingInput(
            cleaned_query,
            "RETRIEVAL_QUERY",
        )

        max_retries = 8
        attempt = 0

        while True:
            try:
                result = model.get_embeddings(
                    [embedding_input],
                    output_dimensionality=(
                        settings.rag_embedding_dimension
                    ),
                    auto_truncate=True,
                )

                vector = list(
                    result[0].values
                )

                break

            except ResourceExhausted:
                attempt += 1

                if attempt > max_retries:
                    logger.exception(
                        "Maximum Vertex AI embedding "
                        "quota retries exceeded."
                    )
                    raise

                wait_seconds = min(
                    10 * (2 ** (attempt - 1)),
                    60,
                )

                wait_seconds += random.uniform(
                    0,
                    3,
                )

                logger.warning(
                    "Vertex AI embedding quota reached | "
                    "retry=%s/%s | wait=%.1fs",
                    attempt,
                    max_retries,
                    wait_seconds,
                )

                time.sleep(
                    wait_seconds
                )

        expected_dimension = (
            settings.rag_embedding_dimension
        )

        if len(vector) != expected_dimension:
            raise RuntimeError(
                "Unexpected query embedding dimension. "
                f"Expected {expected_dimension}, "
                f"received {len(vector)}."
            )

        return vector

    def test_query_embedding(
        self,
        query: str,
    ) -> dict[str, Any]:
        vector = self.create_query_embedding(
            query
        )

        return {
            "status": "success",
            "query": query.strip(),
            "embedding_model": (
                settings.rag_embedding_model
            ),
            "task_type": "RETRIEVAL_QUERY",
            "dimension": len(vector),
            "expected_dimension": (
                settings.rag_embedding_dimension
            ),
            "dimension_matches": (
                len(vector)
                == settings.rag_embedding_dimension
            ),
            "vector_preview": vector[:5],
        }

    # ============================================================
    # VECTOR SEARCH
    # ============================================================

    def _get_index_endpoint(self):
        """
        Return the deployed Vertex AI Vector Search endpoint.
        """
        if self._index_endpoint is not None:
            return self._index_endpoint

        if not self.is_vector_search_configured():
            raise RuntimeError(
                "Vertex AI Vector Search is not fully configured."
            )

        aiplatform.init(
            project=settings.gcp_project_id,
            location=settings.vertex_region,
        )

        self._index_endpoint = (
            aiplatform.MatchingEngineIndexEndpoint(
                index_endpoint_name=(
                    settings.rag_index_endpoint_id
                )
            )
        )

        return self._index_endpoint

    def search(
        self,
        query: str,
        top_k: int | None = None,
    ) -> list[dict[str, Any]]:
        """
        Perform semantic search against the deployed
        Vertex AI Vector Search index.
        """
        cleaned_query = query.strip()

        if not cleaned_query:
            raise ValueError(
                "The RAG search query cannot be empty."
            )

        neighbor_count = (
            top_k
            if top_k is not None
            else settings.rag_top_k
        )

        if neighbor_count < 1:
            raise ValueError(
                "top_k must be at least 1."
            )

        query_vector = self.create_query_embedding(
            cleaned_query
        )

        endpoint = self._get_index_endpoint()

        logger.info(
            "Querying Vertex AI Vector Search | "
            "deployed_index=%s | top_k=%s",
            settings.rag_deployed_index_id,
            neighbor_count,
        )

        response = endpoint.find_neighbors(
            deployed_index_id=(
                settings.rag_deployed_index_id
            ),
            queries=[query_vector],
            num_neighbors=neighbor_count,
        )

        if not response:
            return []

        neighbors = response[0]

        results: list[dict[str, Any]] = []

        for rank, neighbor in enumerate(
            neighbors,
            start=1,
        ):
            neighbor_id = str(
                neighbor.id
            )

            metadata = self.get_chunk_by_id(
                neighbor_id
            )

            if metadata is None:
                logger.warning(
                    "Vector Search returned unknown "
                    "chunk ID: %s",
                    neighbor_id,
                )
                continue

            result = {
                "rank": rank,
                "id": neighbor_id,
                "distance": float(
                    neighbor.distance
                ),
                "text": metadata.get(
                    "text",
                    "",
                ),
                "source": metadata.get(
                    "source",
                    "unknown",
                ),
                "page": metadata.get(
                    "page"
                ),
                "chunk_number": metadata.get(
                    "chunk_number"
                ),
            }

            results.append(
                result
            )

        logger.info(
            "RAG semantic search completed | "
            "query=%s | results=%s",
            cleaned_query,
            len(results),
        )

        return results

    def test_search(
        self,
        query: str,
        top_k: int = 5,
    ) -> dict[str, Any]:
        """
        Diagnostic helper for testing semantic retrieval
        before connecting retrieval to LangChain.
        """
        results = self.search(
            query=query,
            top_k=top_k,
        )

        return {
            "status": (
                "success"
                if results
                else "no_results"
            ),
            "query": query.strip(),
            "result_count": len(results),
            "results": results,
        }

    # ============================================================
    # CONFIGURATION / DIAGNOSTICS
    # ============================================================

    @staticmethod
    def is_vector_search_configured() -> bool:
        return bool(
            settings.gcp_project_id
            and settings.vertex_region
            and settings.rag_index_endpoint_id
            and settings.rag_deployed_index_id
        )

    @staticmethod
    def _extract_source_name(
        record: dict[str, Any],
    ) -> str | None:
        possible_keys = (
            "source",
            "source_file",
            "filename",
            "file_name",
            "document",
            "document_name",
        )

        for key in possible_keys:
            value = record.get(key)

            if value:
                return str(value)

        nested_metadata = record.get(
            "metadata"
        )

        if isinstance(
            nested_metadata,
            dict,
        ):
            for key in possible_keys:
                value = nested_metadata.get(
                    key
                )

                if value:
                    return str(value)

        return None

    def get_metadata_summary(
        self,
    ) -> dict[str, Any]:
        source_documents: set[str] = set()

        for record in self.metadata_records:
            source = self._extract_source_name(
                record
            )

            if source:
                source_documents.add(
                    source
                )

        return {
            "status": "ready",
            "metadata_path": str(
                self.metadata_path
            ),
            "chunk_count": len(
                self.metadata_records
            ),
            "indexed_chunk_count": len(
                self.metadata_by_id
            ),
            "source_document_count": len(
                source_documents
            ),
            "source_documents": sorted(
                source_documents
            ),
            "embedding_model": (
                settings.rag_embedding_model
            ),
            "embedding_dimension": (
                settings.rag_embedding_dimension
            ),
            "vector_search_configured": (
                self.is_vector_search_configured()
            ),
        }


@lru_cache(maxsize=1)
def get_rag_retrieval_service() -> RAGRetrievalService:
    """
    Return one shared RAG retrieval service instance.
    """
    return RAGRetrievalService()