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
            top_k=top_k,
        )

        # =================================================
        # BUILD CONVERSATIONAL PROMPT
        # =================================================

        prompt = build_rag_prompt(
            query=query,
            context_chunks=context_chunks,
            conversation_history=conversation_history,
        )

        # =================================================
        # GENERATE RESPONSE
        # =================================================

        answer = ProviderManager.generate_response(
            provider=self.provider,
            prompt=prompt,
        )

        return {
            "query": query,
            "answer": answer,
            "retrieved_context": context_chunks,
            "conversation_history": (conversation_history),
            "retrieval_strategy": "dense+rereank",
        }
