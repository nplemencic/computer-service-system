import app.models

from fastapi import FastAPI

from app.core.config import Settings, settings
from app.routers.health import router as health_router

from app.routers.auth import router as auth_router



def create_app(config: Settings = settings) -> FastAPI:
    """
    Kreira i konfigurira FastAPI aplikaciju.
    """
    app = FastAPI(
        title=config.APP_NAME,
        debug=config.ENV == "dev",
    )

    app.include_router(
        health_router,
        prefix="/health",
        tags=["health"],
    )

    app.include_router(
        auth_router,
        prefix="/auth",
        tags=["auth"],
    )

    return app


app = create_app()