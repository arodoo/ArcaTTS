"""
Batch processing and model management.
Extension methods for MarianTranslatorAdapter.
"""
import torch

from ..domain.value_objects import LanguagePair
from .model_manager import ModelManager
from .translation_utils import TranslationUtils


class BatchProcessor:
    """Handle batch translation operations."""

    def __init__(self, adapter):
        self.adapter = adapter
        self.utils = TranslationUtils()

    def translate_batch(
        self,
        texts: list[str],
        language_pair: LanguagePair
    ) -> list[str]:
        """Translate multiple texts in batches."""
        model_key = self.utils.get_model_key(language_pair)
        self.adapter._ensure_model_loaded(
            model_key,
            language_pair
        )

        batches = self.utils.batch_texts(texts)
        translations = []

        for batch in batches:
            batch_result = self._translate_batch_internal(
                batch,
                model_key
            )
            translations.extend(batch_result)

        return translations

    def _translate_batch_internal(
        self,
        texts: list[str],
        model_key: str
    ) -> list[str]:
        """Process single batch."""
        tokenizer = self.adapter.tokenizers[model_key]
        model = self.adapter.models[model_key]

        inputs = tokenizer(
            texts,
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=512
        ).to(self.adapter.device)

        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_length=512,
                num_beams=5,
                early_stopping=True
            )

        return [
            tokenizer.decode(out, skip_special_tokens=True)
            for out in outputs
        ]
