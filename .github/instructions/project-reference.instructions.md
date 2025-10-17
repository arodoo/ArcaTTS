---
applyTo: '**'
---

# ArcaTTS Project Reference

## Core Paths

### Source Files
- Books: `boocks/`
- Franz Kafka: `boocks/franz-kafka.txt` (53,403 lines, 54 obras)

### Voice Models
- Path: `models/piper/`
- Mexican Spanish: `es_MX-claude-high.onnx` (60 MB, primary)
- Spain Spanish: `es_ES-sharvard-medium.onnx` (backup)

### Output Directories
- Manifests: `outputs/manifests/`
- Kafka audiobooks: `outputs/kafka/`
- Test outputs: `outputs/test/`
- Structure: `outputs/{author}/{NN_WORK_TITLE}/work.mp3`

### Module Structure
```
modules/
├── tts/
│   ├── cli.py (entry point)
│   ├── domain/ (business logic)
│   │   ├── audio_enhancer.py (204L - WORKING)
│   │   ├── enhanced_text_processor.py
│   │   ├── hyphenation_resolver.py
│   │   ├── punctuation_pauser.py
│   │   ├── pause_aware_chunker.py
│   │   ├── roman_converter.py
│   │   ├── silence_generator.py
│   │   ├── manifest_parser.py
│   │   ├── work_processor.py
│   │   ├── tts_engine.py
│   │   ├── wav_merger.py
│   │   └── mp3_converter.py
│   └── commands/ (CLI operations)
│       ├── parse_cmd.py
│       ├── process_cmd.py
│       ├── process_all_cmd.py
│       └── test_cmd.py
└── grammar/ (future module)
```

## CLI Commands

### Parse Book Structure
```bash
python -m modules.tts.cli parse <book_file> [--verbose]
```
**Example:**
```bash
python -m modules.tts.cli parse boocks/franz-kafka.txt --verbose
```
**Output:** `outputs/manifests/franz-kafka_manifest.json`

### Process Single Work
```bash
python -m modules.tts.cli process-work <manifest> <work_id> --output <dir>
```
**Example:**
```bash
python -m modules.tts.cli process-work \
  outputs/manifests/franz-kafka_manifest.json 50 \
  --output outputs/kafka
```
**Output:** `outputs/kafka/50_LA_VERDAD_SOBRE_SANCHO_PANZA/work.mp3`

### Process All Works (Batch)
```bash
python -m modules.tts.cli process-all <manifest> \
  --output <dir> \
  --workers <N> \
  --start-from <work_id>
```
**Example (Sequential):**
```bash
python -m modules.tts.cli process-all \
  outputs/manifests/franz-kafka_manifest.json \
  --output outputs/kafka \
  --workers 1 \
  --start-from 1
```
**Resume from work #25:**
```bash
python -m modules.tts.cli process-all \
  outputs/manifests/franz-kafka_manifest.json \
  --output outputs/kafka \
  --workers 1 \
  --start-from 25
```

### Quick Test
```bash
python -m modules.tts.cli test "texto de prueba"
```
**Output:** `outputs/test/test.mp3`

## Configuration Constants

### TTS Engine (Piper)
- **Model:** `es_MX-claude-high` (Mexican Spanish)
- **Sample Rate:** 22050 Hz
- **Bit Depth:** 16-bit Mono
- **noise_scale:** 0.667 (quality)
- **noise_w_scale:** 0.8 (quality)
- **License:** MIT (open source)

### Audio Enhancement (6-Stage Pipeline)
1. **Spectral Boost:** 3-8 kHz (clarity)
2. **Dynamic EQ:** 6-9 kHz de-essing (sibilant reduction)
3. **Vocal Presence:** 1-4 kHz boost (intimacy)
4. **Humanization:** 20ms micro-variations
5. **Multi-band Limiter:** Soft compression
6. **Normalization:** -3 dB target

### MP3 Conversion
- **Bitrate:** 128 kbps (default)
- **Format:** MP3 (MPEG-1 Layer 3)
- **Space Savings:** ~75% (4.2 MB WAV → 1.0 MB MP3)
- **Cleanup:** Auto-removes WAV chunks after conversion

### Punctuation Pauses (RAE-Compliant)
```
Comma (,)          → 0.3s (space)
Semicolon (;)      → 0.5s (.. periods)
Colon (:)          → 0.5s (.. periods)
Period (.)         → 0.7s (.... periods)
Question (?)       → 0.6s (... periods)
Exclamation (!)    → 0.6s (... periods)
Ellipsis (...)     → 0.8s (..... periods)
Paragraph break    → 1.0s (....... periods)
Title pause        → 2.0s (silence chunk)
Roman numeral      → 2.0s (silence chunk after)
```

