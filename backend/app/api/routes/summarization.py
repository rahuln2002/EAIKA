from fastapi import APIRouter

from app.services.summarization.summarization_service import (
    SummarizationService,
)

router = APIRouter(
    prefix="/summarization",
    tags=["Summarization"],
)


@router.post("/")
async def summarize(
    text: str,
):
    """
    Summarize long text.
    """

    result = SummarizationService.map_reduce_summarize(text=text)

    return result
