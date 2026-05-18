from sqlalchemy.orm import Session

from app.db.models.chunk import Chunk
from app.rag.retrievers.dense_retriever import (
    DenseRetriever,
)


class RetrievalService:
    """
    Production retrieval service.
    """

    def __init__(
        self,
        provider: str = "qdrant",
    ) -> None:
        self.retriever = DenseRetriever(provider=provider)

    def retrieve_context(
        self,
        db: Session,
        query: str,
        top_k: int = 5,
    ) -> list[str]:
        """
        Retrieve relevant chunks.
        """

        retrieval_results = self.retriever.retrieve(
            query=query,
            top_k=top_k,
        )

        chunk_texts = []

        for result in retrieval_results:
            payload = getattr(
                result,
                "payload",
                {},
            )

            chunk_id = payload.get("chunk_id")

            if not chunk_id:
                continue

            chunk = db.query(Chunk).filter(Chunk.id == chunk_id).first()

            if chunk:
                chunk_texts.append(chunk.content)

        return chunk_texts
