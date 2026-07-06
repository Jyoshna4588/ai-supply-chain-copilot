from fastapi import APIRouter

from app.services.inventory_service import get_low_stock_inventory

router = APIRouter(
    prefix="/inventory",
    tags=["Inventory"],
)


@router.get("/low-stock")
def low_stock_inventory(limit: int = 20):
    return get_low_stock_inventory(limit=limit)