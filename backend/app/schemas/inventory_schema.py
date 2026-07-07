from typing import List

from pydantic import BaseModel


class InventoryItem(BaseModel):
    product_id: str
    product_name: str
    category: str
    brand: str
    warehouse_id: str
    available_stock: int
    safety_stock: int
    reorder_point: int
    inventory_status: str


class InventoryResponse(BaseModel):
    count: int
    items: List[InventoryItem]