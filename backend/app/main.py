from fastapi import FastAPI

# Create the FastAPI application
app = FastAPI(
    title="AI-Powered Supply Chain Copilot",
    description="Backend API for Supply Chain AI Project",
    version="1.0.0"
)

# Home API
@app.get("/")
def home():
    return {
        "message": "Welcome to AI-Powered Supply Chain Copilot 🚀"
    }

# Health Check API
@app.get("/health")
def health():
    return {
        "status": "healthy",
        "application": "Supply Chain AI"
    }