# Processing Strategy: Large Files (53K+ Lines)

## Overview
**File:** franz-kafka.txt (53,508 lines)  
**Output Structure:** Individual audio per work (22+ separate files)  
**Format:** `Kafka/Obra_Nombre/obra.mp3`  
**Strategy:** Split → Process independently → Isolate failures

---

## File Structure Detection

### Index Markers (User-Provided)
```
ÍNDICE
  AMÉRICA (1912)
  LA METAMORFOSIS (1915)
  EL PROCESO (1925)
  ...
FIN DEL ÍNDICE

[Content of each work...]
```

### Output Organization
```
outputs/kafka/
├── 01_America/
│   ├── america_completo.mp3
│   ├── metadata.json
│   └── chapters/
│       ├── 01_capitulo.mp3
│       └── 02_capitulo.mp3
├── 02_La_Metamorfosis/
│   └── metamorfosis_completo.mp3
├── 03_El_Proceso/
│   └── proceso_completo.mp3
└── [20+ more works]
```

**Benefits:**
- ✅ One corruption ≠ lost everything
- ✅ Process in any order
- ✅ Parallel work processing
- ✅ Easy quality check per work
- ✅ Resume specific works only

---

## Critical Problems & Solutions

### 1. Processing Time
- **Problem:** 200-800 hours sequential
- **Solution:** Process 22 works in parallel
- **Result:** ~2-4 hours (all works simultaneously)

### 2. Work Isolation
- **Problem:** Failure in work #15 breaks everything
- **Solution:** Independent processing per work
- **Recovery:** Re-run only failed works

### 3. Storage Management
- **Problem:** 400GB total WAV files
- **Solution:** Per-work compression + cleanup
- **Flow:** Work WAV → MP3 → Delete WAV → Next work

### 4. Index Parsing
- **Problem:** Auto-detect work boundaries
- **Solution:** Use ÍNDICE/FIN markers + pattern matching
- **Validation:** User confirms detected works

### 5. Progress Tracking
- **Problem:** Which works are done?
- **Solution:** JSON manifest + Redis state
- **Status:** Real-time per-work progress

---

## Implementation Plan

### Phase 1: Parse & Validate (10 min)
```bash
# Extract index and validate structure
python -m modules.tts.cli parse franz-kafka.txt

# Output:
# ✓ Found 22 works between ÍNDICE markers
# ✓ Detected work boundaries
# ✓ Generated: kafka_manifest.json
```

**Manifest Example:**
```json
{
  "total_works": 22,
  "works": [
    {
      "id": 1,
      "title": "AMÉRICA",
      "year": 1912,
      "start_line": 150,
      "end_line": 5234,
      "estimated_duration": "2h 15m",
      "status": "pending"
    },
    {
      "id": 2,
      "title": "LA METAMORFOSIS",
      "year": 1915,
      "start_line": 5235,
      "end_line": 7890,
      "status": "pending"
    }
  ]
}
```

### Phase 2: Test Single Work (20 min)
```bash
# Process shortest work first (validation)
python -m modules.tts.cli process-work \
  --manifest kafka_manifest.json \
  --work-id 2 \
  --output outputs/kafka/

# Validates:
# - Parsing correctness
# - Audio quality
# - Merge logic
# - File organization
```

### Phase 3: Parallel Processing (2-8 hours)
```bash
# Process ALL works in parallel
python -m modules.tts.cli process-all \
  --manifest kafka_manifest.json \
  --workers 4 \
  --quality high

# Each work = independent Celery task group
# Failed works auto-retry 3 times
# Progress saved to Redis
```

### Phase 4: Verification (30 min)
```bash
# Check completion status
python -m modules.tts.cli status kafka_manifest.json

# Output:
# ✓ Completed: 20/22 works
# ⚠ Failed: 2 works (IDs: 15, 18)
# ⏳ Processing: 0 works
# 📊 Total audio: 38h 22m (12.4 GB)

# Retry failed works
python -m modules.tts.cli retry-failed kafka_manifest.json
```

---

## Processing Strategy

### Per-Work Workflow
```
For each work in manifest:
  1. Extract text (lines X to Y)
  2. Detect chapters/sections
  3. Chunk text (500 chars)
  4. Parallel synthesis (Celery)
  5. Merge chunks → chapters
  6. Merge chapters → work.mp3
  7. Generate metadata.json
  8. Cleanup temp files
  9. Update manifest status
```

### Parallel Execution
```python
# 4 works processing simultaneously
Work 1: [████████░░] 80% (Chapter 8/10)
Work 2: [██████████] 100% ✓ Complete
Work 3: [███░░░░░░░] 30% (Chapter 3/10)  
Work 4: [░░░░░░░░░░] 0% Queued
```

### Failure Isolation
```
Work 15 fails → Only Work 15 affected
Other 21 works → Continue normally
Retry Work 15 → Independent process
```

---

## File Organization

