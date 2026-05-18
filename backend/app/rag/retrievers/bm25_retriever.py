from rank_bm25 import BM25Okapi


class BM25Retriever:
    """
    BM25 lexical retriever.
    """

    def __init__(
        self,
        documents: list[str],
    ) -> None:
        self.documents = documents

        self.tokenized_docs = [doc.lower().split() for doc in documents]

        self.bm25 = BM25Okapi(self.tokenized_docs)

    def retrieve(
        self,
        query: str,
        top_k: int = 10,
    ) -> list[str]:
        """
        Retrieve BM25-ranked documents.
        """

        tokenized_query = query.lower().split()

        scores = self.bm25.get_scores(tokenized_query)

        ranked_results = sorted(
            zip(self.documents, scores),
            key=lambda x: x[1],
            reverse=True,
        )

        return [doc for doc, _ in ranked_results[:top_k]]
