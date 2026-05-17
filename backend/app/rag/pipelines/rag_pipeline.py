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
    End-to-end Retrieval-Augmented Generation pipeline.
    """

    def __init__(
        self,
        documents: list[str],
        provider: str = "openai",
    ) -> None:
        self.provider = provider

        self.retrieval_service = RetrievalService(documents)

    def run(
        self,
        query: str,
        top_k: int = 5,
    ) -> dict:
        """
        Execute full RAG pipeline.
        """

        retrieval_results = self.retrieval_service.retrieve_context(
            query=query,
            top_k=top_k,
        )

        # =================================================
        # EXTRACT CONTEXT
        # =================================================

        dense_results = retrieval_results["dense_results"]

        context_chunks = []

        for result in dense_results:
            payload = getattr(
                result,
                "payload",
                {},
            )

            if "text" in payload:
                context_chunks.append(payload["text"])

        # =================================================
        # BUILD PROMPT
        # =================================================

        prompt = build_rag_prompt(
            query=query,
            context_chunks=context_chunks,
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
        }
