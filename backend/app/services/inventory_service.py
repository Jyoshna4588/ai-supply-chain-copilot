from app.config.settings import settings
from app.core.logger import logger
from app.repositories.inventory_bigquery_repository import InventoryBigQueryRepository
from app.repositories.inventory_repository import InventoryRepository


def get_low_stock_inventory(limit: int = 20):
    logger.info(f"Fetching low-stock inventory using data_source={settings.data_source}")

    if settings.data_source == "bigquery":
        repository = InventoryBigQueryRepository()

        items = repository.get_low_stock_inventory(limit=limit)
        count = repository.get_low_stock_count()

        logger.info(f"Returning {len(items)} low-stock products from BigQuery")

        return {
            "count": count,
            "items": items,
        }

    inventory_df = InventoryRepository.get_inventory()
    products_df = InventoryRepository.get_products()

    merged_df = inventory_df.merge(
        products_df[["product_id", "product_name", "category", "brand"]],
        on="product_id",
        how="left",
    )

    low_stock_df = merged_df[
        merged_df["available_stock"] < merged_df["safety_stock"]
    ]

    result = low_stock_df[
        [
            "product_id",
            "product_name",
            "category",
            "brand",
            "warehouse_id",
            "available_stock",
            "safety_stock",
            "reorder_point",
            "inventory_status",
        ]
    ].head(limit)

    logger.info(f"Returning {len(result)} low-stock products from CSV")

    return {
        "count": len(low_stock_df),
        "items": result.to_dict(orient="records"),
    }