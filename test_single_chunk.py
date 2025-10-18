"""Test simple: 1 chunk only."""
from modules.translator.domain.chunker import SemanticChunker
from modules.translator.infrastructure.m2m100_adapter import M2M100Adapter
from modules.translator.domain.value_objects import LanguagePair

# Read
with open("boocks/america_small.txt", encoding="utf-8") as f:
    text = f.read()

print(f"Original: {len(text)} chars")

# Chunk
chunker = SemanticChunker(max_tokens=200)
chunks = list(chunker.chunk_text(text))
print(f"Chunks: {len(chunks)}")

# Take chunk 7 (a longer one)
test_chunk = chunks[6]
print(f"\nChunk 7 original ({len(test_chunk['text'])} chars):")
print(test_chunk['text'][:300])
print("\n" + "="*60)

# Translate
translator = M2M100Adapter(use_gpu=False, model_size="418M")
pair = LanguagePair(source="es", target="pt")

translated = translator.translate(test_chunk['text'], pair)

print(f"\nChunk 7 translated ({len(translated)} chars):")
print(translated[:300])
print("\n" + "="*60)

# Check for duplication
original_words = test_chunk['text'].split()
translated_words = translated.split()

print(f"\nOriginal words: {len(original_words)}")
print(f"Translated words: {len(translated_words)}")
print(f"Ratio: {len(translated_words) / len(original_words):.2f}x")

if len(translated_words) > len(original_words) * 1.5:
    print("\n*** WARNING: Translated text is 50% longer! ***")
    print("*** This suggests duplication in the MODEL OUTPUT ***")
