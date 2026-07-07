from pathlib import Path

import pandas as pd

from app.config.settings import settings


BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
DATA_DIR = BASE_DIR / settings.data_dir


class PurchaseOrderRepository:

    @staticmethod
    def get_purchase_orders():
        return pd.read_csv(DATA_DIR / "purchase_orders.csv")

    @staticmethod
    def get_suppliers():
        return pd.read_csv(DATA_DIR / "suppliers.csv")

    @staticmethod
    def get_products():
        return pd.read_csv(DATA_DIR / "products.csv")