from fastapi import APIRouter

from app.rag.pipelines.rag_pipeline import (
    RAGPipeline,
)

router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)

documents = []


@router.post("/")
async def chat(
    query: str,
):
    """
    RAG chat endpoint.
    """

    if not documents:
        return {"message": "No documents indexed yet."}

    rag_pipeline = RAGPipeline(documents)

    response = rag_pipeline.run(
        query=query,
    )

    return response
