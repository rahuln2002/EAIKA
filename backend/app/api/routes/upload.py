from fastapi import APIRouter
from fastapi import Depends
from fastapi import File
from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.api.dependencies.auth import (
    get_current_user,
)
from app.api.dependencies.database import (
    get_db,
)
from app.rag.ingestion.cleaner import (
    clean_text,
)
from app.rag.ingestion.docx_loader import (
    load_docx,
)
from app.rag.ingestion.pdf_loader import (
    load_pdf,
)
from app.services.chat.upload_service import (
    UploadService,
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


@router.post("/")
async def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    Persistent upload endpoint.
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
    # PERSIST DOCUMENT
    # =====================================================

    document = UploadService.create_document(
        db=db,
        filename=file.filename,
        file_path=file_path,
        owner_id=int(current_user["sub"]),
    )

    # =====================================================
    # LOAD DOCUMENT TEXT
    # =====================================================

    if file.filename.endswith(".pdf"):
        text = load_pdf(file_path)

    elif file.filename.endswith(".docx"):
        text = load_docx(file_path)

    else:
        return {"error": "Unsupported file type."}

    cleaned_text = clean_text(text)

    # =====================================================
    # STORE CHUNKS
    # =====================================================

    total_chunks = UploadService.store_chunks(
        db=db,
        document_id=document.id,
        text=cleaned_text,
    )

    return {
        "message": "Document uploaded successfully.",
        "document_id": document.id,
        "chunks_created": total_chunks,
    }
