from sentence_transformers import (
    SentenceTransformer,
    util,
)
from app.core.config.settings import settings


class RelevancyEvaluator:
    """
    Retrieval relevancy evaluator.
    """

    @classmethod
    def evaluate(
        query: str,
        retrieved_context: list[str],
    ) -> dict:
        """
        Evaluate retrieval relevance.
        """

        model = SentenceTransformer(settings.EMBEDDING_MODEL)

        if not retrieved_context:
            return {"avg_relevancy_score": 0.0}

        query_embedding = model.encode(query)

        scores = []

        for chunk in retrieved_context:
            chunk_embedding = model.encode(chunk)

            similarity = util.cos_sim(
                query_embedding,
                chunk_embedding,
            )

            scores.append(float(similarity))

        avg_score = sum(scores) / len(scores)

        return {
            "avg_relevancy_score": round(
                avg_score,
                3,
            )
        }
