from pathlib import Path

import pandas as pd

from app.config.settings import settings


BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
DATA_DIR = BASE_DIR / settings.data_dir


class SupplierRepository:

    @staticmethod
    def get_suppliers():
        return pd.read_csv(DATA_DIR / "suppliers.csv")

    @staticmethod
    def get_supplier_performance():
        return pd.read_csv(DATA_DIR / "supplier_performance.csv")