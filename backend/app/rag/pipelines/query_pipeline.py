class QueryPipeline:
    """
    Query preprocessing pipeline.
    """

    @staticmethod
    def process_query(
        query: str,
    ) -> str:
        """
        Clean and normalize query.
        """

        processed_query = query.strip()

        return processed_query
