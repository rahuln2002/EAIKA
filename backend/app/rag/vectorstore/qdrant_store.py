from qdrant_client import (
    QdrantClient,
)

from qdrant_client.models import (
    Distance,
    PointStruct,
    VectorParams,
)

from app.core.config.settings import (
    settings,
)


class QdrantStore:
    """
    Qdrant vector database manager.
    """

    COLLECTION_NAME = "document_chunks"

    def __init__(
        self,
        embedding_dimension: int = 384,
    ) -> None:

        self.embedding_dimension = embedding_dimension

        self.client = QdrantClient(
            url=settings.QDRANT_URL,
            api_key=(settings.QDRANT_API_KEY if settings.QDRANT_API_KEY else None),
        )

        self._create_collection()

    def _create_collection(
        self,
    ) -> None:
        """
        Create collection if not exists.
        """

        collections = self.client.get_collections()

        collection_names = [collection.name for collection in collections.collections]

        # ============================================
        # CREATE COLLECTION
        # ============================================

        if self.COLLECTION_NAME not in collection_names:
            self.client.create_collection(
                collection_name=(self.COLLECTION_NAME),
                vectors_config=VectorParams(
                    size=(self.embedding_dimension),
                    distance=Distance.COSINE,
                ),
            )

    def add_embeddings(
        self,
        embeddings: list[list[float]],
        metadata: list[dict],
    ) -> None:
        """
        Store embeddings.
        """

        points = []

        for embedding, payload in zip(
            embeddings,
            metadata,
        ):
            points.append(
                PointStruct(
                    id=payload["chunk_id"],
                    vector=embedding,
                    payload=payload,
                )
            )

        self.client.upsert(
            collection_name=(self.COLLECTION_NAME),
            points=points,
        )

    def search(
        self,
        query_embedding: list[float],
        top_k: int = 5,
    ):
        """
        Vector similarity search.
        """

        response = self.client.query_points(
            collection_name=(self.COLLECTION_NAME),
            query=query_embedding,
            limit=top_k,
        )

        return response.points
