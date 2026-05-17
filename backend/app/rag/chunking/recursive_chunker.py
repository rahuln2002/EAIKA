from langchain_text_splitters import (
    RecursiveCharacterTextSplitter,
)


class RecursiveChunker:
    """
    Recursive semantic-aware chunker.
    """

    def __init__(
        self,
        chunk_size: int = 700,
        chunk_overlap: int = 100,
    ) -> None:
        self.chunk_size = chunk_size

        self.chunk_overlap = chunk_overlap

        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            separators=[
                "\n\n",
                "\n",
                ". ",
                " ",
                "",
            ],
        )

    def chunk_text(
        self,
        text: str,
    ) -> list[str]:
        """
        Split text recursively.
        """

        return self.text_splitter.split_text(text)
