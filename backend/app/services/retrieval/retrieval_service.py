from app.rag.retrievers.hybrid_retriever import (
    HybridRetriever,
)


class RetrievalService:
    """
    High-level retrieval service.
    """

    def __init__(
        self,
        documents: list[str],
    ) -> None:
        self.hybrid_retriever = HybridRetriever(documents)

    def retrieve_context(
        self,
        query: str,
        top_k: int = 5,
    ):
        """
        Retrieve relevant context.
        """

        return self.hybrid_retriever.retrieve(
            query=query,
            top_k=top_k,
        )
