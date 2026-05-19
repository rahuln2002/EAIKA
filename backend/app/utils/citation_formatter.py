def format_sources(
    sources: list[dict],
) -> list[dict]:
    """
    Format retrieved sources.
    """

    formatted = []

    for source in sources:
        formatted.append(
            {
                "citation": source["citation"],
                "document_id": source["document_id"],
                "chunk_id": source["chunk_id"],
                "preview": source["content"][:200],
            }
        )

    return formatted
