from fastapi import status

from app.exceptions.error_codes import (
    CHAT_NOT_FOUND,
    DOCUMENT_NOT_FOUND,
    INVALID_CREDENTIALS,
    USER_NOT_FOUND,
)


class AppException(Exception):
    """
    Base application exception.
    """

    def __init__(
        self,
        message: str,
        error_code: str,
        status_code: int,
    ) -> None:
        self.message = message
        self.error_code = error_code
        self.status_code = status_code

        super().__init__(message)


# =========================================================
# AUTH EXCEPTIONS
# =========================================================


class InvalidCredentialsException(AppException):
    def __init__(self) -> None:
        super().__init__(
            message="Invalid email or password.",
            error_code=INVALID_CREDENTIALS,
            status_code=status.HTTP_401_UNAUTHORIZED,
        )


class UserNotFoundException(AppException):
    def __init__(self) -> None:
        super().__init__(
            message="User does not exist.",
            error_code=USER_NOT_FOUND,
            status_code=status.HTTP_404_NOT_FOUND,
        )


# =========================================================
# DOCUMENT EXCEPTIONS
# =========================================================


class DocumentNotFoundException(AppException):
    def __init__(self) -> None:
        super().__init__(
            message="Document not found.",
            error_code=DOCUMENT_NOT_FOUND,
            status_code=status.HTTP_404_NOT_FOUND,
        )


# =========================================================
# CHAT EXCEPTIONS
# =========================================================


class ChatNotFoundException(AppException):
    def __init__(self) -> None:
        super().__init__(
            message="Chat not found.",
            error_code=CHAT_NOT_FOUND,
            status_code=status.HTTP_404_NOT_FOUND,
        )
