from __future__ import annotations

import hashlib
import json
import os
import random
import time
from pathlib import Path

from dotenv import load_dotenv
from google.api_core.exceptions import ResourceExhausted
from google.cloud import storage
import vertexai
from vertexai.language_models import (
    TextEmbeddingInput,
    TextEmbeddingModel,
)
from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter


# ============================================================
# PATHS
# ============================================================

BACKEND_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BACKEND_DIR.parent

DOCUMENTS_DIR = PROJECT_ROOT / "documents"
OUTPUT_DIR = BACKEND_DIR / "rag_output"

# .env is located at the project root:
# C:\Projects\SupplyChainAI\.env
ENV_FILE = PROJECT_ROOT / ".env"


# ============================================================
# LOAD ENVIRONMENT
# ============================================================

load_dotenv(ENV_FILE)

PROJECT_ID = os.getenv("GCP_PROJECT_ID")
REGION = os.getenv("VERTEX_REGION", "us-central1")
GCS_BUCKET = os.getenv("RAG_GCS_BUCKET")

EMBEDDING_MODEL = "gemini-embedding-001"
EMBEDDING_DIMENSION = 768

GCS_VECTOR_PREFIX = "rag/vector_search"
GCS_METADATA_PREFIX = "rag/metadata"


# ============================================================
# VALIDATION
# ============================================================

def validate_configuration() -> None:
    missing = []

    if not PROJECT_ID:
        missing.append("GCP_PROJECT_ID")

    if not GCS_BUCKET:
        missing.append("RAG_GCS_BUCKET")

    if missing:
        raise RuntimeError(
            "Missing required environment variables: "
            + ", ".join(missing)
        )

    if not DOCUMENTS_DIR.exists():
        raise FileNotFoundError(
            f"Documents directory not found: {DOCUMENTS_DIR}"
        )

    pdf_files = list(
        DOCUMENTS_DIR.glob("*.pdf")
    )

    if not pdf_files:
        raise FileNotFoundError(
            f"No PDF documents found in: {DOCUMENTS_DIR}"
        )

    print()
    print("Configuration validated.")
    print(f"Project ID: {PROJECT_ID}")
    print(f"Vertex region: {REGION}")
    print(f"GCS bucket: {GCS_BUCKET}")


# ============================================================
# PDF LOADING
# ============================================================

def load_pdf_documents() -> list[dict]:
    documents = []

    pdf_files = sorted(
        DOCUMENTS_DIR.glob("*.pdf")
    )

    print()
    print("Loading PDF documents...")
    print("-" * 60)

    for pdf_path in pdf_files:
        reader = PdfReader(
            str(pdf_path)
        )

        pages_loaded = 0

        for page_number, page in enumerate(
            reader.pages,
            start=1,
        ):
            text = page.extract_text()

            if not text:
                continue

            cleaned_text = " ".join(
                text.split()
            )

            if not cleaned_text:
                continue

            documents.append(
                {
                    "text": cleaned_text,
                    "source": pdf_path.name,
                    "page": page_number,
                }
            )

            pages_loaded += 1

        print(
            f"[OK] {pdf_path.name} "
            f"({pages_loaded} readable page(s))"
        )

    print("-" * 60)
    print(
        f"Loaded {len(documents)} document page(s)."
    )

    if not documents:
        raise RuntimeError(
            "PDF files were found, but no readable text "
            "could be extracted."
        )

    return documents


# ============================================================
# DOCUMENT CHUNKING
# ============================================================

def create_chunks(
    documents: list[dict],
) -> list[dict]:

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150,
        separators=[
            "\n\n",
            "\n",
            ". ",
            " ",
            "",
        ],
    )

    chunks = []

    print()
    print("Creating semantic-aware chunks...")
    print("-" * 60)

    for document in documents:
        text_chunks = splitter.split_text(
            document["text"]
        )

        for chunk_number, chunk_text in enumerate(
            text_chunks,
            start=1,
        ):
            raw_id = (
                f"{document['source']}|"
                f"{document['page']}|"
                f"{chunk_number}|"
                f"{chunk_text}"
            )

            chunk_id = hashlib.sha256(
                raw_id.encode("utf-8")
            ).hexdigest()[:32]

            chunks.append(
                {
                    "id": chunk_id,
                    "text": chunk_text,
                    "source": document["source"],
                    "page": document["page"],
                    "chunk_number": chunk_number,
                }
            )

    print(
        f"Created {len(chunks)} chunks."
    )

    if not chunks:
        raise RuntimeError(
            "No document chunks were created."
        )

    return chunks


