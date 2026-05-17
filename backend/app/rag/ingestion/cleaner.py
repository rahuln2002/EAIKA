import re


def clean_text(
    text: str,
) -> str:
    """
    Clean extracted document text.
    """

    # =====================================================
    # REMOVE EXTRA WHITESPACES
    # =====================================================

    text = re.sub(
        r"\s+",
        " ",
        text,
    )

    # =====================================================
    # REMOVE MULTIPLE NEWLINES
    # =====================================================

    text = re.sub(
        r"\n+",
        "\n",
        text,
    )

    # =====================================================
    # REMOVE NULL CHARACTERS
    # =====================================================

    text = text.replace(
        "\x00",
        "",
    )

    return text.strip()
