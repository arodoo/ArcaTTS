"""
Batch translation and utilities.
Extension for MarianTranslatorAdapter.
"""
from typing import Optional

from ..domain.value_objects import LanguagePair


class TranslationUtils:
    """Helper methods for translation."""

    @staticmethod
    def prepare_input(
        text: str,
        context: Optional[str]
    ) -> str:
        """Combine text with context if provided."""
        if context:
            return f"{context} {text}"
        return text

    @staticmethod
    def get_model_key(language_pair: LanguagePair) -> str:
        """Generate cache key for model."""
        return f"{language_pair.source}-{language_pair.target}"

    @staticmethod
    def batch_texts(
        texts: list[str],
        batch_size: int = 8
    ) -> list[list[str]]:
        """Split texts into batches."""
        return [
            texts[i:i + batch_size]
            for i in range(0, len(texts), batch_size)
        ]
