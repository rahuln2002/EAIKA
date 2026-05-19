from prometheus_client import (
    Counter,
    Histogram,
)

REQUEST_COUNT = Counter(
    "request_count",
    "Total API Requests",
)

REQUEST_LATENCY = Histogram(
    "request_latency_seconds",
    "API Request Latency",
)

LLM_REQUEST_COUNT = Counter(
    "llm_request_count",
    "Total LLM Requests",
)

RETRIEVAL_REQUEST_COUNT = Counter(
    "retrieval_request_count",
    "Total Retrieval Requests",
)
