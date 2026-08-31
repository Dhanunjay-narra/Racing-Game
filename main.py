import os
import sys
import uvicorn
from fastapi.staticfiles import StaticFiles
from backend.gateway.main import app
from backend.core.config import settings
from backend.core.logger import logger
from backend.identity.router import router as identity_router
from backend.economy.router import router as economy_router
from backend.matchmaking.router import router as matchmaking_router

# Include routers
app.include_router(economy_router, prefix=settings.API_V1_PREFIX)
app.include_router(matchmaking_router, prefix=settings.API_V1_PREFIX)

# Mount static files for 3D client
client_dir = os.path.join(os.path.dirname(__file__), "client")
if os.path.exists(client_dir):
    app.mount("/", StaticFiles(directory=client_dir, html=True), name="client")

if __name__ == "__main__":
    logger.info("=" * 60)
    logger.info(f"  {settings.PROJECT_NAME} v{settings.PROJECT_VERSION}")
    logger.info("  High-Performance Authoritative 3D Racing Platform")
    logger.info(f"  Web Client & API: http://localhost:{settings.PORT}")
    logger.info("=" * 60)
    
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=False,
        log_level="info"
    )