### Hyphenation Markers
- **Negation symbol:** `¬` at line breaks
- **End-of-line hyphen:** `-` (lowercase-hyphen-newline-lowercase)
- **Equals sign:** `=` (rare OCR artifact)
- **Preserved:** Dialogue em-dash `—`, compound words

### Roman Numeral Conversion
```
I    → Primero        XI   → Undécimo
II   → Segundo        XII  → Duodécimo
III  → Tercero        XIII → Decimotercero
IV   → Cuarto         XIV  → Decimocuarto
V    → Quinto         XV   → Decimoquinto
VI   → Sexto          XVI  → Decimosexto
VII  → Séptimo        XVII → Decimoséptimo
VIII → Octavo         XVIII→ Decimoctavo
IX   → Noveno         XIX  → Decimonoveno
X    → Décimo         XX   → Vigésimo
```
**Pattern:** `^([IVX]+)\s*$` (standalone only)

## Text Processing Pipeline

### Order of Operations
```
1. HyphenationResolver.resolve()
   ↓ Fix OCR word breaks (¬, -, =)
2. EnhancedTextProcessor._add_title_pause()
   ↓ Insert 2s silence after first line
3. RomanConverter.convert_line()
   ↓ I→Primero with 2s pause
4. PunctuationPauser.add_pauses()
   ↓ Insert RAE-compliant pauses
5. PunctuationPauser.convert_to_piper_format()
   ↓ Convert <silence:X> markers to periods
6. PauseAwareChunker.chunk_text()
   ↓ Split without collapsing spaces
7. TTSEngine.synthesize()
   ↓ Generate WAV chunks
8. AudioEnhancer.enhance()
   ↓ Apply 6-stage processing
9. WavMerger.merge()
   ↓ Concatenate chunks natively
10. Mp3Converter.convert()
    ↓ WAV→MP3 with cleanup
```

## Manifest Format

### JSON Structure
```json
{
  "author": "Franz Kafka",
  "source_file": "boocks/franz-kafka.txt",
  "total_works": 54,
  "created_at": "2025-01-15T10:30:00",
  "works": [
    {
      "id": 1,
      "title": "OBRA TÍTULO",
      "year": 1915,
      "start_line": 123,
      "end_line": 456,
      "sanitized_title": "OBRA_TITULO",
      "folder_name": "01_OBRA_TITULO"
    }
  ]
}
```

### Index Markers (in source file)
```
ÍNDICE
$TÍTULO DE LA OBRA (1915)
$OTRA OBRA (1920)
FIN DEL ÍNDICE
```

## File Size Guidelines (60/60 Rule)

### Current Status
- ✅ Most files: <60 lines
- ⚠️ audio_enhancer.py: 204L (WORKING - refactor deferred)
- ⚠️ manifest_parser.py: 126L (needs split)
- ⚠️ tts_engine.py: 107L (needs split)
- ⚠️ manifest.py: 99L (needs split)
- ⚠️ process_cmd.py: 106L (needs optimization)

### Target Limits
- **Max lines:** 60 per file (CI fails at 80)
- **Max chars:** 60 per line (CI fails at 80)
- **Buffer:** 60/60 prevents manual fixes
- **Exceptions:** JSON files, generated code

## Performance Metrics

### Processing Times
- **Small work** (<1K lines): ~2 minutes
- **Medium work** (1-3K lines): ~3-5 minutes
- **Large work** (>5K lines): ~8-15 minutes
- **Full Kafka collection** (54 works): ~4.5 hours sequential

### File Sizes (Typical)
- **100 lines text:** ~1 MB MP3
- **500 lines text:** ~4-5 MB MP3
- **1000 lines text:** ~8-10 MB MP3
- **WAV vs MP3:** 75% reduction (4.2 MB → 1.0 MB)

## Environment Setup

### Python Version
```bash
python --version  # 3.11.x required
```

### Virtual Environment
```bash
# Activation
source venv/Scripts/activate  # Git Bash (Windows)
.\venv\Scripts\activate       # PowerShell
venv\Scripts\activate.bat     # CMD

# Deactivation
deactivate
```

### Dependencies Installation
```bash
pip install -r requirements.txt
```

### External Tools
```bash
# FFmpeg (required for MP3 conversion)
choco install ffmpeg -y  # Windows (Chocolatey)
```

## Testing Patterns

### Test Single Work
```bash
# Clear and regenerate
rm -rf outputs/kafka/50_LA_VERDAD_SOBRE_SANCHO_PANZA
python -m modules.tts.cli process-work \
  outputs/manifests/franz-kafka_manifest.json 50 \
  --output outputs/kafka
```

