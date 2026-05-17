import redis

from app.core.config.settings import settings  # noqa: F401

# =========================================================
# REDIS CLIENT
# =========================================================

redis_client = redis.Redis(
    host="localhost",
    port=6379,
    db=0,
    decode_responses=True,
)


def get_redis_client() -> redis.Redis:
    """
    Return Redis client instance.
    """

    return redis_client
