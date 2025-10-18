"""
Serialization helpers for cache repository.
Convert domain objects to/from JSON.
"""
from ..domain.translation import Translation
from ..domain.models import TranslationChunk, GlossaryEntry


class CacheSerializer:
    """Handle translation serialization."""

    @staticmethod
    def serialize(translation: Translation) -> dict:
        """Convert to JSON-serializable dict."""
        return {
            "translation_id": str(translation.translation_id),
            "original_text": translation.original_text,
            "language_pair": {
                "source": translation.language_pair.source,
                "target": translation.language_pair.target,
            },
            "chunks": [
                CacheSerializer._serialize_chunk(c)
                for c in translation.chunks
            ],
            "glossary": {
                k: CacheSerializer._serialize_glossary(v)
                for k, v in translation.glossary.items()
            },
            "created_at": translation.created_at.isoformat(),
            "completed_at": (
                translation.completed_at.isoformat()
                if translation.completed_at else None
            ),
            "final_translation": translation.final_translation,
        }

    @staticmethod
    def _serialize_chunk(chunk: TranslationChunk) -> dict:
        """Serialize chunk."""
        return {
            "chunk_id": str(chunk.chunk_id),
            "original_text": chunk.original_text,
            "translated_text": chunk.translated_text,
            "start_position": chunk.start_position,
            "end_position": chunk.end_position,
            "context_before": chunk.context_before,
            "context_after": chunk.context_after,
        }

    @staticmethod
    def _serialize_glossary(entry: GlossaryEntry) -> dict:
        """Serialize glossary entry."""
        return {
            "source_term": entry.source_term,
            "target_term": entry.target_term,
            "context": entry.context,
            "frequency": entry.frequency,
        }
