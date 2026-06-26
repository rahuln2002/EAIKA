import hashlib

from sqlalchemy.orm import Session

from app.cache.cache_manager import CacheManager
from app.core.constants.cache_constants import (
    RAG_PREFIX,
    RAG_TTL,
)
from app.db.models.chunk import Chunk
from app.db.models.document import Document

from app.rag.retrievers.hybrid_retriever import (
    HybridRetriever,
)


class RetrievalService:
    """
    Production retrieval service with Redis caching.
    """

    def retrieve_context(
        self,
        db: Session,
        query: str,
        user_id: int,
        top_k: int = 5,
        retrieval_k: int = 20,
    ) -> list[str]:
        """
        Retrieve relevant chunks.
        """

        cache_key = (
            f"{RAG_PREFIX}:{user_id}:{hashlib.sha256(query.encode()).hexdigest()}"
        )

        cached = CacheManager.get(
            cache_key,
        )

        if cached is not None:
            return cached

        # =============================================
        # LOAD USER DOCUMENTS
        # =============================================

        documents = self.get_user_chunk_texts(
            db=db,
            user_id=user_id,
        )

        # =============================================
        # HYBRID RETRIEVAL
        # =============================================

        hybrid_retriever = HybridRetriever(
            documents=documents,
        )

        retrieved_chunks = hybrid_retriever.retrieve(
            query=query,
            top_k=retrieval_k,
        )

        # =============================================
        # OPTIONAL RERANKING
        # =============================================

        # retrieved_chunks = RerankerService.rerank(...)

        CacheManager.set(
            cache_key,
            retrieved_chunks,
            expire=RAG_TTL,
        )

        return retrieved_chunks

    @staticmethod
    def get_user_chunk_texts(
        db: Session,
        user_id: int,
    ) -> list[str]:
        """
        Retrieve all user-owned chunk texts.
        """

        chunks = (
            db.query(Chunk)
            .join(
                Document,
                Chunk.document_id == Document.id,
            )
            .filter(
                Document.owner_id == user_id,
            )
            .all()
        )

        return [chunk.content for chunk in chunks]
