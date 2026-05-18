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

        dense_texts = []

        for result in dense_results:
            payload = getattr(
                result,
                "payload",
                {},
            )

            text = payload.get("text")

            if text:
                dense_texts.append(text)

        # =============================================
        # FUSION
        # =============================================

        combined = bm25_results + dense_texts

        # =============================================
        # DEDUPLICATION
        # =============================================

        unique_results = list(dict.fromkeys(combined))

        return unique_results[:top_k]
