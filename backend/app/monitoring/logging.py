import logging

# =========================================================
# LOGGING CONFIGURATION
# =========================================================

logging.basicConfig(
    level=logging.INFO,
    format=("%(asctime)s - %(name)s - %(levelname)s - %(message)s"),
)

logger = logging.getLogger("enterprise-ai-ka")

# =========================================================
# HELPER FUNCTIONS
# =========================================================


def log_info(message: str):
    logger.info(message)


def log_warning(message: str):
    logger.warning(message)


def log_error(
    error: Exception,
    path: str | None = None,
):
    logger.error(f"Error: {error} | Path: {path}")
