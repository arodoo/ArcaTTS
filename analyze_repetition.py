"""Analyze where repetition starts."""
import re

with open("boocks/TEST100.txt", encoding="utf-8") as f:
    content = f.read()

# Find repetition patterns
lines = content.split('\n')

print(f"Total lines: {len(lines)}")
print("="*60)

# Look for repeated phrases
for i, line in enumerate(lines, 1):
    # Check if line has immediate repetition
    words = line.split()
    if len(words) > 10:
        # Check for patterns like "A A A A"
        for j in range(len(words) - 3):
            if words[j] == words[j+1] == words[j+2] == words[j+3]:
                print(f"Line {i}: Found 4x repetition")
                print(f"  Pattern: '{words[j]}'")
                print(f"  Context: {' '.join(words[max(0,j-5):j+10])}")
                print()
                break

# Find the problematic section
problem_text = "- Você vai querer-se."
if problem_text in content:
    idx = content.index(problem_text)
    before = content[max(0, idx-200):idx]
    after = content[idx:min(len(content), idx+200)]
    
    print("="*60)
    print("PROBLEM SECTION FOUND:")
    print("="*60)
    print("BEFORE:")
    print(before)
    print("\n>>> REPETITION STARTS HERE <<<\n")
    print(after)
