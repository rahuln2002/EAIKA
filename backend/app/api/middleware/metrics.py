import time

from fastapi import FastAPI, Request

REQUEST_COUNT = 0


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
        global REQUEST_COUNT

        REQUEST_COUNT += 1

        start_time = time.time()

        response = await call_next(request)

        process_time = round(
            time.time() - start_time,
            4,
        )

        response.headers["X-Process-Time"] = str(process_time)

        response.headers["X-Request-Count"] = str(REQUEST_COUNT)

        return response
