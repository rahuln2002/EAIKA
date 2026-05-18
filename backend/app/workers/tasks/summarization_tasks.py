from app.workers.celery_workers import (
    celery_app,
)
from app.services.summarization.summarization_service import (
    SummarizationService,
)


@celery_app.task
def summarize_document_task(
    text: str,
):
    """
    Background document summarization.
    """

    return SummarizationService.map_reduce_summarize(text=text)
