import time

from fastapi import FastAPI, Request

from app.core.config.logging_config import logger


def setup_request_logging_middleware(
    app: FastAPI,
) -> None:
    """
    Configure request logging middleware.
    """

    @app.middleware("http")
    async def log_requests(
        request: Request,
        call_next,
    ):
        start_time = time.time()

        response = await call_next(request)

        process_time = round(
            time.time() - start_time,
            4,
        )

        logger.info(
            "HTTP Request",
            method=request.method,
            path=request.url.path,
            status_code=response.status_code,
            duration=process_time,
        )

        return response
