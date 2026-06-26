from sqlalchemy.orm import Session

from app.cache.cache_manager import CacheManager
from app.core.constants.cache_constants import (
    UPLOAD_PREFIX,
    UPLOAD_TTL,
)
from app.db.models.chunk import Chunk
from app.db.models.document import Document
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
    Persistent upload + vector synchronization service.
    """

    @staticmethod
    def _update_progress(
        document_id: int,
        status: str,
        progress: int,
    ) -> None:
        """
        Store upload progress in Redis.
        """

        CacheManager.set(
            key=f"{UPLOAD_PREFIX}:{document_id}",
            value={
                "status": status,
                "progress": progress,
            },
            expire=UPLOAD_TTL,
        )

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

        UploadService._update_progress(
            document.id,
            "created",
            5,
        )

        return document

    @staticmethod
    def store_chunks(
        db: Session,
        document_id: int,
        text: str,
        owner_id: int,
    ) -> int:
        """
        Persist chunks and synchronize embeddings.
        """

        UploadService._update_progress(
            document_id,
            "chunking",
            15,
        )

        chunker = RecursiveChunker()

        chunks = chunker.chunk_text(
            text,
        )

        stored_chunks = []

        UploadService._update_progress(
            document_id,
            "saving_chunks",
            35,
        )

        for index, chunk_text in enumerate(chunks):
            chunk = Chunk(
                document_id=document_id,
                content=chunk_text,
                chunk_index=index,
            )

            db.add(chunk)

            stored_chunks.append(chunk)

        db.commit()

        for chunk in stored_chunks:
            db.refresh(chunk)

        UploadService._update_progress(
            document_id,
            "generating_embeddings",
            60,
        )

        embeddings = EmbeddingManager.embed_texts(
            chunks,
        )

        metadata = [
            {
                "chunk_id": chunk.id,
                "document_id": chunk.document_id,
                "owner_id": owner_id,
                "text": chunk.content,
            }
            for chunk in stored_chunks
        ]

        UploadService._update_progress(
            document_id,
            "indexing_vectors",
            85,
        )

        vectorstore = VectorStoreManager(
            provider="qdrant",
        )

        vectorstore.add_embeddings(
            embeddings=embeddings,
            metadata=metadata,
        )

        UploadService._update_progress(
            document_id,
            "completed",
            100,
        )

        return len(chunks)
