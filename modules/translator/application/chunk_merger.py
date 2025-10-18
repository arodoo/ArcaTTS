"""
Chunk merging and finalization logic.
Assembles final translated text.
"""


class ChunkMerger:
    """Merge translated chunks into final text."""

    @staticmethod
    def merge_chunks(chunks: list, original_text: str = "") -> str:
        """Combine chunks preserving original structure."""
        if not chunks:
            return ""

        sorted_chunks = sorted(
            chunks,
            key=lambda c: c.start_position
        )

        if not original_text:
            return "\n\n".join(
                c.translated_text for c in sorted_chunks
            )

        result = []
        last_end = 0

        for chunk in sorted_chunks:
            gap = original_text[last_end:chunk.start_position]
            result.append(gap)
            result.append(chunk.translated_text)
            last_end = chunk.end_position

        final_gap = original_text[last_end:]
        result.append(final_gap)

        return "".join(result)

    @staticmethod
    def preserve_paragraph_breaks(
        original: str,
        merged: str
    ) -> str:
        """Restore paragraph structure."""
        return merged
