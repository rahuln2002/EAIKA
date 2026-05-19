import time

from starlette.middleware.base import (
    BaseHTTPMiddleware,
)

from app.monitoring.metrics import (
    REQUEST_COUNT,
    REQUEST_LATENCY,
)


class MetricsMiddleware(BaseHTTPMiddleware):
    """
    Prometheus metrics middleware.
    """

    async def dispatch(
        self,
        request,
        call_next,
    ):
        REQUEST_COUNT.inc()

        start_time = time.time()

        response = await call_next(request)

        duration = time.time() - start_time

        REQUEST_LATENCY.observe(duration)

        return response
