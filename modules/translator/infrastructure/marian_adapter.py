"""
MarianMT translator adapter.
Implements ITranslator using Helsinki-NLP models.
"""
from typing import Optional
import torch
from transformers import MarianMTModel, MarianTokenizer

from ..domain.translator import ITranslator
from ..domain.value_objects import LanguagePair
from .model_manager import ModelManager
from .translation_utils import TranslationUtils
from .batch_processor import BatchProcessor
from .adapter_extensions import AdapterExtensions
from .language_prefix import LanguagePrefixHandler


class MarianTranslatorAdapter(ITranslator):
    """MarianMT implementation with quality focus."""

    def __init__(self, use_gpu: bool = True):
        self.device = ModelManager.setup_device(use_gpu)
        self.models: dict[str, MarianMTModel] = {}
        self.tokenizers: dict[str, MarianTokenizer] = {}
        self.utils = TranslationUtils()
        self.batch_proc = BatchProcessor(self)

    def translate(
        self,
        text: str,
        language_pair: LanguagePair,
        context: Optional[str] = None
    ) -> str:
        """Translate with context awareness."""
        model_key = self.utils.get_model_key(language_pair)
        self._ensure_model_loaded(model_key, language_pair)

        input_text = self.utils.prepare_input(text, context)
        tokenizer = self.tokenizers[model_key]
        model = self.models[model_key]

        model_name = ModelManager.get_model_name(language_pair)
        prefixed_text = LanguagePrefixHandler.add_prefix(
            input_text,
            language_pair,
            model_name
        )

        inputs = tokenizer(
            prefixed_text,
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=512
        ).to(self.device)

        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_length=512,
                num_beams=5,
                no_repeat_ngram_size=3,
                repetition_penalty=1.2,
                early_stopping=True
            )

        translation = tokenizer.decode(
            outputs[0],
            skip_special_tokens=True
        )
        return translation.strip()

    def translate_batch(
        self,
        texts: list[str],
        language_pair: LanguagePair
    ) -> list[str]:
        """Delegate to batch processor."""
        return self.batch_proc.translate_batch(
            texts,
            language_pair
        )

    def is_model_loaded(
        self,
        language_pair: LanguagePair
    ) -> bool:
        """Check model cache."""
        return AdapterExtensions.is_model_loaded(
            self,
            language_pair
        )

    def _ensure_model_loaded(
        self,
        model_key: str,
        language_pair: LanguagePair
    ):
        """Load model if needed."""
        AdapterExtensions.ensure_model_loaded(
            self,
            model_key,
            language_pair
        )
