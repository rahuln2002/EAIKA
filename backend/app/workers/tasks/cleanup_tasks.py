import os

from app.workers.celery_workers import (
    celery_app,
)
from app.monitoring.logging import logger

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

        except Exception as e:
            logger.warning(f"Cleanup task failed: {e}")

    return {"status": "cleanup completed"}
