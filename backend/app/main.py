from fastapi import FastAPI

from app.api import inventory

from app.config.settings import settings

app = FastAPI(
    title=settings.app_name,
    description="Backend API for Supply Chain AI Project",
    version=settings.app_version,
)

app.include_router(inventory.router)


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