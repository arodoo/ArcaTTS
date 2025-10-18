"""
M2M-100 translator adapter.
Facebook's multilingual translation model.
More robust than MarianMT for long texts.
"""
from typing import Optional
import torch
from transformers import M2M100ForConditionalGeneration
from transformers import M2M100Tokenizer

from ..domain.translator import ITranslator
from ..domain.value_objects import LanguagePair


class M2M100Adapter(ITranslator):
    """M2M-100 implementation for production use."""

    LANG_CODE_MAP = {
        "es": "es",
        "pt": "pt",
        "en": "en",
        "fr": "fr",
        "de": "de",
    }

    def __init__(
        self,
        use_gpu: bool = True,
        model_size: str = "418M"
    ):
        """Initialize with model size: 418M or 1.2B."""
        self.device = self._setup_device(use_gpu)
        
        model_name = f"facebook/m2m100_{model_size}"
        print(f"\n[1/3] Loading {model_name}...")
        print("      (First time: downloading ~2GB model)")
        print("      This may take 5-10 minutes...\n")
        
        print("[2/3] Loading tokenizer...", end="", flush=True)
        self.tokenizer = M2M100Tokenizer.from_pretrained(
            model_name
        )
        print(" OK")
        
        print("[3/3] Loading model to device...", end="", flush=True)
        self.model = M2M100ForConditionalGeneration\
            .from_pretrained(model_name).to(self.device)
        print(" OK")
        
        print(f"\n[OK] Model ready on {self.device}\n")

    def translate(
        self,
        text: str,
        language_pair: LanguagePair,
        context: Optional[str] = None
    ) -> str:
        """Translate with M2M-100."""
        source_lang = self._get_lang_code(
            language_pair.source
        )
        target_lang = self._get_lang_code(
            language_pair.target
        )

        self.tokenizer.src_lang = source_lang

        encoded = self.tokenizer(
            text,
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=1024
        ).to(self.device)

        # Dynamic max_length based on input
        input_length = encoded.input_ids.shape[1]
        dynamic_max_length = min(
            int(input_length * 2.0),  # Allow 2x expansion
            1024
        )

        generated = self.model.generate(
            **encoded,
            forced_bos_token_id=self.tokenizer.get_lang_id(
                target_lang
            ),
            max_length=dynamic_max_length,
            min_length=max(10, int(input_length * 0.5)),
            num_beams=5,
            no_repeat_ngram_size=3,
            repetition_penalty=1.2,
            early_stopping=True
        )

        translation = self.tokenizer.batch_decode(
            generated,
            skip_special_tokens=True
        )[0]

        return translation.strip()

    def translate_batch(
        self,
        texts: list[str],
        language_pair: LanguagePair
    ) -> list[str]:
        """Batch translation."""
        return [
            self.translate(text, language_pair)
            for text in texts
        ]

    def is_model_loaded(
        self,
        language_pair: LanguagePair
    ) -> bool:
        """Check if model is loaded."""
        return self.model is not None

    def _get_lang_code(self, lang: str) -> str:
        """Map language code to M2M-100 format."""
        if lang not in self.LANG_CODE_MAP:
            raise ValueError(f"Unsupported language: {lang}")
        return self.LANG_CODE_MAP[lang]

    @staticmethod
    def _setup_device(use_gpu: bool) -> torch.device:
        """Configure device."""
        if use_gpu and torch.cuda.is_available():
            return torch.device("cuda")
        return torch.device("cpu")
