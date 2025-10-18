"""
Mappers between domain and DTOs.
"""
from ..domain.translation import Translation
from ..domain.models import TranslationChunk
from .dtos import (
    TranslationResponseDTO,
    ChunkDTO,
    TranslationRequestDTO
)


class TranslationMapper:
    """Map Translation to DTO."""

    @staticmethod
    def to_response_dto(
        translation: Translation
    ) -> TranslationResponseDTO:
        """Convert to response DTO."""
        return TranslationResponseDTO(
            translation_id=translation.translation_id,
            translated_text=translation.final_translation,
            source_language=translation.language_pair.source,
            target_language=translation.language_pair.target,
            chunk_count=len(translation.chunks),
            glossary_size=len(translation.glossary),
            is_complete=translation.is_complete
        )


class ChunkMapper:
    """Map TranslationChunk to DTO."""

    @staticmethod
    def to_dto(chunk: TranslationChunk) -> ChunkDTO:
        """Convert to DTO."""
        return ChunkDTO(
            chunk_id=chunk.chunk_id,
            original_text=chunk.original_text,
            translated_text=chunk.translated_text,
            validation_score=(
                chunk.validation.score
                if chunk.validation else 0.0
            ),
            is_valid=(
                chunk.validation.is_valid
                if chunk.validation else False
            )
        )
