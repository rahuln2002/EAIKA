from prometheus_client import Counter
from prometheus_client import Histogram

# =========================================================
# REQUEST METRICS
# =========================================================

REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total HTTP requests",
)

# =========================================================
# LATENCY METRICS
# =========================================================

REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds",
    "HTTP request latency",
)

# =========================================================
# ERROR METRICS
# =========================================================

ERROR_COUNT = Counter(
    "http_errors_total",
    "Total HTTP errors",
)
