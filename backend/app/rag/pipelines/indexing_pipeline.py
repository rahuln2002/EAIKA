from app.rag.chunking.recursive_chunker import (
    RecursiveChunker,
)
from app.services.embeddings.embedding_manager import (
    EmbeddingManager,
)
from app.rag.vectorstore.vectorstore_manager import (
    VectorStoreManager,
)


class IndexingPipeline:
    """
    Document indexing pipeline.
    """

    def __init__(
        self,
        provider: str = "qdrant",
    ) -> None:
        self.chunker = RecursiveChunker()

        self.vectorstore = VectorStoreManager(provider=provider)

    def index_document(
        self,
        document_text: str,
    ) -> dict:
        """
        Index document into vector DB.
        """

        # =============================================
        # CHUNK DOCUMENT
        # =============================================

        chunks = self.chunker.chunk_text(document_text)

        # =============================================
        # GENERATE EMBEDDINGS
        # =============================================

        embeddings = EmbeddingManager.embed_texts(chunks)

        # =============================================
        # CREATE METADATA
        # =============================================

        metadata = []

        for idx, chunk in enumerate(chunks):
            metadata.append(
                {
                    "text": chunk,
                    "chunk_index": idx,
                }
            )

        # =============================================
        # STORE IN VECTOR DB
        # =============================================

        self.vectorstore.add_embeddings(
            embeddings,
            metadata,
        )

        return {
            "chunks_indexed": len(chunks),
        }
