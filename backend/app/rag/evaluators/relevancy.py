from numpy import dot
from numpy.linalg import norm

from app.services.embeddings.embedding_service import (
    EmbeddingService,
)


class RelevancyEvaluator:
    """
    Retrieval relevancy evaluator.
    """

    @staticmethod
    def cosine_similarity(
        embedding_1: list[float],
        embedding_2: list[float],
    ) -> float:
        """
        Compute cosine similarity.
        """

        return float(
            dot(embedding_1, embedding_2) / (norm(embedding_1) * norm(embedding_2))
        )

    @classmethod
    def evaluate(
        cls,
        query: str,
        retrieved_context: list[str],
    ) -> dict:
        """
        Evaluate retrieval relevance.
        """

        if not retrieved_context:
            return {
                "avg_relevancy_score": 0.0,
            }

        # =============================================
        # GENERATE EMBEDDINGS
        # =============================================

        query_embedding = EmbeddingService.generate_query_embedding(
            query,
        )

        context_embeddings = EmbeddingService.generate_embeddings(
            retrieved_context,
        )

        # =============================================
        # CALCULATE SIMILARITIES
        # =============================================

        scores = [
            cls.cosine_similarity(
                query_embedding,
                embedding,
            )
            for embedding in context_embeddings
        ]

        avg_score = sum(scores) / len(scores)

        return {
            "avg_relevancy_score": round(
                avg_score,
                3,
            )
        }


# from sentence_transformers import (
#     SentenceTransformer,
#     util,
# )
# from app.core.config.settings import settings


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


# class RelevancyEvaluator:
#     """
#     Retrieval relevancy evaluator.
#     """

#     @classmethod
#     def evaluate(
#         query: str,
#         retrieved_context: list[str],
#     ) -> dict:
#         """
#         Evaluate retrieval relevance.
#         """

#         model = get_embedding_model()

#         if not retrieved_context:
#             return {"avg_relevancy_score": 0.0}

#         query_embedding = model.encode(query)

#         scores = []

#         for chunk in retrieved_context:
#             chunk_embedding = model.encode(chunk)

#             similarity = util.cos_sim(
#                 query_embedding,
#                 chunk_embedding,
#             )

#             scores.append(float(similarity))

#         avg_score = sum(scores) / len(scores)

#         return {
#             "avg_relevancy_score": round(
#                 avg_score,
#                 3,
#             )
#         }
