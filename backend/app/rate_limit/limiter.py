from fastapi import HTTPException, status

from app.cache.redis_client import (
    get_redis_client,
)

redis_client = get_redis_client()

# =========================================================
# RATE LIMIT CONFIG
# =========================================================

RATE_LIMIT = 100
WINDOW_SECONDS = 60


def check_rate_limit(
    identifier: str,
) -> None:
    """
    Check and enforce rate limits.
    """

    key = f"rate_limit:{identifier}"

    current_count = redis_client.get(key)

    if current_count is None:
        redis_client.set(
            key,
            1,
            ex=WINDOW_SECONDS,
        )

        return

    current_count = int(current_count)

    if current_count >= RATE_LIMIT:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded.",
        )

    redis_client.incr(key)
