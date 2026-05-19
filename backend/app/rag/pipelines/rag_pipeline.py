from sqlalchemy.orm import Session

from app.rag.prompts.retrieval_prompt import (
    build_rag_prompt,
)
from app.services.llm.provider_manager import (
    ProviderManager,
)
from app.services.retrieval.retrieval_service import (
    RetrievalService,
)
from app.services.analytics.analytics_service import (
    AnalyticsService,
)


class RAGPipeline:
    """
    Conversational RAG pipeline.
    """

    def __init__(
        self,
        provider: str = "openai",
    ) -> None:
        self.provider = provider

        self.retrieval_service = RetrievalService()

    def run(
        self,
        db: Session,
        query: str,
        user_id: int,
        conversation_history: list[str],
        top_k: int = 5,
    ) -> dict:
        """
        Execute conversational RAG pipeline.
        """

        # =================================================
        # RETRIEVE CONTEXT
        # =================================================

        context_chunks = self.retrieval_service.retrieve_context(
            db=db,
            query=query,
            user_id=user_id,
            top_k=top_k,
        )

        context_texts = [chunk["content"] for chunk in context_chunks]

        # =================================================
        # BUILD CONVERSATIONAL PROMPT
        # =================================================

        prompt = build_rag_prompt(
            query=query,
            context_chunks=context_texts,
            conversation_history=conversation_history,
        )

        # =================================================
        # GENERATE RESPONSE
        # =================================================

        answer = ProviderManager.generate_response(
            provider=self.provider,
            prompt=prompt,
        )

        # =============================================
        # APPEND CITATIONS
        # =============================================

        citations = [chunk["citation"] for chunk in context_chunks]

        cited_answer = answer + "\n\nSources: " + " ".join(citations)

        # =============================================
        # RUN EVALUATION
        # =============================================

        evaluation = AnalyticsService.evaluate_response(
            query=query,
            answer=cited_answer,
            retrieved_context=context_texts,
        )

        return {
            "query": query,
            "answer": cited_answer,
            "retrieved_context": context_texts,
            "conversation_history": (conversation_history),
            "retrieval_strategy": ("hybrid+dense+rerank"),
            "evaluation": evaluation,
        }
