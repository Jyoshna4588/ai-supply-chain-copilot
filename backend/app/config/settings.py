from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
ENV_FILE = BASE_DIR / ".env"


class Settings(BaseSettings):
    app_name: str = "AI-Powered Supply Chain Copilot"
    app_version: str = "1.0.0"
    environment: str = "development"

    # Data source
    data_source: str = "csv"
    data_dir: str = "data"

    # Google Cloud / BigQuery
    gcp_project_id: str = ""
    bigquery_dataset: str = "supply_chain_erp"

    # Vertex AI / Gemini
    vertex_region: str = "us-central1"
    gemini_model: str = "gemini-2.5-flash"

    # RAG / Vertex AI Vector Search
    rag_embedding_model: str = "gemini-embedding-001"
    rag_embedding_dimension: int = 768

    rag_index_id: str = ""
    rag_index_endpoint_id: str = ""
    rag_deployed_index_id: str = ""

    rag_top_k: int = 5

    # Local RAG metadata generated during ingestion
    rag_metadata_path: str = "backend/rag_output/metadata.json"

    # Cloud Storage
    rag_gcs_bucket: str = ""

    # Logging
    log_level: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()