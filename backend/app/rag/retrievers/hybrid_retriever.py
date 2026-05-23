from app.rag.retrievers.bm25_retriever import (
    BM25Retriever,
)
from app.rag.retrievers.dense_retriever import (
    DenseRetriever,
)


class HybridRetriever:
    """
    Hybrid retrieval system.
    """

    def __init__(
        self,
        documents: list[str],
        provider: str = "qdrant",
    ) -> None:
        self.documents = documents

        self.bm25 = BM25Retriever(documents)

        self.dense = DenseRetriever(provider=provider)

    def retrieve(
        self,
        query: str,
        top_k: int = 10,
    ) -> list[str]:
        """
        Hybrid retrieval.
        """

        # =============================================
        # BM25 RESULTS
        # =============================================

        bm25_results = self.bm25.retrieve(
            query=query,
            top_k=top_k,
        )

        # =============================================
        # DENSE RESULTS
        # =============================================

        dense_results = self.dense.retrieve(
            query=query,
            top_k=top_k,
        )

        # =============================================
        # EXTRACT PAYLOAD TEXTS
        # =============================================

        dense_chunks = []

        for result in dense_results:
            payload = getattr(
                result,
                "payload",
                {},
            )

            content = payload.get("content")

            if content:
                dense_chunks.append(
                    {
                        "chunk_id": payload.get("chunk_id"),
                        "document_id": payload.get("document_id"),
                        "content": content,
                    }
                )

        # =============================================
        # FUSION
        # =============================================

        bm25_chunks = [{"content": text} for text in bm25_results]

        combined = bm25_chunks + dense_chunks

        # =============================================
        # DEDUPLICATION
        # =============================================

        seen = set()

        unique_results = []

        for chunk in combined:
            content = chunk["content"]

            if content not in seen:
                seen.add(content)

                unique_results.append(chunk)

        return unique_results[:top_k]
