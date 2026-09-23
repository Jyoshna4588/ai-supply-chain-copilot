from pathlib import Path

from google.cloud import bigquery


PROJECT_ID = "copper-freedom-474022-f3"
DATASET_ID = "supply_chain_erp"

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR.parent / "data"


CSV_TABLES = {
    "demand_forecast": "demand_forecast.csv",
    "inventory": "inventory.csv",
    "products": "products.csv",
    "purchase_orders": "purchase_orders.csv",
    "returns": "returns.csv",
    "sales_orders": "sales_orders.csv",
    "shipments": "shipments.csv",
    "supplier_performance": "supplier_performance.csv",
    "suppliers": "suppliers.csv",
    "warehouses": "warehouses.csv",
}


def validate_files() -> None:
    """
    Make sure every required CSV exists before uploading anything.
    """
    print("\nChecking CSV files...\n")

    missing_files = []

    for table_name, filename in CSV_TABLES.items():
        file_path = DATA_DIR / filename

        if file_path.exists():
            print(
                f"[OK] {table_name:<25} -> {filename}"
            )
        else:
            print(
                f"[MISSING] {table_name:<20} -> {filename}"
            )

            missing_files.append(filename)

    if missing_files:
        raise FileNotFoundError(
            "Missing required CSV files: "
            + ", ".join(missing_files)
        )


def get_bigquery_client() -> bigquery.Client:
    """
    Create the BigQuery client using the Google credentials
    already configured on this computer.
    """
    return bigquery.Client(
        project=PROJECT_ID
    )


def ensure_dataset_exists(
    client: bigquery.Client,
) -> None:
    """
    Ensure that the target dataset exists.

    The dataset already exists in this project, but this check makes
    the loader safer if it is run again later.
    """
    dataset_reference = (
        f"{PROJECT_ID}.{DATASET_ID}"
    )

    try:
        dataset = client.get_dataset(
            dataset_reference
        )

        print(
            f"\nDataset found: {dataset_reference}"
        )

        print(
            f"Dataset location: {dataset.location}"
        )

    except Exception as exc:
        raise RuntimeError(
            f"Unable to access dataset "
            f"{dataset_reference}."
        ) from exc


def upload_csv(
    client: bigquery.Client,
    table_name: str,
    filename: str,
) -> None:
    """
    Upload one CSV file into one BigQuery table.

    WRITE_TRUNCATE makes the script safe to rerun:
    an existing table is replaced rather than duplicated.
    """
    file_path = DATA_DIR / filename

    table_id = (
        f"{PROJECT_ID}."
        f"{DATASET_ID}."
        f"{table_name}"
    )

    print("\n----------------------------------------")
    print(f"Loading table: {table_name}")
    print(f"Source file:   {file_path}")
    print(f"Destination:   {table_id}")

    job_config = bigquery.LoadJobConfig(
        source_format=(
            bigquery.SourceFormat.CSV
        ),
        skip_leading_rows=1,
        autodetect=True,
        write_disposition=(
            bigquery.WriteDisposition.WRITE_TRUNCATE
        ),
    )

    with file_path.open("rb") as source_file:
        load_job = client.load_table_from_file(
            source_file,
            table_id,
            job_config=job_config,
        )

        load_job.result()

    table = client.get_table(
        table_id
    )

    print(
        f"[SUCCESS] {table_name}"
    )

    print(
        f"Rows loaded: {table.num_rows}"
    )

    print(
        f"Columns: {len(table.schema)}"
    )


def verify_tables(
    client: bigquery.Client,
) -> None:
    """
    Verify that all expected tables now exist.
    """
    print(
        "\n\n========================================"
    )

    print(
        "VERIFYING BIGQUERY TABLES"
    )

    print(
        "========================================\n"
    )

    existing_tables = {
        table.table_id
        for table in client.list_tables(
            f"{PROJECT_ID}.{DATASET_ID}"
        )
    }

    missing_tables = []

    for table_name in CSV_TABLES:
        if table_name in existing_tables:
            print(
                f"[OK] {table_name}"
            )
        else:
            print(
                f"[MISSING] {table_name}"
            )

            missing_tables.append(
                table_name
            )

    if missing_tables:
        raise RuntimeError(
            "Some tables were not created: "
            + ", ".join(missing_tables)
        )


def main() -> None:
    print(
        "\n========================================"
    )

    print(
        "SUPPLY CHAIN BIGQUERY DATA LOADER"
    )

    print(
        "========================================"
    )

    print(
        f"\nProject: {PROJECT_ID}"
    )

    print(
        f"Dataset: {DATASET_ID}"
    )

    print(
        f"Data directory: {DATA_DIR}"
    )

    validate_files()

    client = get_bigquery_client()

    ensure_dataset_exists(
        client
    )

    for table_name, filename in CSV_TABLES.items():
        upload_csv(
            client=client,
            table_name=table_name,
            filename=filename,
        )

    verify_tables(
        client
    )

    print(
        "\n========================================"
    )

    print(
        "ALL TABLES LOADED SUCCESSFULLY"
    )

    print(
        "========================================\n"
    )


if __name__ == "__main__":
    main()