import os

from app.workers.celery_workers import (
    celery_app,
)

TEMP_DIRECTORY = "data/temp"


@celery_app.task
def cleanup_temp_files():
    """
    Cleanup temporary files.
    """

    if not os.path.exists(TEMP_DIRECTORY):
        return

    for filename in os.listdir(TEMP_DIRECTORY):
        file_path = os.path.join(
            TEMP_DIRECTORY,
            filename,
        )

        try:
            os.remove(file_path)

        except Exception:
            pass

    return {"status": "cleanup completed"}
