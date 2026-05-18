from fastapi import APIRouter
from fastapi import Depends

from app.api.dependencies.auth import (
    get_current_user,
)
from app.services.retrieval.retrieval_service import (
    RetrievalService,
)

router = APIRouter(
    prefix="/search",
    tags=["Search"],
)

documents = [
    "RAG improves retrieval systems.",
    "Embeddings power semantic search.",
]

retrieval_service = RetrievalService(documents)


@router.post("/")
async def search(
    query: str,
    current_user=Depends(get_current_user),
):
    """
    Protected semantic search endpoint.
    """

    results = retrieval_service.retrieve_context(query)

    return results
