from sqlalchemy.orm import Session

from app.db.models.chunk import Chunk
from app.rag.retrievers.dense_retriever import (
    DenseRetriever,
)

from app.services.reranking.reranker_service import (
    RerankerService,
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
        retrieval_k: int = 20,
    ) -> list[str]:
        """
        Retrieve relevant chunks.
        """

        retrieval_results = self.retriever.retrieve(
            query=query,
            top_k=retrieval_k,
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

            # =============================================
            # RERANK RESULTS
            # =============================================

            reranked_chunks = RerankerService.rerank(
                query=query,
                documents=chunk_texts,
                top_k=top_k,
            )

            return reranked_chunks

        return chunk_texts
