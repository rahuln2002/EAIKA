from fastapi import APIRouter

from app.monitoring.healthcheck import (
    healthcheck,
)

router = APIRouter(
    prefix="/health",
    tags=["Health"],
)


@router.get("/")
async def health():
    """
    Healthcheck endpoint.
    """

    return await healthcheck()
