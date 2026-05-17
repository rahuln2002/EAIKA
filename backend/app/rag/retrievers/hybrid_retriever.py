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
        self.dense_retriever = DenseRetriever(provider=provider)

        self.bm25_retriever = BM25Retriever(documents)

    def retrieve(
        self,
        query: str,
        top_k: int = 5,
    ) -> dict:
        """
        Combine dense + BM25 retrieval.
        """

        dense_results = self.dense_retriever.retrieve(
            query,
            top_k=top_k,
        )

        sparse_results = self.bm25_retriever.retrieve(
            query,
            top_k=top_k,
        )

        return {
            "dense_results": dense_results,
            "sparse_results": sparse_results,
        }
