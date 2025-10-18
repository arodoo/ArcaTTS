"""
Translator interface for domain layer.
Abstraction for translation implementations.
"""
from abc import ABC, abstractmethod
from typing import Optional

from .value_objects import LanguagePair


class ITranslator(ABC):
    """Translation service contract."""

    @abstractmethod
    def translate(
        self,
        text: str,
        language_pair: LanguagePair,
        context: Optional[str] = None
    ) -> str:
        """Translate text with optional context."""
        pass

    @abstractmethod
    def translate_batch(
        self,
        texts: list[str],
        language_pair: LanguagePair
    ) -> list[str]:
        """Translate multiple texts efficiently."""
        pass

    @abstractmethod
    def is_model_loaded(
        self,
        language_pair: LanguagePair
    ) -> bool:
        """Check if model for pair is loaded."""
        pass
