import app.models
from fastapi import FastAPI
from app.core.config import Settings, settings
from app.routers.health import router as health_router
from app.routers.auth import router as auth_router
from app.routers.devices import (
    router as devices_router
)

from app.routers.service_requests import (
    router as service_requests_router
)


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

    app.include_router(
        devices_router,
        prefix="/devices",
        tags=["devices"],
    )

    app.include_router(
        service_requests_router,
        prefix="/service-requests",
        tags=["service-requests"],
    )   

    return app


app = create_app()