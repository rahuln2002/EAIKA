from app.services.summarization.summarization_service import (
    SummarizationService,
)


class SummarizerAgent:
    """
    Enterprise summarization agent.
    """

    @staticmethod
    def summarize_document(
        text: str,
    ) -> dict:
        """
        Run document summarization.
        """

        return SummarizationService.map_reduce_summarize(text=text)
