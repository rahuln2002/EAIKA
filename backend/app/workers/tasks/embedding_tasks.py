from app.services.embeddings.embedding_manager import (
    EmbeddingManager,
)
from app.workers.celery_workers import (
    celery_app,
)


@celery_app.task
def generate_embeddings_task(
    chunks: list[str],
):
    """
    Generate embeddings asynchronously.
    """

    embeddings = EmbeddingManager.embed_texts(chunks)

    return embeddings
