from fastembed import TextEmbedding

from app.core.config.settings import settings

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
        embedding_model = TextEmbedding(
            model_name=settings.EMBEDDING_MODEL,
        )

    return embedding_model


class EmbeddingService:
    @staticmethod
    def generate_embeddings(
        texts: list[str],
    ) -> list[list[float]]:
        """
        Generate embeddings for documents.
        """

        model = get_embedding_model()

        embeddings = list(model.embed(texts))

        return [embedding.tolist() for embedding in embeddings]

    @staticmethod
    def generate_query_embedding(
        query: str,
    ) -> list[float]:
        """
        Generate query embedding.
        """

        model = get_embedding_model()

        embedding = list(model.embed([query]))[0]

        return embedding.tolist()
