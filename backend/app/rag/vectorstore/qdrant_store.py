from qdrant_client import (
    QdrantClient,
    # models,
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
        Create Qdrant collection.
        """

        try:
            self.client.delete_collection(
                collection_name=self.COLLECTION_NAME,
            )
        except Exception:
            pass

        collections = self.client.get_collections()

        collection_names = [collection.name for collection in collections.collections]

        if self.COLLECTION_NAME not in collection_names:
            self.client.create_collection(
                collection_name=self.COLLECTION_NAME,
                vectors_config=VectorParams(
                    size=self.embedding_dimension,
                    distance=Distance.COSINE,
                ),
            )

    def add_embeddings(
        self,
        embeddings: list[list[float]],
        metadata: list[dict],
    ) -> None:
        """
        Store embeddings in Qdrant.
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
            collection_name=self.COLLECTION_NAME,
            points=points,
        )

    def search(
        self,
        query_embedding: list[float],
        top_k: int = 5,
    ):
        """
        Search vector similarity.
        """

        response = self.client.query_points(
            collection_name=self.COLLECTION_NAME,
            query=query_embedding,
            limit=top_k,
        )

        return response.points
