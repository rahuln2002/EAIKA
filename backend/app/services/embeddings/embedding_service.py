from sentence_transformers import (
    SentenceTransformer,
)

from app.core.config.settings import (
    settings,
)

# =========================================================
# LOAD EMBEDDING MODEL
# =========================================================

embedding_model = SentenceTransformer(settings.EMBEDDING_MODEL)


class EmbeddingService:
    """
    Embedding generation service.
    """

    @staticmethod
    def generate_embedding(
        text: str,
    ) -> list[float]:
        """
        Generate embedding for text.
        """

        embedding = embedding_model.encode(
            text,
            normalize_embeddings=True,
        )

        return embedding.tolist()

    @staticmethod
    def generate_embeddings(
        texts: list[str],
    ) -> list[list[float]]:
        """
        Generate embeddings for multiple texts.
        """

        embeddings = embedding_model.encode(
            texts,
            normalize_embeddings=True,
        )

        return embeddings.tolist()
