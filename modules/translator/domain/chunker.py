"""
Semantic text chunker for translation.
Splits text intelligently preserving context.
"""
import re
from typing import Iterator

from .splitter import SentenceSplitter
from .context import ContextExtractor


class SemanticChunker:
    """Split text maintaining narrative coherence."""

    def __init__(
        self,
        max_tokens: int = 100,
        context_sentences: int = 2
    ):
        self.max_tokens = max_tokens
        self.splitter = SentenceSplitter()
        self.context = ContextExtractor(context_sentences)

    def chunk_text(self, text: str) -> Iterator[dict]:
        """Split text into contextual chunks."""
        paragraphs = self._split_paragraphs(text)
        current_pos = 0

        for para_idx, paragraph in enumerate(paragraphs):
            sentences = self.splitter.split_sentences(
                paragraph
            )

            for chunk_sentences in self.splitter.group_sentences(
                sentences,
                self.max_tokens
            ):
                first_sentence_start = text.find(
                    chunk_sentences[0],
                    current_pos
                )
                
                if first_sentence_start == -1:
                    first_sentence_start = current_pos
                
                last_sentence = chunk_sentences[-1]
                last_sentence_end = text.find(
                    last_sentence,
                    first_sentence_start
                )
                
                if last_sentence_end == -1:
                    last_sentence_end = first_sentence_start
                else:
                    last_sentence_end += len(last_sentence)
                
                start = first_sentence_start
                end = last_sentence_end
                chunk_text = text[start:end]

                yield {
                    "text": chunk_text,
                    "start": start,
                    "end": end,
                    "context_before": self.context.get_context_before(
                        paragraphs, para_idx
                    ),
                    "context_after": self.context.get_context_after(
                        paragraphs, para_idx
                    ),
                }

                current_pos = end

    def _split_paragraphs(self, text: str) -> list[str]:
        """Split by double newline or clear breaks."""
        return [
            p.strip()
            for p in re.split(r'\n\s*\n', text)
            if p.strip()
        ]
