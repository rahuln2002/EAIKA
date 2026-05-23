from sqlalchemy.orm import Session

from app.db.models.analytics import (
    Analytics,
)

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
    Enterprise RAG analytics service.
    """

    @staticmethod
    def evaluate_response(
        query: str,
        answer: str,
        retrieved_context: list[str],
    ) -> dict:
        """
        Run evaluation suite.
        """

        faithfulness = FaithfulnessEvaluator.evaluate(
            answer=answer,
            retrieved_context=retrieved_context,
        )

        hallucination = HallucinationEvaluator.evaluate(
            answer=answer,
            retrieved_context=retrieved_context,
        )

        relevancy = RelevancyEvaluator.evaluate(
            query=query,
            retrieved_context=retrieved_context,
        )

        retrieval_metrics = RetrievalMetrics.evaluate(retrieved_context)

        return {
            "faithfulness": faithfulness,
            "hallucination": hallucination,
            "relevancy": relevancy,
            "retrieval_metrics": retrieval_metrics,
        }

    @staticmethod
    def log_analytics(
        db: Session,
        user_id: int,
        query: str,
        response_time: float,
        retrieved_chunks: int,
    ):
        """
        Persist analytics event.
        """

        analytics = Analytics(
            user_id=user_id,
            query=query,
            response_time=response_time,
            retrieved_chunks=retrieved_chunks,
        )

        db.add(analytics)

        db.commit()
