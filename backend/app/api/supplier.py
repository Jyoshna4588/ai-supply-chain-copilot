from fastapi import APIRouter

from app.services.supplier_service import (
    get_all_suppliers,
    get_supplier_performance,
    get_delayed_suppliers,
)


router = APIRouter(
    prefix="/suppliers",
    tags=["Suppliers"],
)


@router.get("")
def suppliers(limit: int = 20):
    return get_all_suppliers(limit=limit)


@router.get("/performance")
def supplier_performance(limit: int = 20):
    return get_supplier_performance(limit=limit)


@router.get("/delayed")
def delayed_suppliers(limit: int = 10):
    return get_delayed_suppliers(limit=limit)