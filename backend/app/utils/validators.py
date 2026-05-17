from pathlib import Path

from fastapi import HTTPException, UploadFile, status

from app.core.config.settings import (
    settings,
)


def validate_file_extension(
    filename: str,
) -> None:
    """
    Validate file extension.
    """

    extension = Path(filename).suffix.lower()

    if extension not in settings.ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unsupported file type.",
        )


async def validate_file_size(
    file: UploadFile,
) -> None:
    """
    Validate uploaded file size.
    """

    contents = await file.read()

    file_size_mb = len(contents) / (1024 * 1024)

    await file.seek(0)

    if file_size_mb > settings.MAX_UPLOAD_SIZE_MB:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File size exceeds limit.",
        )
