from sentence_transformers import (
    SentenceTransformer,
)

from app.core.config.settings import (
    settings,
)

# =========================================================
# GLOBAL MODEL HOLDER
# =========================================================

embedding_model = None


def get_embedding_model():
    """
    Lazy-load embedding model.
    """

    global embedding_model

    if embedding_model is None:
        embedding_model = SentenceTransformer(settings.EMBEDDING_MODEL)

    return embedding_model


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

        model = get_embedding_model()

        embedding = model.encode(
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

        model = get_embedding_model()

        embeddings = model.encode(
            texts,
            normalize_embeddings=True,
        )

        return embeddings.tolist()
