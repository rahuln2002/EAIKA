from sqlalchemy.orm import Session

from app.db.models.chunk import Chunk
from app.rag.retrievers.dense_retriever import (
    DenseRetriever,
)

# from app.services.reranking.reranker_service import (
#     RerankerService,
# )
from app.rag.retrievers.hybrid_retriever import (
    HybridRetriever,
)
from app.db.models.document import (
    Document,
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
        user_id: int,
        top_k: int = 5,
        retrieval_k: int = 20,
    ) -> list[str]:
        """
        Retrieve relevant chunks.
        """

        # =============================================
        # GET DOCUMENT CORPUS
        # =============================================

        documents = self.get_user_chunk_texts(
            db=db,
            user_id=user_id,
        )

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

        # reranked_chunks = RerankerService.rerank(
        #     query=query,
        #     documents=retrieved_chunks,
        #     top_k=top_k,
        # )

        # final_results = []

        # for idx, chunk_text in enumerate(reranked_chunks):
        #     chunk = db.query(Chunk).filter(Chunk.content == chunk_text).first()

        #     if not chunk:
        #         continue

        #     final_results.append(
        #         {
        #             "chunk_id": chunk.id,
        #             "document_id": (chunk.document_id),
        #             "content": chunk.content,
        #             "citation": f"[{idx + 1}]",
        #         }
        #     )

        return retrieved_chunks

    def get_user_chunk_texts(
        self,
        db: Session,
        user_id: int,
    ) -> list[str]:
        """
        Retrieve user-owned chunk texts.
        """

        chunks = (
            db.query(Chunk)
            .join(
                Document,
                Chunk.document_id == Document.id,
            )
            .filter(Document.owner_id == user_id)
            .all()
        )

        return [chunk.content for chunk in chunks]
