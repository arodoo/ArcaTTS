"""Test full translation of first 2 chunks."""
from modules.translator.domain.chunker import SemanticChunker
from modules.translator.infrastructure.m2m100_adapter import (
    M2M100Adapter
)
from modules.translator.domain.value_objects import LanguagePair

# Read file
with open("boocks/america_small.txt", encoding="utf-8") as f:
    text = f.read()

# Get first 2 chunks
chunker = SemanticChunker(max_tokens=512)
chunks = list(chunker.chunk_text(text))[:2]

# Translate
translator = M2M100Adapter(use_gpu=False, model_size="418M")
pair = LanguagePair(source="es", target="pt")

for i, chunk in enumerate(chunks, 1):
    chunk_text = chunk["text"]
    translated = translator.translate(chunk_text, pair)
    
    print(f"=== CHUNK {i} ===")
    print(f"Original ({len(chunk_text)} chars):")
    print(chunk_text)
    print()
    print(f"Translated ({len(translated)} chars):")
    print(translated)
    print()
    print(f"Duplicated: {len(translated) > len(chunk_text) * 1.5}")
    print("="*60)
    print()
