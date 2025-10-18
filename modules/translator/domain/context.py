"""
Context extraction for chunks.
Provides surrounding text for better translation.
"""


class ContextExtractor:
    """Extract context around chunks."""

    def __init__(self, context_sentences: int = 2):
        self.context_sentences = context_sentences

    def get_context_before(
        self,
        paragraphs: list[str],
        current_idx: int
    ) -> str:
        """Get previous paragraphs as context."""
        start = max(0, current_idx - self.context_sentences)
        context_paras = paragraphs[start:current_idx]
        return " ".join(context_paras)

    def get_context_after(
        self,
        paragraphs: list[str],
        current_idx: int
    ) -> str:
        """Get following paragraphs as context."""
        end = min(
            len(paragraphs),
            current_idx + self.context_sentences + 1
        )
        context_paras = paragraphs[current_idx + 1:end]
        return " ".join(context_paras)
