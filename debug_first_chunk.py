"""Debug chunk processing."""
from modules.translator.infrastructure.m2m100_adapter import M2M100Adapter
from modules.translator.application.translation_service import TranslationService
from modules.translator.domain.chunker import SemanticChunker

# Read file
with open("boocks/america_small.txt", encoding="utf-8") as f:
    text = f.read()

# Get first chunk only
chunker = SemanticChunker(max_tokens=512)
chunks = list(chunker.chunk_text(text))
first_chunk = chunks[0]

print(f"Chunk text: '{first_chunk['text']}'")
print(f"Length: {len(first_chunk['text'])}")
print()

# Try translation
translator = M2M100Adapter(use_gpu=False, model_size="418M")
service = TranslationService(translator)

translation = service.translate_text(
    first_chunk['text'],
    target_language="pt",
    source_language="es"
)

print(f"Translated: '{translation.final_translation}'")
