import requests

from app.core.config.settings import settings


class EmbeddingService:
    @staticmethod
    def generate_embeddings(
        texts: list[str],
    ) -> list[list[float]]:

        response = requests.post(
            settings.EMBEDDING_API_URL,
            headers={
                "Authorization": f"Bearer {settings.JINA_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": "jina-embeddings-v3",
                "input": texts,
            },
            timeout=60,
        )

        response.raise_for_status()

        data = response.json()["data"]

        return [item["embedding"] for item in data]

    @staticmethod
    def generate_query_embedding(
        query: str,
    ) -> list[float]:

        return EmbeddingService.generate_embeddings([query])[0]


# from sentence_transformers import (
#     SentenceTransformer,
# )

# from app.core.config.settings import settings

# # =========================================================
# # GLOBAL MODEL HOLDER
# # =========================================================

# embedding_model = None


# def get_embedding_model():
#     """
#     Lazy-load embedding model.
#     """

#     global embedding_model

#     if embedding_model is None:
#         embedding_model = SentenceTransformer(
#             settings.EMBEDDING_MODEL,
#         )

#     return embedding_model


# class EmbeddingService:
#     @staticmethod
#     def generate_embeddings(
#         texts: list[str],
#     ) -> list[list[float]]:
#         """
#         Generate document embeddings.
#         """

#         model = get_embedding_model()

#         embeddings = model.encode(
#             texts,
#             convert_to_numpy=True,
#         )

#         return embeddings.tolist()

#     @staticmethod
#     def generate_query_embedding(
#         query: str,
#     ) -> list[float]:
#         """
#         Generate query embedding.
#         """

#         model = get_embedding_model()

#         embedding = model.encode(
#             query,
#             convert_to_numpy=True,
#         )

#         return embedding.tolist()