### Verify Audio Quality
1. Listen to `work.mp3`
2. Check file size (should be ~1 MB per 100 lines)
3. Verify pauses (title, Roman numerals, punctuation)
4. Confirm no word breaks (hyphenation fixed)

### Check Manifest
```bash
cat outputs/manifests/franz-kafka_manifest.json | head -50
```

## Common Workflows

### Process New Book
```bash
# 1. Parse structure
python -m modules.tts.cli parse boocks/new-book.txt --verbose

# 2. Test single work
python -m modules.tts.cli process-work \
  outputs/manifests/new-book_manifest.json 1 \
  --output outputs/new-author

# 3. Process all
python -m modules.tts.cli process-all \
  outputs/manifests/new-book_manifest.json \
  --output outputs/new-author \
  --workers 1
```

### Resume Interrupted Batch
```bash
# Check last completed work
ls outputs/kafka/ | tail -5

# Resume from next work (e.g., #25)
python -m modules.tts.cli process-all \
  outputs/manifests/franz-kafka_manifest.json \
  --output outputs/kafka \
  --workers 1 \
  --start-from 25
```

### Clean Output Directory
```bash
# Remove all generated audio
rm -rf outputs/kafka/*

# Remove specific work
rm -rf outputs/kafka/50_LA_VERDAD_SOBRE_SANCHO_PANZA
```

## Debugging Strategies

### Audio Quality Issues
1. Check if audio_enhancer.py is 204-line version (WORKING)
2. Never modify filter logic during refactoring
3. Test with known-good work (e.g., #50)
4. Compare old vs new chunks

### Missing Pauses
1. Verify PauseAwareChunker preserves spacing
2. Check PunctuationPauser period counts
3. Confirm RomanConverter adds silence chunks
4. Test with punctuation-heavy text

### Word Breaks
1. Check HyphenationResolver integration
2. Verify processing order (hyphenation FIRST)
3. Look for OCR artifacts (¬, -, =)
4. Test with known hyphenated words

### File Size Limit Violations
1. Count lines: `wc -l <file>`
2. Split at logical boundaries (classes, functions)
3. Follow DDD layers (domain/app/infra)
4. Respect 60/60 buffer (CI@80)

## Production Checklist

### Before Batch Processing
- [ ] Manifest generated and validated
- [ ] Single work tested successfully
- [ ] Audio quality confirmed "perfecto"
- [ ] FFmpeg installed and working
- [ ] Sufficient disk space (~10 GB for Kafka)
- [ ] Virtual environment activated

### During Batch Processing
- [ ] Monitor terminal for errors
- [ ] Check outputs/ directory for progress
- [ ] Note last completed work ID
- [ ] Verify MP3 files are generated

### After Batch Processing
- [ ] Count completed works: `ls outputs/kafka/ | wc -l`
- [ ] Check for failed works (missing MP3s)
- [ ] Verify total output size
- [ ] Test random samples for quality

## Architecture Principles

### DDD Layers
- **Domain:** Pure business logic (no I/O)
- **Commands:** CLI operations (orchestration)
- **Infrastructure:** External services (future: Celery, Redis, MinIO)

### SOLID Principles
- Single Responsibility: One concern per file
- Open/Closed: Extend without modifying
- Liskov Substitution: Interfaces over implementations
- Interface Segregation: Small, focused interfaces
- Dependency Inversion: Depend on abstractions

### Clean Architecture
- Domain layer has ZERO external dependencies
- Commands depend on domain, not vice versa
- Infrastructure adapters wrap external tools

## Known Limitations

### Current Implementation
- Sequential processing only (workers=1)
- No parallel TTS generation
- No distributed processing (Celery/Redis unused)
- No cloud storage (MinIO unused)
- Chapter detection not implemented

### Future Enhancements
- Parallel processing (workers>1)
- GPU acceleration (Piper CUDA support)
- Real-time progress streaming
- Web interface
- API endpoint for remote processing

## Critical Rules

### NEVER
- Modify audio_enhancer.py filter logic
- Collapse spaces in text processing
- Ignore 60/60 rule "temporarily"
- Process without testing single work first
- Commit TODO/FIXME comments

### ALWAYS
- Test audio quality after changes
- Preserve spacing in pause markers
- Count lines before committing
- Use descriptive variable names
- Catch specific exceptions (never empty)
- Write production-ready code from start

---

**Last Updated:** January 2025  
**Project:** ArcaTTS (Local TTS Pipeline)  
**License:** MIT (Piper), proprietary (project code)
