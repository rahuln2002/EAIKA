from fastapi import APIRouter
from fastapi import File
from fastapi import UploadFile

from app.rag.pipelines.indexing_pipeline import (
    IndexingPipeline,
)
from app.utils.file_utils import (
    save_uploaded_file,
)
from app.utils.validators import (
    validate_file_extension,
    validate_file_size,
)
from app.workers.tasks.ingestion_tasks import (
    ingest_document_task,
)

router = APIRouter(
    prefix="/upload",
    tags=["Upload"],
)

indexing_pipeline = IndexingPipeline()


@router.post("/")
async def upload_document(
    file: UploadFile = File(...),
):
    """
    Upload and index document.
    """

    # =====================================================
    # VALIDATION
    # =====================================================

    validate_file_extension(file.filename)

    await validate_file_size(file)

    # =====================================================
    # SAVE FILE
    # =====================================================

    file_path = await save_uploaded_file(file)

    # =====================================================
    # INDEX DOCUMENT
    # =====================================================

    task = ingest_document_task.delay(file_path)

    return {
        "message": "Document queued for indexing.",
        "task_id": task.id,
    }
