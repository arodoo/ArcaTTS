"""
Main translation orchestration service.
Coordinates entire translation pipeline.
"""
from typing import Optional
from tqdm import tqdm

from ..domain.translation import Translation
from ..domain.value_objects import LanguagePair
from ..domain.translator import ITranslator
from ..domain.chunker import SemanticChunker
from ..domain.glossary_service import GlossaryService
from ..domain.post_processor import TranslationPostProcessor
from ..domain.validation_service import ValidationService
from .language_detector import LanguageDetector
from .chunk_translator import ChunkTranslator
from .chunk_merger import ChunkMerger


class TranslationService:
    """Orchestrate full translation workflow."""

    def __init__(self, translator: ITranslator):
        self.translator = translator
        self.chunker = SemanticChunker()
        self.glossary = GlossaryService()
        self.post_processor = TranslationPostProcessor()
        self.validator = ValidationService()
        self.language_detector = LanguageDetector()
        self.chunk_translator = ChunkTranslator(self)
        self.merger = ChunkMerger()

    def translate_text(
        self,
        text: str,
        target_language: str,
        source_language: Optional[str] = None
    ) -> Translation:
        """Execute complete translation pipeline."""
        source_lang = source_language or (
            self.language_detector.detect_language(text)
        )

        language_pair = LanguagePair(
            source=source_lang,
            target=target_language
        )

        translation = Translation(
            original_text=text,
            language_pair=language_pair
        )

        chunks = list(self.chunker.chunk_text(text))

        print(f"\nTranslating {len(chunks)} chunks...")

        for idx, chunk_data in enumerate(chunks, 1):
            percent = (idx / len(chunks)) * 100
            print(
                f"Progress: [{idx}/{len(chunks)}] "
                f"{percent:.1f}% complete",
                end="\r",
                flush=True
            )
            
            translated_chunk = (
                self.chunk_translator.translate_chunk(
                    chunk_data,
                    language_pair
                )
            )
            translation.add_chunk(translated_chunk)

            self.glossary.update_from_chunk(
                chunk_data["text"],
                translated_chunk.translated_text
            )

        print("\n\nMerging chunks...")
        merged = self.merger.merge_chunks(
            translation.chunks,
            text
        )
        final = self.merger.preserve_paragraph_breaks(
            text,
            merged
        )
        translation.finalize(final)

        return translation
