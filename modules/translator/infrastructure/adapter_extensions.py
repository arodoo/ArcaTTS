"""
Adapter extensions for model loading.
Completes MarianTranslatorAdapter implementation.
"""
from ..domain.value_objects import LanguagePair
from .model_manager import ModelManager
from .batch_processor import BatchProcessor


class AdapterExtensions:
    """Additional methods for adapter."""

    @staticmethod
    def ensure_model_loaded(
        adapter,
        model_key: str,
        language_pair: LanguagePair
    ):
        """Load model if not in cache."""
        if model_key in adapter.models:
            return

        model_name = ModelManager.get_model_name(
            language_pair
        )
        adapter.models[model_key] = ModelManager.load_model(
            model_name,
            adapter.device
        )
        adapter.tokenizers[model_key] = (
            ModelManager.load_tokenizer(model_name)
        )

    @staticmethod
    def is_model_loaded(
        adapter,
        language_pair: LanguagePair
    ) -> bool:
        """Check if model loaded in cache."""
        from .translation_utils import TranslationUtils
        model_key = TranslationUtils.get_model_key(
            language_pair
        )
        return model_key in adapter.models
