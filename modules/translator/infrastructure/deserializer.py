"""
Deserialization helpers for cache.
Reconstruct domain objects from JSON.
"""
from uuid import UUID
from datetime import datetime

from ..domain.translation import Translation
from ..domain.value_objects import LanguagePair
from ..domain.models import TranslationChunk, GlossaryEntry


class CacheDeserializer:
    """Reconstruct translations from data."""

    @staticmethod
    def deserialize(data: dict) -> Translation:
        """Rebuild Translation from dict."""
        lang_pair = LanguagePair(
            source=data["language_pair"]["source"],
            target=data["language_pair"]["target"]
        )

        translation = Translation(
            original_text=data["original_text"],
            language_pair=lang_pair,
            translation_id=UUID(data["translation_id"]),
            created_at=datetime.fromisoformat(
                data["created_at"]
            )
        )

        for chunk_data in data["chunks"]:
            chunk = CacheDeserializer._deserialize_chunk(
                chunk_data
            )
            translation.chunks.append(chunk)

        for key, gloss_data in data["glossary"].items():
            entry = CacheDeserializer._deserialize_glossary(
                gloss_data
            )
            translation.glossary[key] = entry

        if data["completed_at"]:
            translation.completed_at = datetime.fromisoformat(
                data["completed_at"]
            )
            translation.final_translation = (
                data["final_translation"]
            )

        return translation

    @staticmethod
    def _deserialize_chunk(data: dict) -> TranslationChunk:
        """Rebuild chunk."""
        return TranslationChunk(
            chunk_id=UUID(data["chunk_id"]),
            original_text=data["original_text"],
            translated_text=data["translated_text"],
            start_position=data["start_position"],
            end_position=data["end_position"],
            context_before=data["context_before"],
            context_after=data["context_after"],
        )

    @staticmethod
    def _deserialize_glossary(data: dict) -> GlossaryEntry:
        """Rebuild glossary entry."""
        return GlossaryEntry(
            source_term=data["source_term"],
            target_term=data["target_term"],
            context=data["context"],
            frequency=data["frequency"],
        )