# ============================================================
# VERTEX AI EMBEDDINGS
# ============================================================

def create_embeddings(
    chunks: list[dict],
) -> list[dict]:

    print()
    print("Initializing Vertex AI...")
    print("-" * 60)

    vertexai.init(
        project=PROJECT_ID,
        location=REGION,
    )

    model = TextEmbeddingModel.from_pretrained(
        EMBEDDING_MODEL
    )

    print(f"Project: {PROJECT_ID}")
    print(f"Region: {REGION}")
    print(
        f"Embedding model: {EMBEDDING_MODEL}"
    )
    print(
        f"Embedding dimension: "
        f"{EMBEDDING_DIMENSION}"
    )

    print()
    print("Generating Vertex AI embeddings...")
    print("-" * 60)

    embedded_chunks = []

    total = len(chunks)

    for index, chunk in enumerate(
        chunks,
        start=1,
    ):

        embedding_input = TextEmbeddingInput(
            chunk["text"],
            "RETRIEVAL_DOCUMENT",
        )

        max_retries = 8
        attempt = 0

        while True:
            try:
                result = model.get_embeddings(
                    [embedding_input],
                    output_dimensionality=(
                        EMBEDDING_DIMENSION
                    ),
                    auto_truncate=True,
                )

                vector = result[0].values

                break

            except ResourceExhausted:
                attempt += 1

                if attempt > max_retries:
                    print()
                    print(
                        "[ERROR] Maximum Vertex AI "
                        "quota retries exceeded."
                    )
                    raise

                # Exponential backoff:
                # 10, 20, 40, then max 60 seconds.
                wait_seconds = min(
                    10 * (2 ** (attempt - 1)),
                    60,
                )

                # Add a little randomness so repeated
                # requests don't always hit the same window.
                wait_seconds += random.uniform(
                    0,
                    3,
                )

                print()
                print(
                    "[RATE LIMIT] Vertex AI embedding "
                    "quota reached."
                )

                print(
                    f"Waiting {wait_seconds:.1f} seconds "
                    f"before retry "
                    f"{attempt}/{max_retries}..."
                )

                time.sleep(
                    wait_seconds
                )

        if len(vector) != EMBEDDING_DIMENSION:
            raise RuntimeError(
                "Unexpected embedding dimension for "
                f"{chunk['id']}: "
                f"{len(vector)}"
            )

        embedded_chunk = {
            **chunk,
            "embedding": vector,
        }

        embedded_chunks.append(
            embedded_chunk
        )

        print(
            f"[{index}/{total}] "
            f"Embedded "
            f"{chunk['source']} "
            f"page {chunk['page']} "
            f"chunk {chunk['chunk_number']}"
        )

        # Deliberately slow down requests slightly
        # because this project currently has a
        # relatively small Vertex AI embedding quota.
        #
        # For only 17 chunks this adds very little
        # total runtime and makes ingestion more reliable.
        if index < total:
            time.sleep(2)

    print("-" * 60)

    print(
        f"Generated "
        f"{len(embedded_chunks)} embeddings."
    )

    return embedded_chunks


# ============================================================
# LOCAL OUTPUT
# ============================================================

def save_local_files(
    embedded_chunks: list[dict],
) -> tuple[Path, Path]:

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    vector_file = (
        OUTPUT_DIR / "vectors.jsonl"
    )

    metadata_file = (
        OUTPUT_DIR / "metadata.json"
    )

    print()
    print("Writing local RAG files...")
    print("-" * 60)

    # --------------------------------------------------------
    # Vector Search input file
    # --------------------------------------------------------

    with vector_file.open(
        "w",
        encoding="utf-8",
    ) as file:

        for chunk in embedded_chunks:

            vector_record = {
                "id": chunk["id"],
                "embedding": chunk["embedding"],
            }

            file.write(
                json.dumps(
                    vector_record
                )
                + "\n"
            )

    # --------------------------------------------------------
    # Metadata lookup
    # --------------------------------------------------------

    metadata = {}

    for chunk in embedded_chunks:
        metadata[
            chunk["id"]
        ] = {
            "text": chunk["text"],
            "source": chunk["source"],
            "page": chunk["page"],
            "chunk_number": (
                chunk["chunk_number"]
            ),
        }

    with metadata_file.open(
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            metadata,
            file,
            indent=2,
            ensure_ascii=False,
        )

    print(
        f"[OK] {vector_file}"
    )

    print(
        f"[OK] {metadata_file}"
    )

    return (
        vector_file,
        metadata_file,
    )


