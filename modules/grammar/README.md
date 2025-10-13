# Grammar Module# Grammar Module



**Automatic Grammar Correction for Spanish Text****Text Grammar Correction**



Detects and fixes grammar, spelling, and punctuation errors Automatically detects and fixes grammar, spelling, and 

using LanguageTool while preserving the original file.punctuation errors in text documents.



---## Features (Planned)



## Features- Grammar error detection

- Spelling correction

✅ **Grammar checking** - Detects grammatical errors  - Punctuation normalization

✅ **Spelling correction** - Fixes typos and misspellings  - Style consistency

✅ **Punctuation** - Corrects punctuation mistakes  - Multi-language support (EN, ES, PT-BR)

✅ **Spanish language** - Optimized for Spanish text  - Batch processing for large documents

✅ **Preserves original** - Never modifies source file  

✅ **Batch processing** - Handles large files efficiently## Structure



---```

grammar/

## Installation├── domain/          # Business logic

│   ├── corrector.py # Grammar correction engine

```bash│   └── rules.py     # Language-specific rules

# Install dependencies├── tasks/           # Celery tasks

pip install language-tool-python└── tests/           # Test suite

```

# LanguageTool will auto-download on first use

```## Usage (Planned)



---```bash

python -m modules.grammar.cli correct \

## Usage  --input text.txt \

  --language es \

### 1. Check for Errors (No Fixing)  --output corrected.txt

```

```bash

python -m modules.grammar.cli check \## Dependencies (Planned)

  boocks/franz-kafka.txt \

  --language es \- LanguageTool or similar grammar checker

  --verbose- spaCy for NLP processing

```- Language-specific models


**Output:**
```
Checking boocks/franz-kafka.txt...

✓ Found 127 issues

1. [spelling]
   Message: Posible error ortográfico
   Original: 'prueva'
   Suggested: 'prueba'

2. [grammar]
   Message: Concordancia de número
   Original: 'falta algunos'
   Suggested: 'faltan algunos'
...
```

---

### 2. Correct Errors (Generate Fixed File)

```bash
python -m modules.grammar.cli correct \
  boocks/franz-kafka.txt \
  --language es
```

**Output:**
```
Processing boocks/franz-kafka.txt...

✓ Correction complete!

Total errors: 127
Fixed: 105
Output: boocks_corrected/franz-kafka.txt
```

**Custom output path:**
```bash
python -m modules.grammar.cli correct \
  boocks/franz-kafka.txt \
  --output my_corrected/kafka_fixed.txt
```

---

## File Structure

```
modules/grammar/
├── domain/
│   ├── models.py        # Error models
│   ├── checker.py       # LanguageTool wrapper
│   └── corrector.py     # Correction engine
├── tasks/               # Celery tasks (future)
├── tests/               # Unit tests
├── cli.py               # CLI interface
└── test_grammar.py      # Quick test
```

---

## Domain Models

### GrammarError
Represents a detected error:
- `line_number` - Line in file
- `offset` - Character position
- `error_type` - Type (spelling, grammar, etc.)
- `severity` - Low, medium, high
- `message` - Error description
- `suggested_replacement` - Suggested fix

### CorrectionResult
Result of correction process:
- `original_file` - Input path
- `corrected_file` - Output path
- `total_errors` - Errors found
- `fixed_errors` - Errors corrected
- `errors` - List of GrammarError

---

## Error Types

- **SPELLING** - Typos, misspellings
- **GRAMMAR** - Grammatical errors
- **PUNCTUATION** - Missing/incorrect punctuation
- **TYPOGRAPHY** - Formatting issues
- **STYLE** - Style recommendations

---

## Language Support

Currently supported:
- **Spanish (es)** - Primary
- **English (en)** - Available
- **Portuguese (pt)** - Available

To change language:
```bash
--language en
```

---

## Output

### Default Location
```
boocks_corrected/
└── franz-kafka.txt      # Corrected version
```

### Original File
```
boocks/
└── franz-kafka.txt      # NEVER modified
```

**Guarantee:** Original files are never touched!

---

## Examples

### Example 1: Check Only
```bash
# See what errors exist
python -m modules.grammar.cli check \
  boocks/franz-kafka.txt \
  -v
```

### Example 2: Correct with Custom Path
```bash
# Fix and save to specific location
python -m modules.grammar.cli correct \
  boocks/franz-kafka.txt \
  --output corrected_books/kafka.txt
```

### Example 3: Detect Without Fixing
```bash
# Generate file but don't apply fixes
python -m modules.grammar.cli correct \
  boocks/franz-kafka.txt \
  --no-fix
```

---

## Testing

### Quick Test (Sample Text)
```bash
python -m modules.grammar.test_grammar
```

### Full File Test
```bash
python -m modules.grammar.cli check \
  boocks/franz-kafka.txt \
  --verbose
```

---

## Performance

**Processing Speed:**
- Small files (< 10KB): ~2-5 seconds
- Medium files (100KB): ~10-30 seconds  
- Large files (1MB+): ~1-5 minutes

**For the Kafka file (53K lines):**
- Estimated time: 2-4 minutes
- Errors expected: 100-500
- Auto-fixable: 70-90%

---

## Integration with TTS Module

Grammar correction should run **before** TTS:

```bash
# Step 1: Fix grammar
python -m modules.grammar.cli correct \
  boocks/franz-kafka.txt

# Step 2: Generate audio from corrected file
python -m modules.tts.cli process \
  boocks_corrected/franz-kafka.txt \
  --language es
```

---

## Future Enhancements

- [ ] Batch processing via Celery
- [ ] Custom rule configuration
- [ ] Interactive correction mode
- [ ] Diff visualization
- [ ] Multiple language models
- [ ] Grammar statistics/reports

---

## Troubleshooting

### LanguageTool Download Failed
```bash
# Manually specify local LanguageTool
export LANGUAGETOOL_JAR=/path/to/languagetool.jar
```

### Memory Issues (Large Files)
Process in chunks (future feature via Celery)

### Wrong Language Detected
Always specify explicitly:
```bash
--language es
```

---

## Dependencies

- `language-tool-python` - Grammar checking engine
- `click` - CLI framework
- Java Runtime (auto-installed by language-tool)

---

**Status:** ✅ Ready to use  
**Next:** Run correction on Kafka file!
