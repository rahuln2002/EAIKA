from fastapi import APIRouter
from fastapi import Depends

from app.api.dependencies.auth import (
    get_current_user,
)
from app.rag.pipelines.rag_pipeline import (
    RAGPipeline,
)

router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)

documents = []

rag_pipeline = RAGPipeline(documents)


@router.post("/")
async def chat(
    query: str,
    current_user=Depends(get_current_user),
):
    """
    Protected RAG chat endpoint.
    """

    response = rag_pipeline.run(
        query=query,
    )

    return {
        "user": current_user,
        "response": response,
    }
