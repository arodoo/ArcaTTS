"""Check gaps between chunks."""
from modules.translator.domain.chunker import SemanticChunker

with open("boocks/america_small.txt", encoding="utf-8") as f:
    text = f.read()

chunker = SemanticChunker(max_tokens=512)
chunks = list(chunker.chunk_text(text))

print("Checking gaps between chunks:")
print("="*60)

for i in range(len(chunks) - 1):
    current_end = chunks[i]["end"]
    next_start = chunks[i+1]["start"]
    
    if current_end != next_start:
        gap_size = next_start - current_end
        gap_text = text[current_end:next_start]
        print(f"Gap {i+1}->{i+2}: {current_end} to {next_start}")
        print(f"  Size: {gap_size} chars")
        print(f"  Content: {repr(gap_text)}")
        print()
