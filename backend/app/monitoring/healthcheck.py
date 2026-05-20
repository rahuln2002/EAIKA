from sqlalchemy import text

from app.cache.redis_client import (
    get_redis_client,
)
from app.db.session import engine
from app.monitoring.logging import logger


async def healthcheck() -> dict:
    """
    Perform application health checks.
    """

    health_status = {
        "api": "healthy",
        "database": "unhealthy",
        "redis": "unhealthy",
    }

    # =====================================================
    # DATABASE HEALTH
    # =====================================================

    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        health_status["database"] = "healthy"

    except Exception as e:
        logger.warning(f"Healthcheck failed: {e}")

    # =====================================================
    # REDIS HEALTH
    # =====================================================

    try:
        redis_client = get_redis_client()

        redis_client.ping()

        health_status["redis"] = "healthy"

    except Exception as e:
        logger.warning(f"Healthcheck failed: {e}")

    return health_status
