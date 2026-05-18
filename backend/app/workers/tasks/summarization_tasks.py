from app.services.llm.provider_manager import (
    ProviderManager,
)
from app.workers.celery_workers import (
    celery_app,
)


@celery_app.task
def summarize_document_task(
    text: str,
):
    """
    Summarize document asynchronously.
    """

    prompt = f"""
Summarize the following document:

{text}
"""

    summary = ProviderManager.generate_response(
        provider="openai",
        prompt=prompt,
    )

    return summary
