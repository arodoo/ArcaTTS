"""Test translation of large chunk."""
from modules.translator.domain.chunker import SemanticChunker
from modules.translator.infrastructure.m2m100_adapter import (
    M2M100Adapter
)
from modules.translator.domain.value_objects import LanguagePair

# Read file
with open("boocks/america_small.txt", encoding="utf-8") as f:
    text = f.read()

# Get chunk 7 (large one)
chunker = SemanticChunker(max_tokens=512)
chunks = list(chunker.chunk_text(text))
chunk = chunks[6]  # Chunk 7 (index 6)

print(f"Testing large chunk (chunk 7)")
print(f"Original: {len(chunk['text'])} chars")
print("="*60)

# Translate
translator = M2M100Adapter(use_gpu=False, model_size="418M")
pair = LanguagePair(source="es", target="pt")

translated = translator.translate(chunk["text"], pair)

print(f"Translated: {len(translated)} chars")
print("="*60)

# Check for repetition
lines = translated.split("\n")
print(f"Lines in translation: {len(lines)}")

# Save to files for comparison
with open("boocks/chunk7_original.txt", "w", encoding="utf-8") as f:
    f.write(chunk["text"])

with open("boocks/chunk7_translated.txt", "w", encoding="utf-8") as f:
    f.write(translated)

print("\nSaved to boocks/chunk7_original.txt and boocks/chunk7_translated.txt")
print("Check if translation has duplications")
