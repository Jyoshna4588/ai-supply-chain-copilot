from app.repositories.supplier_repository import SupplierRepository


def get_all_suppliers(limit: int = 20):
    suppliers_df = SupplierRepository.get_suppliers()

    return {
        "count": len(suppliers_df),
        "items": suppliers_df.head(limit).to_dict(orient="records"),
    }


def get_supplier_performance(limit: int = 20):
    performance_df = SupplierRepository.get_supplier_performance()

    sorted_df = performance_df.sort_values(
        by="delay_rate",
        ascending=False
    )

    return {
        "count": len(performance_df),
        "items": sorted_df.head(limit).to_dict(orient="records"),
    }


def get_delayed_suppliers(limit: int = 10):
    performance_df = SupplierRepository.get_supplier_performance()

    delayed_df = performance_df[
        performance_df["risk_profile"] == "Delayed"
    ].sort_values(
        by="delay_rate",
        ascending=False
    )

    return {
        "count": len(delayed_df),
        "items": delayed_df.head(limit).to_dict(orient="records"),
    }