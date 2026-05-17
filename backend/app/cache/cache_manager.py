import json
from typing import Any

from app.cache.redis_client import (
    get_redis_client,
)

redis_client = get_redis_client()


class CacheManager:
    """
    Centralized cache manager.
    """

    @staticmethod
    def set(
        key: str,
        value: Any,
        expire: int = 3600,
    ) -> None:
        """
        Store value in Redis cache.
        """

        redis_client.set(
            key,
            json.dumps(value),
            ex=expire,
        )

    @staticmethod
    def get(
        key: str,
    ) -> Any | None:
        """
        Retrieve cached value.
        """

        value = redis_client.get(key)

        if value is None:
            return None

        return json.loads(value)

    @staticmethod
    def delete(
        key: str,
    ) -> None:
        """
        Delete cached value.
        """

        redis_client.delete(key)
