from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.exceptions.custom_exceptions import AppException
from app.exceptions.error_codes import (
    INTERNAL_SERVER_ERROR,
    VALIDATION_ERROR,
)


def register_exception_handlers(
    app: FastAPI,
) -> None:
    """
    Register global exception handlers.
    """

    # =====================================================
    # CUSTOM APPLICATION EXCEPTIONS
    # =====================================================

    @app.exception_handler(AppException)
    async def app_exception_handler(
        request: Request,
        exc: AppException,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "success": False,
                "error": {
                    "code": exc.error_code,
                    "message": exc.message,
                },
            },
        )

    # =====================================================
    # VALIDATION ERRORS
    # =====================================================

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request,
        exc: RequestValidationError,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=422,
            content={
                "success": False,
                "error": {
                    "code": VALIDATION_ERROR,
                    "message": "Validation failed.",
                    "details": exc.errors(),
                },
            },
        )

    # =====================================================
    # GENERIC EXCEPTIONS
    # =====================================================

    @app.exception_handler(Exception)
    async def generic_exception_handler(
        request: Request,
        exc: Exception,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": {
                    "code": INTERNAL_SERVER_ERROR,
                    "message": "Internal server error.",
                },
            },
        )
