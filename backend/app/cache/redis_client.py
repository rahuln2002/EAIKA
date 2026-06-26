import redis

from app.core.config.settings import settings

# =========================================================
# REDIS CLIENT
# =========================================================

redis_client = redis.Redis.from_url(
    url=settings.REDIS_URL,
    decode_responses=True,
)


def get_redis_client() -> redis.Redis:
    """
    Return Redis client instance.
    """

    return redis_client
