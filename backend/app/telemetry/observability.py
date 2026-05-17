from app.monitoring.logging import (
    log_error,
    log_info,
)
from app.telemetry.tracing import (
    generate_trace_id,
)


def observe_event(
    message: str,
    level: str = "info",
    **kwargs,
) -> None:
    """
    Observe application event.
    """

    trace_id = generate_trace_id()

    event_data = {
        "trace_id": trace_id,
        **kwargs,
    }

    if level == "error":
        log_error(
            message,
            **event_data,
        )

    else:
        log_info(
            message,
            **event_data,
        )
