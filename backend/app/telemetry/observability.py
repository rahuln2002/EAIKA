import time
from functools import wraps

from app.telemetry.tracing import (
    tracer,
)


def trace_function(
    span_name: str,
):
    """
    Trace function execution.
    """

    def decorator(func):
        @wraps(func)
        def wrapper(
            *args,
            **kwargs,
        ):
            with tracer.start_as_current_span(span_name) as span:
                start_time = time.time()

                result = func(
                    *args,
                    **kwargs,
                )

                duration = time.time() - start_time

                span.set_attribute(
                    "execution_time",
                    duration,
                )

                return result

        return wrapper

    return decorator
