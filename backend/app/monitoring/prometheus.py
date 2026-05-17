from fastapi import APIRouter
from fastapi.responses import PlainTextResponse
from prometheus_client import generate_latest

router = APIRouter()


@router.get("/metrics")
async def metrics():
    """
    Expose Prometheus metrics.
    """

    data = generate_latest()

    return PlainTextResponse(
        content=data.decode("utf-8"),
        media_type="text/plain",
    )
