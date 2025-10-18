"""
Chunk translation and merging helpers.
Extension for TranslationService.
"""
from ..domain.models import TranslationChunk
from ..domain.value_objects import LanguagePair
from ..domain.proper_name_protector import ProperNameProtector


class ChunkTranslator:
    """Handle individual chunk translation."""

    def __init__(self, service):
        self.service = service
        self.name_protector = ProperNameProtector()

    def translate_chunk(
        self,
        chunk_data: dict,
        language_pair: LanguagePair
    ) -> TranslationChunk:
        """Translate single chunk with validation."""
        original_text = chunk_data["text"]
        
        raw_translation = self.service.translator.translate(
            original_text,
            language_pair,
            context=chunk_data.get("context_before")
        )
        
        restored_translation = (
            self.name_protector.restore_names(
                original_text,
                raw_translation
            )
        )

        processed = self.service.post_processor.process(
            original_text,
            restored_translation
        )

        validation = self.service.validator.validate(
            original_text,
            processed
        )

        chunk = TranslationChunk(
            original_text=original_text,
            translated_text=processed,
            start_position=chunk_data["start"],
            end_position=chunk_data["end"],
            context_before=chunk_data.get("context_before", ""),
            context_after=chunk_data.get("context_after", "")
        )

        chunk.mark_validated(validation)
        return chunk
