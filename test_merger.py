"""Test merger with simulated translated chunks."""
from modules.translator.application.chunk_merger import ChunkMerger
from modules.translator.domain.models import TranslationChunk

# Original text with gaps
original = "FRANZ KAFKA\n\nAMERICA\n\nCAPÍTULO PRIMERO"

# Simulate chunks (positions match gaps)
chunks = [
    TranslationChunk(
        original_text="FRANZ KAFKA",
        translated_text="FRANÇA KAFKA",
        start_position=0,
        end_position=11,
        context_before="",
        context_after=""
    ),
    TranslationChunk(
        original_text="AMERICA",
        translated_text="AMÉRICA",
        start_position=13,
        end_position=20,
        context_before="",
        context_after=""
    ),
    TranslationChunk(
        original_text="CAPÍTULO PRIMERO",
        translated_text="CAPÍTULO PRIMEIRO",
        start_position=22,
        end_position=38,
        context_before="",
        context_after=""
    ),
]

print(f"Original ({len(original)} chars):")
print(repr(original))
print("="*60)

merged = ChunkMerger.merge_chunks(chunks, original)

print(f"Merged ({len(merged)} chars):")
print(repr(merged))
print("="*60)

print("Result:")
print(merged)
print("="*60)

expected = "FRANÇA KAFKA\n\nAMÉRICA\n\nCAPÍTULO PRIMEIRO"
if merged == expected:
    print("SUCCESS - Merger preserves gaps correctly")
else:
    print("FAIL - Merger corrupted text")
    print(f"Expected: {repr(expected)}")
