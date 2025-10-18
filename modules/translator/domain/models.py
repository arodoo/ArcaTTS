"""
Core domain entities for translation.
Mutable entities with identity.
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from .value_objects import LanguagePair, ValidationScore


@dataclass
class TranslationChunk:
    """Single translation segment with context."""
    original_text: str
    translated_text: str
    start_position: int
    end_position: int
    context_before: str = ""
    context_after: str = ""
    chunk_id: UUID = field(default_factory=uuid4)
    validation: Optional[ValidationScore] = None

    def mark_validated(self, score: ValidationScore):
        """Mark chunk as validated."""
        self.validation = score


@dataclass
class GlossaryEntry:
    """Consistent term mapping."""
    source_term: str
    target_term: str
    context: str = ""
    frequency: int = 1

    def increment_usage(self):
        """Track term usage."""
        self.frequency += 1
