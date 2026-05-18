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
        "system_status": "healthy",
        "evaluation_enabled": True,
        "metrics": [
            "faithfulness",
            "hallucination",
            "relevancy",
            "retrieval_metrics",
        ],
    }
