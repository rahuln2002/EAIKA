from datetime import datetime


def current_timestamp() -> str:
    """
    Return current UTC timestamp.
    """

    return datetime.utcnow().isoformat()


def format_file_size(
    size_bytes: int,
) -> str:
    """
    Format bytes into readable size.
    """

    for unit in ["B", "KB", "MB", "GB"]:
        if size_bytes < 1024:
            return f"{size_bytes:.2f} {unit}"

        size_bytes /= 1024

    return f"{size_bytes:.2f} TB"
