from api.router import api_router
from core.logging import configure_logging
from fastapi import FastAPI

configure_logging()

app = FastAPI()

app.include_router(
    api_router,
    prefix="/api/v1",
)