### Final Structure
```
outputs/kafka/
├── _manifest.json              # Master status file
├── _progress.json              # Real-time progress
│
├── 01_America_1912/
│   ├── america.mp3             # Final output (2h 15m)
│   ├── metadata.json           # Work info
│   └── cover.jpg               # Optional
│
├── 02_La_Metamorfosis_1915/
│   ├── metamorfosis.mp3        # Final output (1h 30m)
│   └── metadata.json
│
├── 03_El_Proceso_1925/
│   ├── proceso.mp3
│   └── metadata.json
│
└── [... 19 more works ...]
```

### Metadata Per Work
```json
{
  "title": "LA METAMORFOSIS",
  "author": "Franz Kafka",
  "year": 1915,
  "language": "es",
  "narrator": "Piper es_MX-claude-high",
  "duration": "1:32:45",
  "file_size": "425 MB",
  "chapters": 3,
  "generated": "2025-10-16T15:30:00Z",
  "enhancements": [
    "spectral_boost",
    "de-essing",
    "vocal_presence",
    "micro_humanization"
  ]
}
```

---

## Optimization Settings

### Quality Mode (Recommended)
```python
TTSEngine(
    language="es",
    enhance_quality=True
)
config = {
    "speed": 0.95,          # Slightly slower
    "chunk_size": 500,      # Optimal for quality
    "crossfade_ms": 100,    # Smooth transitions
    "workers": 8            # Parallel processing
}
```

### Fast Mode (Testing)
```python
TTSEngine(enhance_quality=False)
config = {
    "chunk_size": 1000,
    "workers": 16
}
```

---

## Monitoring & Recovery

### Real-time Dashboard
```bash
# Web interface
celery -A infrastructure.celery.celeryconfig flower
# → http://localhost:5555

# CLI status
python -m modules.tts.cli status

# Output:
# 📊 Kafka Complete Works Processing
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ✓ Completed:  18/22 works (81%)
# ⏳ Processing: 3/22 works
# ❌ Failed:     1/22 works
# 
# Currently processing:
#   - Work 19: EL CASTILLO [██████░░░░] 65%
#   - Work 20: CARTA AL PADRE [███░░░░░░░] 35%
#   - Work 21: UN ARTISTA... [█░░░░░░░░░] 12%
#
# Estimated completion: 2h 15m
```

### Recovery Commands
```bash
# List failed works
python -m modules.tts.cli failed

# Retry specific work
python -m modules.tts.cli retry --work-id 15

# Retry all failed
python -m modules.tts.cli retry-all

# Resume interrupted processing
python -m modules.tts.cli resume
```

### Checkpointing
```json
// Redis: kafka:work:15:checkpoint
{
  "work_id": 15,
  "title": "UN MÉDICO RURAL",
  "chunks_total": 456,
  "chunks_completed": 342,
  "last_chunk_id": "15_ch3_342",
  "last_updated": "2025-10-16T14:22:35Z",
  "can_resume": true
}
```

---

## Estimated Timeline

| Phase | Time | Description |
|-------|------|-------------|
| Parse & Validate | 10m | Extract index, create manifest |
| Test Single Work | 20m | Validate with shortest work |
| Infrastructure | 30m | Redis, MinIO, Celery setup |
| **Parallel Processing** | **2-8h** | All 22 works simultaneously |
| Verification | 30m | Check completion, retry failures |
| **Total** | **4-10h** | Complete collection (optimized) |

### Per-Work Estimates (Parallel)
```
Short works (1-2h audio):   30-60 min processing
Medium works (2-4h audio):  1-2 hours processing  
Long works (4-6h audio):    2-4 hours processing

With 4 parallel workers:
  Total sequential: 40-80 hours
  Actual time: 8-20 hours (4x faster)
  
With 8 parallel workers:
  Actual time: 4-10 hours (8x faster)
```

---

## Hardware Requirements

**Minimum (Sequential):**
- CPU: 4 cores
- RAM: 8GB
- Disk: 50GB free
- Time: 20-40h per complete run

**Recommended (4 works parallel):**
- CPU: 8 cores
- RAM: 16GB
- Disk: 100GB free (SSD)
- Time: 8-12h per complete run

**Optimal (8 works parallel):**
- CPU: 16 cores
- RAM: 32GB
- Disk: 200GB free (NVMe SSD)
- Time: 4-6h per complete run

---

## Quality Assurance

### Per-Work Validation
```bash
# Auto-check after each work completes
python -m modules.tts.cli validate --work-id 15

# Checks:
# ✓ Audio file exists and playable
# ✓ Duration matches expected
# ✓ No corrupted segments
# ✓ Consistent audio levels
# ✓ Metadata generated
```

### Batch Validation
```bash
# After all processing
python -m modules.tts.cli validate-all

# Generates report:
# - Total duration: 38h 22m
# - Average quality score: 94/100
# - Files with issues: 0
# - Total size: 12.4 GB
```

---

## Next Steps

1. ✅ TTS engine complete with enhancements
2. ✅ Strategy documented
3. ⏳ **Implement manifest parser** (reads ÍNDICE markers)
4. ⏳ **Create work splitter** (extracts each work)
5. ⏳ **Build batch processor** (parallel execution)
6. ⏳ Test with La Metamorfosis
7. ⏳ Process complete collection

---

**Strategy:** Independent works → Parallel processing → Isolated failures  
**Priority:** Reliability > Speed > Quality  
**Approach:** Parse → Test one → Process all → Validate
