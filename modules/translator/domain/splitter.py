"""
Sentence splitting and grouping logic.
Continuation of SemanticChunker.
"""
import re
from typing import Iterator


class SentenceSplitter:
    """Handle sentence-level operations."""

    SENTENCE_END = re.compile(
        r'(?<=[.!?…])\s+(?=[A-ZÁÉÍÓÚÑa-z«"])'
    )
    DIALOGUE_START = re.compile(r'^[—\-«"\'"]')

    def split_sentences(self, paragraph: str) -> list[str]:
        """Split paragraph into sentences."""
        sentences = self.SENTENCE_END.split(paragraph)
        return [s.strip() for s in sentences if s.strip()]

    def estimate_tokens(self, text: str) -> int:
        """Rough token count (words * 1.3)."""
        words = len(text.split())
        return int(words * 1.3)

    def is_dialogue(self, sentence: str) -> bool:
        """Check if sentence is dialogue."""
        return bool(self.DIALOGUE_START.match(sentence))

    def group_sentences(
        self,
        sentences: list[str],
        max_tokens: int
    ) -> Iterator[list[str]]:
        """Group sentences within token limit."""
        current_group = []
        current_tokens = 0

        for sentence in sentences:
            tokens = self.estimate_tokens(sentence)

            if current_tokens + tokens > max_tokens:
                if current_group:
                    yield current_group
                current_group = [sentence]
                current_tokens = tokens
            else:
                current_group.append(sentence)
                current_tokens += tokens

        if current_group:
            yield current_group
