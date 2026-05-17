import faiss
import numpy as np


class FAISSStore:
    """
    FAISS vector store.
    """

    def __init__(
        self,
        embedding_dimension: int = 384,
    ) -> None:
        self.embedding_dimension = embedding_dimension

        self.index = faiss.IndexFlatL2(self.embedding_dimension)

        self.metadata = []

    def add_embeddings(
        self,
        embeddings: list[list[float]],
        metadata: list[dict],
    ) -> None:
        """
        Add embeddings to FAISS index.
        """

        vectors = np.array(
            embeddings,
            dtype=np.float32,
        )

        self.index.add(vectors)

        self.metadata.extend(metadata)

    def search(
        self,
        query_embedding: list[float],
        top_k: int = 5,
    ) -> list[dict]:
        """
        Search similar embeddings.
        """

        query_vector = np.array(
            [query_embedding],
            dtype=np.float32,
        )

        distances, indices = self.index.search(
            query_vector,
            top_k,
        )

        results = []

        for score, idx in zip(
            distances[0],
            indices[0],
        ):
            if idx < len(self.metadata):
                results.append(
                    {
                        "score": float(score),
                        "metadata": self.metadata[idx],
                    }
                )

        return results
