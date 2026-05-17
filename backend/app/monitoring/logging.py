from app.core.config.logging_config import (
    logger,
)


def log_info(
    message: str,
    **kwargs,
) -> None:
    """
    Log info message.
    """

    logger.info(
        message,
        **kwargs,
    )


def log_error(
    message: str,
    **kwargs,
) -> None:
    """
    Log error message.
    """

    logger.error(
        message,
        **kwargs,
    )
