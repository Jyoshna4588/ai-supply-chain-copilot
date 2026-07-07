from fastapi import APIRouter

from app.services.purchase_order_service import (
    get_all_purchase_orders,
    get_delayed_purchase_orders,
    get_open_purchase_orders,
)


router = APIRouter(
    prefix="/purchase-orders",
    tags=["Purchase Orders"],
)


@router.get("")
def purchase_orders(limit: int = 20):
    return get_all_purchase_orders(limit=limit)


@router.get("/delayed")
def delayed_purchase_orders(limit: int = 20):
    return get_delayed_purchase_orders(limit=limit)


@router.get("/open")
def open_purchase_orders(limit: int = 20):
    return get_open_purchase_orders(limit=limit)