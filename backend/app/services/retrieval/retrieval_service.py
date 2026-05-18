from sqlalchemy.orm import Session

from app.db.models.chunk import Chunk
from app.rag.retrievers.dense_retriever import (
    DenseRetriever,
)
from app.services.reranking.reranker_service import (
    RerankerService,
)
from app.rag.retrievers.hybrid_retriever import (
    HybridRetriever,
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

        # =============================================
        # GET DOCUMENT CORPUS
        # =============================================

        documents = self.get_all_chunk_texts(db)

        # =============================================
        # HYBRID RETRIEVER
        # =============================================

        hybrid_retriever = HybridRetriever(documents=documents)

        retrieved_chunks = hybrid_retriever.retrieve(
            query=query,
            top_k=retrieval_k,
        )

        # =============================================
        # RERANK RESULTS
        # =============================================

        reranked_chunks = RerankerService.rerank(
            query=query,
            documents=retrieved_chunks,
            top_k=top_k,
        )

        return reranked_chunks

    def get_all_chunk_texts(
        self,
        db: Session,
    ) -> list[str]:
        """
        Retrieve all chunk texts.
        """

        chunks = db.query(Chunk).all()

        return [chunk.content for chunk in chunks]
