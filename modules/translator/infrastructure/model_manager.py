"""
Model loading and management helpers.
Continuation of MarianTranslatorAdapter.
"""
import torch
from transformers import MarianMTModel, MarianTokenizer

from ..domain.value_objects import LanguagePair


class ModelManager:
    """Handle model loading and caching."""

    MODEL_MAP = {
        "en-es": "Helsinki-NLP/opus-mt-en-es",
        "es-en": "Helsinki-NLP/opus-mt-es-en",
        "en-fr": "Helsinki-NLP/opus-mt-en-fr",
        "fr-en": "Helsinki-NLP/opus-mt-fr-en",
        "es-pt": "Helsinki-NLP/opus-mt-itc-itc",
        "pt-es": "Helsinki-NLP/opus-mt-itc-itc",
    }

    @staticmethod
    def get_model_name(language_pair: LanguagePair) -> str:
        """Get HuggingFace model name for pair."""
        key = f"{language_pair.source}-{language_pair.target}"
        if key not in ModelManager.MODEL_MAP:
            raise ValueError(
                f"Unsupported language pair: {key}"
            )
        return ModelManager.MODEL_MAP[key]

    @staticmethod
    def load_model(
        model_name: str,
        device: torch.device
    ) -> MarianMTModel:
        """Load model to device."""
        model = MarianMTModel.from_pretrained(model_name)
        return model.to(device)

    @staticmethod
    def load_tokenizer(model_name: str) -> MarianTokenizer:
        """Load tokenizer for model."""
        return MarianTokenizer.from_pretrained(model_name)

    @staticmethod
    def setup_device(use_gpu: bool) -> torch.device:
        """Configure compute device."""
        if use_gpu and torch.cuda.is_available():
            return torch.device("cuda")
        return torch.device("cpu")
