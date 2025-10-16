# 🎙️ Text-to-Voice App (XTTS-v2)

**Monolithic Python pipeline for local, cost-zero TTS at scale.**  
Designed for solo creators with GPU access requiring fast iteration.

---

## 🏗️ Simplified Architecture

```
Python CLI (argparse)
  ↓
Celery Tasks (translate → TTS chunks → merge)
  ↓
Redis (broker + result backend)
  ↓
XTTS-v2 Workers (Direct GPU Access)
  ↓
MinIO (S3-compatible local storage)
```

**Key Design Decisions:**
- ❌ **No Docker:** Direct venv for fast debug & deployment
- ❌ **No PostgreSQL:** Redis + local JSON for persistence
- ❌ **No FastAPI/React:** CLI-driven automation, no web overhead
- ✅ **No Licensing:** Open-source Piper TTS (MIT license)
- ✅ **Cost-Zero:** Runs entirely on local hardware

---

## 🛠️ Tech Stack (Revised)

**CLI:** Python argparse  
**Task Queue:** Celery  
**Broker/Backend:** Redis (dual role)  
**Storage:** MinIO (local S3 API)  
**TTS Engine:** Piper TTS (ONNX Runtime)  
**Languages:** EN, ES, PT-BR  
**Environment:** Python venv (no containers)

---

## ✨ Features

- CLI-based job submission & monitoring
- Upload/paste text (.txt files)
- Voice selection & cloning
- Parallel chunk processing (Celery workers)
- Real-time job status via Redis
- Multi-format output (MP3, WAV, OGG)
- Multi-language support (EN/ES/PT-BR)
- Job history & result storage

---

## 📊 Component Breakdown

### 1. Python CLI (`cli.py`)
**Purpose:** User interface for pipeline control  
**Commands:**
- `python cli.py submit --text-file book.txt --voice-id 5`
- `python cli.py status --job-id abc123`
- `python cli.py list-jobs`
- `python cli.py upload-voice --sample voice.wav --name "My Voice"`

**Actions:** Dispatches Celery tasks, queries Redis for status

---

### 2. Celery Workers (`workers/`)
**Purpose:** Async task execution with parallelism  
**Tasks:**
- `chunk_text_task`: Split large text into processable chunks
- `translate_chunk_task` (optional): Cross-language translation
- `synthesize_audio_task`: XTTS-v2 GPU processing per chunk
- `merge_audio_task`: Combine chunks into final file

**Concurrency:** Multi-worker for GPU utilization

---

### 3. Redis
**Role 1:** Celery message broker (task queue)  
**Role 2:** Result backend (job status, metadata)  
**Persistence:** Job metadata, progress tracking, voice profiles

**Why not PostgreSQL?**  
Redis provides sufficient persistence for a solo project without 
the overhead of relational schema management.

---

### 4. MinIO
**Purpose:** S3-compatible local object storage  
**Stores:**
- Audio chunks (intermediate)
- Final merged audio files
- Voice sample uploads
- Model checkpoints (optional)

**Why MinIO?**  
Maintains S3 API compatibility (easy migration to cloud if needed) 
while operating cost-free locally.

---

### 5. Piper TTS Engine
**Integration:** Direct Python import (piper-tts library)  
**Runtime:** ONNX Runtime (CPU/GPU compatible)  
**Capabilities:**
- Open-source, no licensing restrictions
- Multi-language synthesis (EN/ES/PT-BR)
- High-quality neural voices
- Fast CPU inference

**Performance:** Lightweight and efficient

---

## 🔄 Data Flow

```
1. User runs CLI → submits text file
   ↓
2. CLI dispatches `chunk_text_task` to Celery
   ↓
3. Celery queues `synthesize_audio_task` per chunk
   ↓
4. Workers grab tasks from Redis, process on GPU
   ↓
5. Chunks saved to MinIO → task results to Redis
   ↓
6. Final `merge_audio_task` combines chunks
   ↓
7. CLI polls Redis → downloads from MinIO
```

---

## 📁 Project Structure

```
/
├── cli.py                 # CLI entry point
├── config.py              # Redis/MinIO/TTS config
├── requirements.txt       # Dependencies
├── setup.sh               # venv setup script
│
├── domain/                # Core business logic
│   ├── tts_engine.py      # XTTS-v2 wrapper
│   ├── text_processor.py  # Chunking logic
│   └── audio_merger.py    # Post-processing
│
├── tasks/                 # Celery task definitions
│   ├── __init__.py
│   ├── text_tasks.py      # chunk_text_task
│   ├── tts_tasks.py       # synthesize_audio_task
│   └── merge_tasks.py     # merge_audio_task
│
├── storage/               # MinIO client wrappers
│   └── minio_client.py
│
└── tests/                 # Unit & integration tests
    ├── test_tts.py
    └── test_tasks.py
```

---

## � Implementation Status

✅ **Environment Setup** - Python 3.11, dependencies installed  
✅ **Core TTS** - Piper TTS integration (license-free)  
✅ **Text Pipeline** - Text chunking & processing logic  
✅ **Storage Layer** - MinIO client wrapper  
✅ **CLI Interface** - Command-line tools  
✅ **Audio Merging** - Chunk combination with pydub  
✅ **Celery Tasks** - Async task definitions  
⏳ **Testing** - Piper model download & integration  
⏳ **Redis/MinIO** - Service configuration needed  
⏳ **Monitoring** - Celery Flower setup pending

---

## 📈 Performance & Scaling

**Local Scaling:**
- Add Celery workers (`celery -A tasks worker -c 4`)
- Batch size optimization per GPU memory
- Chunk-level parallelism (10+ chunks simultaneously)

**GPU Utilization:**
- Direct CUDA access (no virtualization overhead)
- Mixed precision (FP16) for 2x speedup
- Model caching in GPU memory

**Storage:**
- MinIO automatic cleanup (retention policies)
- Compress old jobs to archives

---

**Next Steps:** Setup venv → Install dependencies → Configure services
# ArcaTTS
