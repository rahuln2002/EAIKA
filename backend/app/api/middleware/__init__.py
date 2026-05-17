from app.api.middleware.auth_middleware import (
    setup_auth_middleware,
)
from app.api.middleware.cors import setup_cors
from app.api.middleware.logging import (
    setup_request_logging_middleware,
)
from app.api.middleware.metrics import (
    setup_metrics_middleware,
)

__all__ = [
    "setup_cors",
    "setup_request_logging_middleware",
    "setup_metrics_middleware",
    "setup_auth_middleware",
]
