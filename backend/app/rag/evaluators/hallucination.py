class HallucinationEvaluator:
    """
    Detect hallucinated content.
    """

    @staticmethod
    def evaluate(
        answer: str,
        retrieved_context: list[str],
    ) -> dict:
        """
        Simple hallucination detection.
        """

        context = " ".join(retrieved_context).lower()

        answer_words = answer.lower().split()

        hallucinated_terms = [word for word in answer_words if word not in context]

        hallucination_ratio = len(hallucinated_terms) / max(len(answer_words), 1)

        return {
            "hallucination_score": round(
                hallucination_ratio,
                3,
            ),
            "hallucinated_terms": hallucinated_terms[:20],
        }
