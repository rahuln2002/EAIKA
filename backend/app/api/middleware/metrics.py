import time

from fastapi import FastAPI, Request

from app.monitoring.metrics import (
    ERROR_COUNT,
    REQUEST_COUNT,
    REQUEST_LATENCY,
)

REQUEST_COUNT_LOCAL = 0


def setup_metrics_middleware(
    app: FastAPI,
) -> None:
    """
    Configure metrics middleware.
    """

    @app.middleware("http")
    async def metrics_middleware(
        request: Request,
        call_next,
    ):
        REQUEST_COUNT.inc()

        start_time = time.time()

        try:
            response = await call_next(request)

        except Exception:
            ERROR_COUNT.inc()
            raise

        process_time = round(
            time.time() - start_time,
            4,
        )

        REQUEST_LATENCY.observe(process_time)

        response.headers["X-Process-Time"] = str(process_time)

        return response
