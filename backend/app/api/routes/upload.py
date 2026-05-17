from fastapi import APIRouter
from fastapi import File
from fastapi import UploadFile

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
from app.utils.file_utils import (
    save_uploaded_file,
)
from app.utils.validators import (
    validate_file_extension,
    validate_file_size,
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
    # LOAD TEXT
    # =====================================================

    if file.filename.endswith(".pdf"):
        document_text = load_pdf(file_path)

    elif file.filename.endswith(".docx"):
        document_text = load_docx(file_path)

    else:
        return {
            "error": "Unsupported file type.",
        }

    # =====================================================
    # CLEAN TEXT
    # =====================================================

    cleaned_text = clean_text(document_text)

    # =====================================================
    # INDEX DOCUMENT
    # =====================================================

    result = indexing_pipeline.index_document(cleaned_text)

    return {
        "message": "Document indexed successfully.",
        "result": result,
    }
