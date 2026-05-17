import logging
import sys

import structlog

from app.core.config.settings import settings


def setup_logging() -> None:
    """
    Configure structured logging for the application.
    """

    timestamper = structlog.processors.TimeStamper(fmt="iso")

    structlog.configure(
        processors=[
            structlog.stdlib.add_log_level,
            timestamper,
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.dev.ConsoleRenderer(),
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

    logging.basicConfig(
        level=settings.LOG_LEVEL,
        format="%(message)s",
        stream=sys.stdout,
    )


logger = structlog.get_logger()
