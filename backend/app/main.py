from fastapi import FastAPI

from app.api import inventory

from app.config.settings import settings

from app.api import supplier

from app.api import purchase_order

from app.core.middleware import RequestLoggingMiddleware

from app.core.exceptions import global_exception_handler

app = FastAPI(
    title=settings.app_name,
    description="Backend API for Supply Chain AI Project",
    version=settings.app_version,
)

app.add_middleware(RequestLoggingMiddleware)

app.add_exception_handler(Exception, global_exception_handler)

app.include_router(inventory.router)

app.include_router(supplier.router)

app.include_router(purchase_order.router)


@app.get("/")
def home():
    return {
        "message": "Welcome to AI-Powered Supply Chain Copilot 🚀"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "application": "Supply Chain AI"
    }