from app.services.embeddings.embedding_service import (
    EmbeddingService,
)
from app.utils.tokenizer import (
    truncate_tokens,
)


class EmbeddingManager:
    """
    High-level embedding manager.
    """

    MAX_EMBEDDING_TOKENS = 512

    @classmethod
    def embed_text(
        cls,
        text: str,
    ) -> list[float]:
        """
        Generate embedding safely.
        """

        cleaned_text = truncate_tokens(
            text,
            cls.MAX_EMBEDDING_TOKENS,
        )

        return EmbeddingService.generate_embedding(cleaned_text)

    @classmethod
    def embed_texts(
        cls,
        texts: list[str],
    ) -> list[list[float]]:
        """
        Generate embeddings for multiple texts.
        """

        processed_texts = [
            truncate_tokens(
                text,
                cls.MAX_EMBEDDING_TOKENS,
            )
            for text in texts
        ]

        return EmbeddingService.generate_embeddings(processed_texts)
