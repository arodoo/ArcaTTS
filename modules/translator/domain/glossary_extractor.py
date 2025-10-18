"""
Glossary extraction service.
Identifies and tracks consistent terminology.
"""
import re
from typing import Set

from ..domain.models import GlossaryEntry


class GlossaryExtractor:
    """Extract terms for consistent translation."""

    PROPER_NOUN_PATTERN = re.compile(
        r'\b[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)*\b'
    )
    QUOTED_PATTERN = re.compile(r'[«"]([^»"]+)[»"]')

    def extract_proper_nouns(self, text: str) -> Set[str]:
        """Find capitalized names and places."""
        matches = self.PROPER_NOUN_PATTERN.findall(text)
        return {
            match for match in matches
            if len(match) > 2 and not self._is_sentence_start(
                text, match
            )
        }

    def extract_quoted_terms(self, text: str) -> Set[str]:
        """Find terms in quotes (technical/emphasis)."""
        return set(self.QUOTED_PATTERN.findall(text))

    def extract_numbers(self, text: str) -> Set[str]:
        """Find numbers for validation."""
        number_pattern = re.compile(r'\b\d+(?:[.,]\d+)?\b')
        return set(number_pattern.findall(text))

    def _is_sentence_start(
        self,
        text: str,
        word: str
    ) -> bool:
        """Check if word starts sentence."""
        pattern = re.compile(
            rf'(?:^|[.!?]\s+)({re.escape(word)})\b'
        )
        return bool(pattern.search(text))
