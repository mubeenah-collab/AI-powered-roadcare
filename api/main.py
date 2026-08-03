from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config.settings import settings
from api.router import router

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Production-Grade AI Powered Intelligent Road Damage Detection & Monitoring System API"
)

# Configure CORS Middleware for React Frontend & Mobile App Integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API Router
app.include_router(router, prefix=settings.API_PREFIX)

@app.get("/health")
async def health_check():
    """Service health monitoring endpoint."""
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "yolo_model": settings.YOLO_MODEL_PATH,
        "depth_estimation": settings.ENABLE_DEPTH_ESTIMATION
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api.main:app", host="0.0.0.0", port=8000, reload=True)
