import pandas as pd

from app.repositories.purchase_order_repository import PurchaseOrderRepository


def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    return df.replace([float("inf"), float("-inf")], "").fillna("")


def get_all_purchase_orders(limit: int = 20):
    po_df = PurchaseOrderRepository.get_purchase_orders()
    po_df = clean_dataframe(po_df)

    return {
        "count": len(po_df),
        "items": po_df.head(limit).to_dict(orient="records"),
    }


def get_delayed_purchase_orders(limit: int = 20):
    po_df = PurchaseOrderRepository.get_purchase_orders()
    suppliers_df = PurchaseOrderRepository.get_suppliers()
    products_df = PurchaseOrderRepository.get_products()

    delayed_df = po_df[po_df["status"] == "Delayed"]

    enriched_df = delayed_df.merge(
        suppliers_df[["supplier_id", "supplier_name", "risk_profile"]],
        on="supplier_id",
        how="left",
    ).merge(
        products_df[["product_id", "product_name", "category"]],
        on="product_id",
        how="left",
    )

    result = enriched_df[
        [
            "po_number",
            "supplier_id",
            "supplier_name",
            "risk_profile",
            "product_id",
            "product_name",
            "category",
            "quantity",
            "order_value",
            "order_date",
            "expected_delivery_date",
            "actual_delivery_date",
            "status",
            "delay_reason",
        ]
    ].head(limit)

    result = clean_dataframe(result)

    return {
        "count": len(delayed_df),
        "items": result.to_dict(orient="records"),
    }


def get_open_purchase_orders(limit: int = 20):
    po_df = PurchaseOrderRepository.get_purchase_orders()

    open_df = po_df[po_df["status"] == "Open"]
    open_df = clean_dataframe(open_df)

    return {
        "count": len(open_df),
        "items": open_df.head(limit).to_dict(orient="records"),
    }