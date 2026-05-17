from fastapi import Request

from app.rate_limit.limiter import (
    check_rate_limit,
)


def rate_limit_dependency(
    request: Request,
) -> None:
    """
    FastAPI rate limit dependency.
    """

    client_ip = request.client.host

    check_rate_limit(client_ip)
