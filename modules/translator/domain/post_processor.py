"""
Post-processing for translated text.
Preserves formatting, punctuation, numbers.
"""
import re

from .formatting import FormattingPreserver


class TranslationPostProcessor:
    """Clean and format translated text."""

    def __init__(self):
        self.formatter = FormattingPreserver()

    def process(
        self,
        original: str,
        translated: str
    ) -> str:
        """Apply all post-processing steps."""
        result = translated
        result = self._preserve_numbers(original, result)
        result = self._fix_punctuation(result)
        result = self.formatter.preserve_line_breaks(
            original,
            result
        )
        result = self.formatter.preserve_formatting(
            original,
            result
        )
        result = self.formatter.preserve_whitespace(
            original,
            result
        )
        return result.strip()

    def _preserve_numbers(
        self,
        original: str,
        translated: str
    ) -> str:
        """Ensure numbers match original."""
        orig_nums = re.findall(r'\b\d+(?:[.,]\d+)?\b', original)
        trans_nums = re.findall(
            r'\b\d+(?:[.,]\d+)?\b',
            translated
        )

        if len(orig_nums) == len(trans_nums):
            for orig_num, trans_num in zip(
                orig_nums, trans_nums
            ):
                translated = translated.replace(
                    trans_num,
                    orig_num,
                    1
                )

        return translated

    def _fix_punctuation(self, text: str) -> str:
        """Clean spacing around punctuation."""
        text = re.sub(r'\s+([.,;:!?])', r'\1', text)
        text = re.sub(r'([.,;:!?])([^\s])', r'\1 \2', text)
        return text
