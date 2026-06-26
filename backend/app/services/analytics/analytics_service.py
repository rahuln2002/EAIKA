from sqlalchemy.orm import Session

from app.db.models.analytics import Analytics

from app.rag.evaluators.faithfulness import FaithfulnessEvaluator
from app.rag.evaluators.hallucination import HallucinationEvaluator
from app.rag.evaluators.relevancy import RelevancyEvaluator
from app.rag.evaluators.retrieval_metrics import RetrievalMetrics

from app.monitoring.logging import logger


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

        return {
            "faithfulness": FaithfulnessEvaluator.evaluate(
                answer=answer,
                retrieved_context=retrieved_context,
            ),
            "hallucination": HallucinationEvaluator.evaluate(
                answer=answer,
                retrieved_context=retrieved_context,
            ),
            "relevancy": RelevancyEvaluator.evaluate(
                query=query,
                retrieved_context=retrieved_context,
            ),
            "retrieval_metrics": RetrievalMetrics.evaluate(retrieved_context),
        }

    @staticmethod
    def log_analytics(
        db: Session,
        user_id: int,
        query: str,
        total_response_time: float,
        retrieved_chunks: int,
        retrieval_latency: float,
        history_latency: float,
        llm_latency: float,
        provider: str = "mistral",
        event_type: str = "chat",
    ) -> None:
        """
        Persist analytics event.
        """

        try:
            analytics = Analytics(
                user_id=user_id,
                event_type=event_type,
                provider=provider,
                query=query,
                latency=total_response_time,
                retrieval_latency=retrieval_latency,
                history_latency=history_latency,
                llm_latency=llm_latency,
                retrieved_chunks=retrieved_chunks,
            )

            db.add(analytics)
            db.commit()

        except Exception as e:
            db.rollback()

            logger.warning(f"Failed to log analytics: {e}")
