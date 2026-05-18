from sentence_transformers import (
    CrossEncoder,
)


class RerankerService:
    """
    Cross-encoder reranking service.
    """

    MODEL_NAME = "cross-encoder/ms-marco-MiniLM-L-6-v2"

    model = CrossEncoder(MODEL_NAME)

    @classmethod
    def rerank(
        cls,
        query: str,
        documents: list[str],
        top_k: int = 5,
    ) -> list[str]:
        """
        Rerank retrieved documents.
        """

        if not documents:
            return []

        # =============================================
        # BUILD QUERY-DOCUMENT PAIRS
        # =============================================

        pairs = [[query, doc] for doc in documents]

        # =============================================
        # SCORE DOCUMENTS
        # =============================================

        scores = cls.model.predict(pairs)

        # =============================================
        # SORT BY SCORE
        # =============================================

        ranked_results = sorted(
            zip(documents, scores),
            key=lambda x: x[1],
            reverse=True,
        )

        # =============================================
        # RETURN TOP-K
        # =============================================

        return [doc for doc, _ in ranked_results[:top_k]]
