from fastapi import APIRouter
from backend.core.config import settings

router = APIRouter(tags=["Health & Diagnostics"])


@router.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "version": settings.PROJECT_VERSION,
        "environment": settings.ENVIRONMENT,
        "tick_rate": settings.TICK_RATE
    }


@router.get("/api/v1/ping")
async def ping():
    return {"pong": True}
