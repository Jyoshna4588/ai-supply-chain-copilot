from functools import lru_cache

from langchain_google_genai import ChatGoogleGenerativeAI

from app.config.settings import settings


@lru_cache(maxsize=1)
def get_llm() -> ChatGoogleGenerativeAI:
    """
    Return one shared Gemini chat model configured for Vertex AI.

    Authentication uses Google Application Default Credentials,
    which is the same credential flow used by the Google Cloud SDK
    and your existing Vertex AI integration.
    """

    if not settings.gcp_project_id:
        raise ValueError(
            "GCP_PROJECT_ID is missing. "
            "Add it to the project's .env file."
        )

    return ChatGoogleGenerativeAI(
        model=settings.gemini_model,
        project=settings.gcp_project_id,
        location=settings.vertex_region,
        vertexai=True,
        temperature=0.2,
        max_output_tokens=2048,
    )