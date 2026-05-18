from app.rag.evaluators.faithfulness import (
    FaithfulnessEvaluator,
)
from app.rag.evaluators.hallucination import (
    HallucinationEvaluator,
)
from app.rag.evaluators.relevancy import (
    RelevancyEvaluator,
)
from app.rag.evaluators.retrieval_metrics import (
    RetrievalMetrics,
)


class AnalyticsService:
    """
    Enterprise RAG evaluation service.
    """

    @staticmethod
    def evaluate_response(
        query: str,
        answer: str,
        retrieved_context: list[str],
    ) -> dict:
        """
        Run complete RAG evaluation suite.
        """

        faithfulness = FaithfulnessEvaluator.evaluate(
            answer=answer,
            retrieved_context=(retrieved_context),
        )

        hallucination = HallucinationEvaluator.evaluate(
            answer=answer,
            retrieved_context=(retrieved_context),
        )

        relevancy = RelevancyEvaluator.evaluate(
            query=query,
            retrieved_context=(retrieved_context),
        )

        retrieval_metrics = RetrievalMetrics.evaluate(retrieved_context)

        return {
            "faithfulness": faithfulness,
            "hallucination": hallucination,
            "relevancy": relevancy,
            "retrieval_metrics": (retrieval_metrics),
        }
