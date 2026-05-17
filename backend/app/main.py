from fastapi import FastAPI

from app.api.middleware import (
    setup_auth_middleware,
    setup_cors,
    setup_metrics_middleware,
    setup_request_logging_middleware,
)
from app.core.config import (
    logger,
    settings,
    setup_logging,
)
from app.exceptions import (
    register_exception_handlers,
)

# =========================================================
# INITIALIZE APP
# =========================================================

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
)

# =========================================================
# LOGGING
# =========================================================

setup_logging()

logger.info("Starting application...")

# =========================================================
# MIDDLEWARE
# =========================================================

setup_cors(app)

setup_request_logging_middleware(app)

setup_metrics_middleware(app)

setup_auth_middleware(app)

# =========================================================
# EXCEPTION HANDLERS
# =========================================================

register_exception_handlers(app)


# =========================================================
# ROOT ROUTE
# =========================================================


@app.get("/")
async def root():
    return {
        "message": "Enterprise AI Knowledge Assistant API",
    }
