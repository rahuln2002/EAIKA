from app.rag.vectorstore.vectorstore_manager import (
    VectorStoreManager,
)
from app.services.embeddings.embedding_manager import (
    EmbeddingManager,
)


class DenseRetriever:
    """
    Semantic dense retriever.
    """

    def __init__(
        self,
        provider: str = "qdrant",
    ) -> None:
        self.vectorstore = VectorStoreManager(provider=provider)

    def retrieve(
        self,
        query: str,
        top_k: int = 5,
    ):
        """
        Perform semantic retrieval.
        """

        query_embedding = EmbeddingManager.embed_text(query)

        results = self.vectorstore.search(
            query_embedding,
            top_k=top_k,
        )

        return results
