from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
DATA_DIR = BASE_DIR / "data"


class InventoryRepository:

    @staticmethod
    def get_inventory():
        """
        Read inventory data from the ERP inventory table.
        """
        return pd.read_csv(DATA_DIR / "inventory.csv")

    @staticmethod
    def get_products():
        """
        Read product master data.
        """
        return pd.read_csv(DATA_DIR / "products.csv")