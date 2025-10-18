"""
Translation aggregate root.
Manages entire translation lifecycle.
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from .models import TranslationChunk, GlossaryEntry
from .value_objects import LanguagePair, ValidationScore


@dataclass
class Translation:
    """Complete translation entity."""
    original_text: str
    language_pair: LanguagePair
    translation_id: UUID = field(default_factory=uuid4)
    chunks: list[TranslationChunk] = field(default_factory=list)
    glossary: dict[str, GlossaryEntry] = field(
        default_factory=dict
    )
    created_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
    final_translation: str = ""

    def add_chunk(self, chunk: TranslationChunk):
        """Add translated chunk."""
        self.chunks.append(chunk)

    def add_glossary_entry(self, entry: GlossaryEntry):
        """Add or update glossary term."""
        key = entry.source_term.lower()
        if key in self.glossary:
            self.glossary[key].increment_usage()
        else:
            self.glossary[key] = entry

    def finalize(self, merged_text: str):
        """Mark translation as complete."""
        self.final_translation = merged_text
        self.completed_at = datetime.now()

    @property
    def is_complete(self) -> bool:
        """Check if translation finished."""
        return self.completed_at is not None
