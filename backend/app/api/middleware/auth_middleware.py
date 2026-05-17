from fastapi import FastAPI, Request


def setup_auth_middleware(
    app: FastAPI,
) -> None:
    """
    Configure auth middleware.
    """

    @app.middleware("http")
    async def auth_middleware(
        request: Request,
        call_next,
    ):
        authorization = request.headers.get("Authorization")

        if authorization:
            request.state.authorization = authorization

        response = await call_next(request)

        return response
