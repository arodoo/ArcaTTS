"""Test name protection in translation."""
from modules.translator.infrastructure.m2m100_adapter import (
    M2M100Adapter
)
from modules.translator.application.translation_service import (
    TranslationService
)

# Small test
text = "FRANZ KAFKA"

translator = M2M100Adapter(use_gpu=False, model_size="418M")
service = TranslationService(translator)

translation = service.translate_text(
    text,
    target_language="pt",
    source_language="es"
)

print(f"Original: {text}")
print(f"Translated: {translation.final_translation}")
print(f"Should preserve: FRANZ KAFKA")
