"""Debug translation to see what's being sent."""
from modules.translator.domain.chunker import SemanticChunker
from modules.translator.infrastructure.m2m100_adapter import M2M100Adapter
from modules.translator.domain.value_objects import LanguagePair

# Read small file
with open("boocks/america_small.txt", encoding="utf-8") as f:
    text = f.read()

print(f"Original: {len(text)} chars, {text.count(chr(10))} lines")
print("="*60)

# Get chunks
chunker = SemanticChunker(max_tokens=200)
chunks = list(chunker.chunk_text(text))

print(f"Generated {len(chunks)} chunks\n")

# Test translate first 3 chunks
translator = M2M100Adapter(use_gpu=False, model_size="418M")
pair = LanguagePair(source="es", target="pt")

for i, chunk in enumerate(chunks[:3], 1):
    original = chunk["text"]
    translated = translator.translate(original, pair)
    
    print(f"=== CHUNK {i} ===")
    print(f"Original ({len(original)} chars):")
    print(original[:200] + "..." if len(original) > 200 else original)
    print()
    print(f"Translated ({len(translated)} chars):")
    print(translated[:200] + "..." if len(translated) > 200 else translated)
    print()
    print(f"Has repetition: {'repeated' in translated.lower() or translated.count('.') > original.count('.') * 2}")
    print("="*60)
    print()
