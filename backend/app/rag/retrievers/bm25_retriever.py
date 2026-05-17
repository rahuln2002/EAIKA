from rank_bm25 import BM25Okapi


class BM25Retriever:
    """
    BM25 keyword retriever.
    """

    def __init__(
        self,
        documents: list[str],
    ) -> None:
        self.documents = documents

        # =============================================
        # HANDLE EMPTY CORPUS
        # =============================================

        if not documents:
            self.bm25 = None
            self.tokenized_documents = []
            return

        self.tokenized_documents = [doc.split() for doc in documents]

        self.bm25 = BM25Okapi(self.tokenized_documents)

    def retrieve(
        self,
        query: str,
        top_k: int = 5,
    ):
        """
        Perform BM25 retrieval.
        """

        # =============================================
        # HANDLE EMPTY INDEX
        # =============================================

        if self.bm25 is None:
            return []

        tokenized_query = query.split()

        scores = self.bm25.get_scores(tokenized_query)

        ranked_results = sorted(
            zip(
                self.documents,
                scores,
            ),
            key=lambda x: x[1],
            reverse=True,
        )

        return ranked_results[:top_k]
