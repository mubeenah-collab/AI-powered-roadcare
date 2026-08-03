import os
import sys
import logging
from pathlib import Path

# Ensure project root directory is present in sys.path so imports like 'from backend...' resolve cleanly
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from backend.config.settings import settings
from backend.api.router import router
from database.connection import engine
from database.models import Base

# Configure System-Wide Production Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("roadvision.backend")

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Production-Grade RoadVision AI Backend API with PostgreSQL + PostGIS Spatial Deduplication & Road Health Scoring",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_db_init():
    """Verifies PostgreSQL connection and initializes ORM tables on startup."""
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("[+] PostgreSQL + PostGIS database connection verified & tables initialized successfully.")
    except Exception as e:
        logger.warning(f"[!] PostgreSQL startup connection warning (running with resilient database layer): {e}")

# Global Exception Handlers for non-HTTP exceptions
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled Exception on {request.url}: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "status": "error",
            "error_type": "InternalServerError",
            "message": "An unexpected error occurred on the server.",
            "path": str(request.url)
        }
    )

app.include_router(router, prefix=settings.API_PREFIX)

@app.get("/", include_in_schema=False)
async def root_redirect():
    """Redirect root endpoint directly to Swagger UI."""
    return RedirectResponse(url="/docs")

@app.get("/health", tags=["Health"])
async def health_check():
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "database": "PostgreSQL + PostGIS (asyncpg)",
        "yolo_model": settings.YOLO_MODEL_PATH
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
