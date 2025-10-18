"""
Data Transfer Objects for translation.
"""
from dataclasses import dataclass
from typing import Optional
from uuid import UUID


@dataclass
class TranslationRequestDTO:
    """Request to translate text."""
    text: str
    target_language: str
    source_language: Optional[str] = None


@dataclass
class TranslationResponseDTO:
    """Translation result."""
    translation_id: UUID
    translated_text: str
    source_language: str
    target_language: str
    chunk_count: int
    glossary_size: int
    is_complete: bool


@dataclass
class ChunkDTO:
    """Chunk information."""
    chunk_id: UUID
    original_text: str
    translated_text: str
    validation_score: float
    is_valid: bool
