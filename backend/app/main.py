from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import ai
from app.api import dashboard
from app.api import inventory
from app.api import purchase_order
from app.api import supplier
from app.config.settings import settings
from app.core.exceptions import global_exception_handler
from app.core.middleware import RequestLoggingMiddleware


app = FastAPI(
    title=settings.app_name,
    description="Backend API for Supply Chain AI Project",
    version=settings.app_version,
)


# ---------------------------------------------------------
# CORS Configuration
# ---------------------------------------------------------
# Allow the local Vite frontend, local Docker frontend,
# and deployed Cloud Run frontend to access this API.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "https://supply-chain-ai-frontend-620610885141.us-central1.run.app",
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------
# Request Logging Middleware
# ---------------------------------------------------------
app.add_middleware(
    RequestLoggingMiddleware
)


# ---------------------------------------------------------
# Global Exception Handler
# ---------------------------------------------------------
app.add_exception_handler(
    Exception,
    global_exception_handler,
)


# ---------------------------------------------------------
# API Routers
# ---------------------------------------------------------
app.include_router(inventory.router)
app.include_router(supplier.router)
app.include_router(purchase_order.router)
app.include_router(ai.router)
app.include_router(dashboard.router)


# ---------------------------------------------------------
# Root Endpoint
# ---------------------------------------------------------
@app.get("/")
def home():
    return {
        "message": "Welcome to AI-Powered Supply Chain Copilot 🚀"
    }


# ---------------------------------------------------------
# Health Check
# ---------------------------------------------------------
@app.get("/health")
def health():
    return {
        "status": "healthy",
        "application": "Supply Chain AI",
    }