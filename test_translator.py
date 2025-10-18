"""Test translator independently."""
from modules.translator.infrastructure.m2m100_adapter import (
    M2M100Adapter
)
from modules.translator.domain.value_objects import LanguagePair

# Create translator
translator = M2M100Adapter(use_gpu=False, model_size="418M")
pair = LanguagePair(source="es", target="pt")

# Test texts
test_texts = [
    "FRANZ KAFKA",
    "Cuando Karl Rossmann entró en el puerto de Nueva York.",
    "El barco ya había aminorado su marcha.",
]

print("Testing translator:")
print("="*60)

for text in test_texts:
    translation = translator.translate(text, pair)
    print(f"ES: {text}")
    print(f"PT: {translation}")
    print()
