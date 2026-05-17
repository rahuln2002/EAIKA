import os
from pathlib import Path

from app.utils.helpers import (
    current_timestamp,
    format_file_size,
)


def extract_metadata(
    file_path: str,
) -> dict:
    """
    Extract file metadata.
    """

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    file_stats = os.stat(file_path)

    metadata = {
        "filename": path.name,
        "extension": path.suffix,
        "size_bytes": file_stats.st_size,
        "size_readable": format_file_size(file_stats.st_size),
        "created_at": current_timestamp(),
    }

    return metadata
