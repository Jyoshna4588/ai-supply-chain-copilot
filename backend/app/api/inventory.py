from fastapi import APIRouter

from app.schemas.inventory_schema import InventoryResponse
from app.services.inventory_service import get_low_stock_inventory

router = APIRouter(
    prefix="/inventory",
    tags=["Inventory"],
)


@router.get(
    "/low-stock",
    response_model=InventoryResponse
)
def low_stock_inventory(limit: int = 20):
    return get_low_stock_inventory(limit=limit)