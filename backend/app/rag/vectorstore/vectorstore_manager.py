from app.rag.vectorstore.faiss_store import (
    FAISSStore,
)
from app.rag.vectorstore.qdrant_store import (
    QdrantStore,
)


class VectorStoreManager:
    """
    Unified vector store manager.
    """

    def __init__(
        self,
        provider: str = "qdrant",
    ) -> None:
        self.provider = provider

        if provider == "faiss":
            self.vectorstore = FAISSStore()

        elif provider == "qdrant":
            self.vectorstore = QdrantStore()

        else:
            raise ValueError(f"Unsupported provider: {provider}")

    def add_embeddings(
        self,
        embeddings: list[list[float]],
        metadata: list[dict],
    ) -> None:
        """
        Add embeddings.
        """

        self.vectorstore.add_embeddings(
            embeddings,
            metadata,
        )

    def search(
        self,
        query_embedding: list[float],
        top_k: int = 5,
    ):
        """
        Search embeddings.
        """

        return self.vectorstore.search(
            query_embedding,
            top_k,
        )
