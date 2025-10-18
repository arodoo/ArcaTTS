"""
Glossary management service.
Maintains term consistency across translation.
"""
from typing import Dict

from ..domain.models import GlossaryEntry
from ..domain.glossary_extractor import GlossaryExtractor


class GlossaryService:
    """Manage translation glossary."""

    def __init__(self):
        self.extractor = GlossaryExtractor()
        self.glossary: Dict[str, GlossaryEntry] = {}

    def update_from_chunk(
        self,
        original: str,
        translated: str
    ):
        """Extract and map terms from chunk pair."""
        orig_nouns = self.extractor.extract_proper_nouns(
            original
        )
        trans_nouns = self.extractor.extract_proper_nouns(
            translated
        )

        self._map_terms(
            list(orig_nouns),
            list(trans_nouns),
            original
        )

    def get_term_translation(
        self,
        source_term: str
    ) -> str:
        """Lookup consistent translation."""
        key = source_term.lower()
        if key in self.glossary:
            return self.glossary[key].target_term
        return source_term

    def _map_terms(
        self,
        source_terms: list[str],
        target_terms: list[str],
        context: str
    ):
        """Create term mappings."""
        for src, tgt in zip(source_terms, target_terms):
            key = src.lower()
            if key in self.glossary:
                self.glossary[key].increment_usage()
            else:
                self.glossary[key] = GlossaryEntry(
                    source_term=src,
                    target_term=tgt,
                    context=context[:100]
                )
