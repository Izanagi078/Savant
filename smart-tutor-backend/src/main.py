# src/main.py
from fastapi import FastAPI
from src.api.routes.contentRoutes import router as content_router

# Create FastAPI app instance
app = FastAPI(title="Smart Tutor Content API")

# Register the content routes
app.include_router(content_router)

# Health check endpoint
@app.get("/health")
def health():
    return {"status": "ok"}
