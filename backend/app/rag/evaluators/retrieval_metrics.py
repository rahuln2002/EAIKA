class RetrievalMetrics:
    """
    Retrieval analytics metrics.
    """

    @staticmethod
    def evaluate(
        retrieved_context: list[str],
    ) -> dict:
        """
        Compute retrieval metrics.
        """

        total_chunks = len(retrieved_context)

        avg_chunk_length = sum(len(chunk.split()) for chunk in retrieved_context) / max(
            total_chunks, 1
        )

        return {
            "retrieved_chunks": total_chunks,
            "avg_chunk_length": round(
                avg_chunk_length,
                2,
            ),
        }
