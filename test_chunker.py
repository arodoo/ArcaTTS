"""Test chunker independently."""
from modules.translator.domain.chunker import SemanticChunker

# Read small file
with open("boocks/america_small.txt", encoding="utf-8") as f:
    text = f.read()

print(f"Original text: {len(text)} chars, {text.count(chr(10))} lines")
print("="*60)

# Create chunker
chunker = SemanticChunker(max_tokens=512)
chunks = list(chunker.chunk_text(text))

print(f"Generated {len(chunks)} chunks")
print("="*60)

# Check each chunk
for i, chunk in enumerate(chunks):
    chunk_text = chunk["text"]
    start = chunk["start"]
    end = chunk["end"]
    
    # Verify chunk matches original
    expected = text[start:end]
    matches = chunk_text == expected
    
    print(f"Chunk {i+1}: start={start}, end={end}")
    print(f"  Length: {len(chunk_text)} chars")
    print(f"  Matches original: {matches}")
    
    if not matches:
        print(f"  ❌ ERROR: Chunk doesn't match!")
        print(f"  Chunk text: {chunk_text[:100]}...")
        print(f"  Expected: {expected[:100]}...")
    
    print()

# Reconstruct text
reconstructed = "".join([chunk["text"] for chunk in chunks])
print("="*60)
print(f"Reconstructed: {len(reconstructed)} chars")
print(f"Original: {len(text)} chars")
print(f"Match: {reconstructed == text}")

if reconstructed != text:
    print("❌ RECONSTRUCTION FAILED")
else:
    print("✅ RECONSTRUCTION SUCCESS")
