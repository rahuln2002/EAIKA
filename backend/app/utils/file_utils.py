import os
import uuid
from pathlib import Path

from fastapi import UploadFile

# =========================================================
# STORAGE DIRECTORIES
# =========================================================

BASE_UPLOAD_DIR = "data/raw"


def ensure_upload_directory() -> None:
    """
    Ensure upload directory exists.
    """

    Path(BASE_UPLOAD_DIR).mkdir(
        parents=True,
        exist_ok=True,
    )


def generate_unique_filename(
    filename: str,
) -> str:
    """
    Generate unique filename.
    """

    extension = Path(filename).suffix

    unique_name = f"{uuid.uuid4()}{extension}"

    return unique_name


async def save_uploaded_file(
    file: UploadFile,
) -> str:
    """
    Save uploaded file to disk.
    """

    ensure_upload_directory()

    unique_filename = generate_unique_filename(file.filename)

    file_path = os.path.join(
        BASE_UPLOAD_DIR,
        unique_filename,
    )

    contents = await file.read()

    with open(file_path, "wb") as output_file:
        output_file.write(contents)

    return file_path


def delete_file(
    file_path: str,
) -> None:
    """
    Delete file from disk.
    """

    if os.path.exists(file_path):
        os.remove(file_path)
