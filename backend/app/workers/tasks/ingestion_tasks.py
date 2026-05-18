from app.rag.ingestion.cleaner import (
    clean_text,
)
from app.rag.ingestion.docx_loader import (
    load_docx,
)
from app.rag.ingestion.pdf_loader import (
    load_pdf,
)
from app.rag.pipelines.indexing_pipeline import (
    IndexingPipeline,
)
from app.workers.celery_workers import (
    celery_app,
)


@celery_app.task
def ingest_document_task(
    file_path: str,
):
    """
    Background document ingestion task.
    """

    # =====================================================
    # LOAD DOCUMENT
    # =====================================================

    if file_path.endswith(".pdf"):
        text = load_pdf(file_path)

    elif file_path.endswith(".docx"):
        text = load_docx(file_path)

    else:
        return {"error": "Unsupported file type."}

    # =====================================================
    # CLEAN TEXT
    # =====================================================

    cleaned_text = clean_text(text)

    # =====================================================
    # INDEX DOCUMENT
    # =====================================================

    pipeline = IndexingPipeline()

    result = pipeline.index_document(cleaned_text)

    return result
