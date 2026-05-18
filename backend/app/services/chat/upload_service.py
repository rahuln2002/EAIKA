from sqlalchemy.orm import Session

from app.db.models.chunk import Chunk
from app.db.models.document import (
    Document,
)
from app.rag.chunking.recursive_chunker import (
    RecursiveChunker,
)


class UploadService:
    """
    Persistent upload service.
    """

    @staticmethod
    def create_document(
        db: Session,
        filename: str,
        file_path: str,
        owner_id: int,
    ) -> Document:
        """
        Persist uploaded document.
        """

        document = Document(
            filename=filename,
            file_path=file_path,
            owner_id=owner_id,
        )

        db.add(document)

        db.commit()

        db.refresh(document)

        return document

    @staticmethod
    def store_chunks(
        db: Session,
        document_id: int,
        text: str,
    ) -> int:
        """
        Persist document chunks.
        """

        chunker = RecursiveChunker()

        chunks = chunker.chunk_text(text)

        for idx, chunk_text in enumerate(chunks):
            chunk = Chunk(
                document_id=document_id,
                content=chunk_text,
                chunk_index=idx,
            )

            db.add(chunk)

        db.commit()

        return len(chunks)
