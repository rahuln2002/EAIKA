import re


class SemanticChunker:
    """
    Lightweight semantic chunker.
    """

    def __init__(
        self,
        max_chunk_size: int = 1000,
    ) -> None:
        self.max_chunk_size = max_chunk_size

    def chunk_text(
        self,
        text: str,
    ) -> list[str]:
        """
        Chunk text semantically using paragraphs.
        """

        paragraphs = re.split(
            r"\n\s*\n",
            text,
        )

        chunks = []

        current_chunk = ""

        for paragraph in paragraphs:
            if len(current_chunk) + len(paragraph) < self.max_chunk_size:
                current_chunk += paragraph + "\n\n"

            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())

                current_chunk = paragraph

        if current_chunk:
            chunks.append(current_chunk.strip())

        return chunks
