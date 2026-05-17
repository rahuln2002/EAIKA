from fastapi import APIRouter

from app.services.retrieval.retrieval_service import (
    RetrievalService,
)

router = APIRouter(
    prefix="/search",
    tags=["Search"],
)

documents = []


@router.post("/")
async def search(
    query: str,
):
    """
    Semantic search endpoint.
    """

    if not documents:
        return {"message": "No documents indexed yet."}

    retrieval_service = RetrievalService(documents)

    results = retrieval_service.retrieve_context(query)

    return results
