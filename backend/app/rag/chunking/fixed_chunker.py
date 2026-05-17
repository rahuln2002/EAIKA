from langchain_text_splitters import (
    CharacterTextSplitter,
)


class FixedChunker:
    """
    Fixed-size text chunker.
    """

    def __init__(
        self,
        chunk_size: int = 500,
        chunk_overlap: int = 50,
    ) -> None:
        self.chunk_size = chunk_size

        self.chunk_overlap = chunk_overlap

        self.text_splitter = CharacterTextSplitter(
            separator="\n",
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
        )

    def chunk_text(
        self,
        text: str,
    ) -> list[str]:
        """
        Split text into fixed-size chunks.
        """

        return self.text_splitter.split_text(text)
