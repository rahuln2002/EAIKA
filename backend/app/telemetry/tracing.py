import uuid


def generate_trace_id() -> str:
    """
    Generate unique trace ID.
    """

    return str(uuid.uuid4())
