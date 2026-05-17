from fastapi import APIRouter

router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"],
)


@router.get("/")
async def analytics():
    """
    Analytics endpoint.
    """

    return {
        "total_documents": 0,
        "total_queries": 0,
        "system_status": "healthy",
    }
