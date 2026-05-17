import tiktoken

# =========================================================
# TOKENIZER
# =========================================================

encoding = tiktoken.get_encoding("cl100k_base")


def count_tokens(
    text: str,
) -> int:
    """
    Count tokens in text.
    """

    tokens = encoding.encode(text)

    return len(tokens)


def truncate_tokens(
    text: str,
    max_tokens: int,
) -> str:
    """
    Truncate text to max token limit.
    """

    tokens = encoding.encode(text)

    truncated = tokens[:max_tokens]

    return encoding.decode(truncated)
