from fastapi import APIRouter

from app.services.dashboard_service import DashboardService


router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
)


dashboard_service = DashboardService()


@router.get("/summary")
def get_dashboard_summary():
    """
    Return summary KPIs for the React dashboard.
    """

    return dashboard_service.get_summary()