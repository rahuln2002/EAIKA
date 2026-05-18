class FaithfulnessEvaluator:
    """
    Evaluates grounding faithfulness.
    """

    @staticmethod
    def evaluate(
        answer: str,
        retrieved_context: list[str],
    ) -> dict:
        """
        Basic faithfulness evaluation.
        """

        context_text = " ".join(retrieved_context).lower()

        answer_words = answer.lower().split()

        matched_words = [word for word in answer_words if word in context_text]

        score = len(matched_words) / max(len(answer_words), 1)

        return {
            "faithfulness_score": round(
                score,
                3,
            ),
            "matched_terms": len(matched_words),
            "total_terms": len(answer_words),
        }
