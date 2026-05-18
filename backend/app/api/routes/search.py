from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from app.api.dependencies.auth import (
    get_current_user,
)
from app.api.dependencies.database import (
    get_db,
)
from app.services.retrieval.retrieval_service import (
    RetrievalService,
)

router = APIRouter(
    prefix="/search",
    tags=["Search"],
)

retrieval_service = RetrievalService()


@router.post("/")
async def search(
    query: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    Production semantic search endpoint.
    """

    results = retrieval_service.retrieve_context(
        db=db,
        query=query,
    )

    return {
        "query": query,
        "results": results,
        "retrieval_strategy": ("dense+rereank"),
    }
