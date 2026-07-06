from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
DATA_DIR = BASE_DIR / "data"


def get_low_stock_inventory(limit: int = 20):
    inventory_df = pd.read_csv(DATA_DIR / "inventory.csv")
    products_df = pd.read_csv(DATA_DIR / "products.csv")

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

    return {
        "count": len(low_stock_df),
        "items": result.to_dict(orient="records"),
    }