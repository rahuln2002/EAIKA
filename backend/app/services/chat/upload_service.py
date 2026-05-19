from sqlalchemy.orm import Session

from app.db.models.chunk import Chunk
from app.db.models.document import (
    Document,
)
from app.rag.chunking.recursive_chunker import (
    RecursiveChunker,
)
from app.rag.vectorstore.vectorstore_manager import (
    VectorStoreManager,
)
from app.services.embeddings.embedding_manager import (
    EmbeddingManager,
)


class UploadService:
    """
    Persistent upload + vector sync service.
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
        owner_id: int,
    ) -> int:
        """
        Persist chunks + sync embeddings.
        """

        chunker = RecursiveChunker()

        chunks = chunker.chunk_text(text)

        # =================================================
        # STORE CHUNKS IN POSTGRES
        # =================================================

        stored_chunks = []

        for idx, chunk_text in enumerate(chunks):
            chunk = Chunk(
                document_id=document_id,
                content=chunk_text,
                chunk_index=idx,
            )

            db.add(chunk)

            stored_chunks.append(chunk)

        db.commit()

        # =================================================
        # REFRESH TO GET IDS
        # =================================================

        for chunk in stored_chunks:
            db.refresh(chunk)

        # =================================================
        # GENERATE EMBEDDINGS
        # =================================================

        embeddings = EmbeddingManager.embed_texts(chunks)

        # =================================================
        # VECTOR METADATA
        # =================================================

        metadata = []

        for chunk in stored_chunks:
            metadata.append(
                {
                    "chunk_id": chunk.id,
                    "document_id": chunk.document_id,
                    "owner_id": owner_id,
                    "text": chunk.content,
                }
            )

        # =================================================
        # STORE IN VECTOR DB
        # =================================================

        vectorstore = VectorStoreManager(provider="qdrant")

        vectorstore.add_embeddings(
            embeddings=embeddings,
            metadata=metadata,
        )

        return len(chunks)
