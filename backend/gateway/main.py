import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from backend.core.config import settings
from backend.core.logger import logger
from backend.database.session import init_db
from backend.gateway.health import router as health_router
from backend.identity.router import router as identity_router
from backend.gateway.middleware import RequestTimingMiddleware

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    description="Production 3D Racing Game & Competitive Esports Platform API Gateway",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Middleware
app.add_middleware(RequestTimingMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(health_router)
app.include_router(identity_router, prefix=settings.API_V1_PREFIX)


@app.on_event("startup")
async def on_startup():
    logger.info(f"Starting {settings.PROJECT_NAME} v{settings.PROJECT_VERSION} in {settings.ENVIRONMENT} mode...")
    await init_db()
    logger.info("Velocity Nexus API Gateway ready.")


@app.on_event("shutdown")
async def on_shutdown():
    logger.info("Shutting down Velocity Nexus API Gateway...")