# ============================================================
# CLOUD STORAGE UPLOAD
# ============================================================

def upload_to_gcs(
    vector_file: Path,
    metadata_file: Path,
) -> None:

    print()
    print(
        "Uploading RAG files "
        "to Cloud Storage..."
    )
    print("-" * 60)

    client = storage.Client(
        project=PROJECT_ID
    )

    bucket = client.bucket(
        GCS_BUCKET
    )

    if not bucket.exists():
        raise RuntimeError(
            "GCS bucket does not exist: "
            f"{GCS_BUCKET}"
        )

    # --------------------------------------------------------
    # Vector Search source
    # --------------------------------------------------------

    vector_blob_name = (
        f"{GCS_VECTOR_PREFIX}/"
        "vectors.jsonl"
    )

    vector_blob = bucket.blob(
        vector_blob_name
    )

    vector_blob.upload_from_filename(
        str(vector_file),
        content_type="application/json",
    )

    print(
        f"[OK] gs://{GCS_BUCKET}/"
        f"{vector_blob_name}"
    )

    # --------------------------------------------------------
    # Chunk metadata
    # --------------------------------------------------------

    metadata_blob_name = (
        f"{GCS_METADATA_PREFIX}/"
        "metadata.json"
    )

    metadata_blob = bucket.blob(
        metadata_blob_name
    )

    metadata_blob.upload_from_filename(
        str(metadata_file),
        content_type="application/json",
    )

    print(
        f"[OK] gs://{GCS_BUCKET}/"
        f"{metadata_blob_name}"
    )


# ============================================================
# INGESTION SUMMARY
# ============================================================

def print_summary(
    embedded_chunks: list[dict],
) -> None:

    sources = sorted(
        {
            chunk["source"]
            for chunk in embedded_chunks
        }
    )

    print()
    print("=" * 60)

    print(
        "RAG INGESTION COMPLETED SUCCESSFULLY"
    )

    print("=" * 60)

    print(
        f"Documents: {len(sources)}"
    )

    print(
        f"Chunks: "
        f"{len(embedded_chunks)}"
    )

    print(
        f"Embedding model: "
        f"{EMBEDDING_MODEL}"
    )

    print(
        f"Embedding dimension: "
        f"{EMBEDDING_DIMENSION}"
    )

    print()
    print(
        "Vector Search source:"
    )

    print(
        f"gs://{GCS_BUCKET}/"
        f"{GCS_VECTOR_PREFIX}/"
    )

    print()
    print(
        "Metadata source:"
    )

    print(
        f"gs://{GCS_BUCKET}/"
        f"{GCS_METADATA_PREFIX}/"
        "metadata.json"
    )

    print()
    print(
        "Documents indexed:"
    )

    for source in sources:
        print(
            f"  - {source}"
        )

    print()

    print(
        "Next step: create the Vertex AI "
        "Vector Search index."
    )


# ============================================================
# MAIN
# ============================================================

def main() -> None:

    print()
    print("=" * 60)

    print(
        "SUPPLY CHAIN COPILOT - RAG INGESTION"
    )

    print("=" * 60)

    print(
        f"Documents directory: "
        f"{DOCUMENTS_DIR}"
    )

    validate_configuration()

    documents = load_pdf_documents()

    chunks = create_chunks(
        documents
    )

    embedded_chunks = create_embeddings(
        chunks
    )

    (
        vector_file,
        metadata_file,
    ) = save_local_files(
        embedded_chunks
    )

    upload_to_gcs(
        vector_file,
        metadata_file,
    )

    print_summary(
        embedded_chunks
    )


if __name__ == "__main__":
    main()