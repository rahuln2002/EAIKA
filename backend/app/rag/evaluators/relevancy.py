from sentence_transformers import (
    SentenceTransformer,
    util,
)


class RelevancyEvaluator:
    """
    Retrieval relevancy evaluator.
    """

    MODEL_NAME = "sentence-transformers/paraphrase-MiniLM-L3-v2"

    model = None

    @classmethod
    def evaluate(
        cls,
        query: str,
        retrieved_context: list[str],
    ) -> dict:
        """
        Evaluate retrieval relevance.
        """

        if cls.model is None:
            cls.model = SentenceTransformer(cls.MODEL_NAME)

        if not retrieved_context:
            return {"avg_relevancy_score": 0.0}

        query_embedding = cls.model.encode(query)

        scores = []

        for chunk in retrieved_context:
            chunk_embedding = cls.model.encode(chunk)

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
