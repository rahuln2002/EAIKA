from app.rag.chunking.recursive_chunker import (
    RecursiveChunker,
)
from app.rag.prompts.summarization_prompt import (
    build_reduce_prompt,
    build_summary_prompt,
)
from app.services.llm.provider_manager import (
    ProviderManager,
)


class SummarizationService:
    """
    Enterprise document summarization.
    """

    @staticmethod
    def summarize_text(
        text: str,
        provider: str = "groq",
    ) -> str:
        """
        Summarize text directly.
        """

        prompt = build_summary_prompt(text)

        summary = ProviderManager.generate_response(
            provider=provider,
            prompt=prompt,
        )

        return summary

    @staticmethod
    def map_reduce_summarize(
        text: str,
        provider: str = "groq",
    ) -> dict:
        """
        Perform hierarchical summarization.
        """

        # =============================================
        # CHUNK DOCUMENT
        # =============================================

        chunker = RecursiveChunker(
            chunk_size=1500,
            chunk_overlap=200,
        )

        chunks = chunker.chunk_text(text)

        # =============================================
        # MAP STEP
        # =============================================

        partial_summaries = []

        for chunk in chunks:
            summary = SummarizationService.summarize_text(
                text=chunk,
                provider=provider,
            )

            partial_summaries.append(summary)

        # =============================================
        # REDUCE STEP
        # =============================================

        reduce_prompt = build_reduce_prompt(partial_summaries)

        final_summary = ProviderManager.generate_response(
            provider=provider,
            prompt=reduce_prompt,
        )

        return {
            "total_chunks": len(chunks),
            "partial_summaries": (partial_summaries),
            "final_summary": final_summary,
        }
