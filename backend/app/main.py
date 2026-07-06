from fastapi import FastAPI

from app.api import inventory

app = FastAPI(
    title="AI-Powered Supply Chain Copilot",
    description="Backend API for Supply Chain AI Project",
    version="1.0.0",
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