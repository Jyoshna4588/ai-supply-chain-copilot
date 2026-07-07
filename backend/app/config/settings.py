from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
ENV_FILE = BASE_DIR / ".env"


class Settings(BaseSettings):
    app_name: str = "AI-Powered Supply Chain Copilot"
    app_version: str = "1.0.0"
    environment: str = "development"

    data_source: str = "csv"
    data_dir: str = "data"

    gcp_project_id: str = ""
    bigquery_dataset: str = "supply_chain_erp"
    vertex_region: str = "us-central1"
    gemini_model: str = "gemini-2.5-flash"

    log_level: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        env_file_encoding="utf-8",
    )


settings = Settings()