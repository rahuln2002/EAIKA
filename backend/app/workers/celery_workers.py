from celery import Celery

from app.core.config.settings import (
    settings,
)

# =========================================================
# INITIALIZE CELERY
# =========================================================

celery_app = Celery(
    "enterprise_ai_ka",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
)

# =========================================================
# CELERY CONFIG
# =========================================================

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    enable_utc=True,
)

# =========================================================
# IMPORT TASK MODULES
# =========================================================

celery_app.autodiscover_tasks(
    [
        "app.workers.tasks",
    ]
)
