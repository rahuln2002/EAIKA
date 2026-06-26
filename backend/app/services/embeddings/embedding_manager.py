import hashlib

from app.cache.cache_manager import CacheManager
from app.core.constants.cache_constants import (
    EMBEDDING_PREFIX,
    EMBEDDING_TTL,
)
from app.services.embeddings.embedding_service import (
    EmbeddingService,
)
from app.utils.tokenizer import (
    truncate_tokens,
)


class EmbeddingManager:
    """
    High-level embedding manager with Redis caching.
    """

    MAX_EMBEDDING_TOKENS = 512

    @staticmethod
    def _cache_key(
        text: str,
    ) -> str:
        """
        Generate deterministic cache key.
        """

        text_hash = hashlib.sha256(
            text.encode("utf-8"),
        ).hexdigest()

        return f"{EMBEDDING_PREFIX}:{text_hash}"

    @classmethod
    def embed_text(
        cls,
        text: str,
    ) -> list[float]:
        """
        Generate a single embedding with Redis caching.
        """

        cleaned_text = truncate_tokens(
            text,
            cls.MAX_EMBEDDING_TOKENS,
        )

        cache_key = cls._cache_key(
            cleaned_text,
        )

        cached_embedding = CacheManager.get(
            cache_key,
        )

        if cached_embedding is not None:
            return cached_embedding

        embedding = EmbeddingService.generate_query_embedding(
            cleaned_text,
        )

        CacheManager.set(
            cache_key,
            embedding,
            expire=EMBEDDING_TTL,
        )

        return embedding

    @classmethod
    def embed_texts(
        cls,
        texts: list[str],
    ) -> list[list[float]]:
        """
        Generate embeddings for multiple texts with Redis caching.
        """

        processed_texts = [
            truncate_tokens(
                text,
                cls.MAX_EMBEDDING_TOKENS,
            )
            for text in texts
        ]

        embeddings: list[list[float]] = [[] for _ in processed_texts]

        uncached_texts: list[str] = []
        uncached_indices: list[int] = []

        for index, text in enumerate(
            processed_texts,
        ):
            cache_key = cls._cache_key(
                text,
            )

            cached_embedding = CacheManager.get(
                cache_key,
            )

            if cached_embedding is not None:
                embeddings[index] = cached_embedding

            else:
                uncached_texts.append(
                    text,
                )

                uncached_indices.append(
                    index,
                )

        if uncached_texts:
            generated_embeddings = EmbeddingService.generate_embeddings(
                uncached_texts,
            )

            for index, embedding in zip(
                uncached_indices,
                generated_embeddings,
            ):
                cache_key = cls._cache_key(
                    processed_texts[index],
                )

                CacheManager.set(
                    cache_key,
                    embedding,
                    expire=EMBEDDING_TTL,
                )

                embeddings[index] = embedding

        return embeddings
