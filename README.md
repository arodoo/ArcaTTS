# ArcaTTS - Local Text-to-Speech Pipeline# 🎙️ Text-to-Voice App (XTTS-v2)



Sistema local de generación de audiolibros usando Piper TTS con procesamiento profesional de audio.**Monolithic Python pipeline for local, cost-zero TTS at scale.**  

Designed for solo creators with GPU access requiring fast iteration.

## 🚀 Instalación Rápida

---

```bash

# Activar entorno virtual## 🏗️ Simplified Architecture

source venv/Scripts/activate  # Git Bash

# .\venv\Scripts\activate     # PowerShell```

Python CLI (argparse)

# Instalar dependencias  ↓

pip install -r requirements.txtCelery Tasks (translate → TTS chunks → merge)

  ↓

# Instalar FFmpeg (para conversión MP3)Redis (broker + result backend)

choco install ffmpeg -y  ↓

```XTTS-v2 Workers (Direct GPU Access)

  ↓

## 📖 Comandos PrincipalesMinIO (S3-compatible local storage)

```

### 1. Parsear Libro (Generar Manifest)

**Key Design Decisions:**

Extrae la estructura del libro (índice de obras) y genera un manifest JSON.- ❌ **No Docker:** Direct venv for fast debug & deployment

- ❌ **No PostgreSQL:** Redis + local JSON for persistence

```bash- ❌ **No FastAPI/React:** CLI-driven automation, no web overhead

python -m modules.tts.cli parse boocks/libro.txt [--verbose]- ✅ **No Licensing:** Open-source Piper TTS (MIT license)

```- ✅ **Cost-Zero:** Runs entirely on local hardware



**Ejemplo:**---

```bash

python -m modules.tts.cli parse boocks/franz-kafka.txt --verbose## 🛠️ Tech Stack (Revised)

```

**CLI:** Python argparse  

**Output:** `outputs/manifests/libro_manifest.json`**Task Queue:** Celery  

**Broker/Backend:** Redis (dual role)  

**Requisitos del archivo de entrada:****Storage:** MinIO (local S3 API)  

- Debe tener sección ÍNDICE con marcadores `$TÍTULO (YEAR)`**TTS Engine:** Piper TTS (ONNX Runtime)  

- Ejemplo:**Languages:** EN, ES, PT-BR  

  ```**Environment:** Python venv (no containers)

  ÍNDICE

  $LA METAMORFOSIS (1915)---

  $EL PROCESO (1925)

  FIN DEL ÍNDICE## ✨ Features

  ```

- CLI-based job submission & monitoring

---- Upload/paste text (.txt files)

- Voice selection & cloning

### 2. Procesar Obra Individual- Parallel chunk processing (Celery workers)

- Real-time job status via Redis

Genera audio MP3 de una sola obra del manifest.- Multi-format output (MP3, WAV, OGG)

- Multi-language support (EN/ES/PT-BR)

```bash- Job history & result storage

python -m modules.tts.cli process-work <manifest> <work_id> --output <dir>

```---



**Ejemplo:**## 📊 Component Breakdown

```bash

python -m modules.tts.cli process-work \### 1. Python CLI (`cli.py`)

  outputs/manifests/franz-kafka_manifest.json 50 \**Purpose:** User interface for pipeline control  

  --output outputs/kafka**Commands:**

```- `python cli.py submit --text-file book.txt --voice-id 5`

- `python cli.py status --job-id abc123`

**Output:** `outputs/kafka/50_TITULO_OBRA/work.mp3`- `python cli.py list-jobs`

- `python cli.py upload-voice --sample voice.wav --name "My Voice"`

**Útil para:**

- Probar calidad antes del batch completo**Actions:** Dispatches Celery tasks, queries Redis for status

- Regenerar una obra específica

- Depuración---



---### 2. Celery Workers (`workers/`)

**Purpose:** Async task execution with parallelism  

### 3. Procesar Libro Completo (Batch)**Tasks:**

- `chunk_text_task`: Split large text into processable chunks

Genera audio MP3 de todas las obras del manifest.- `translate_chunk_task` (optional): Cross-language translation

- `synthesize_audio_task`: XTTS-v2 GPU processing per chunk

```bash- `merge_audio_task`: Combine chunks into final file

python -m modules.tts.cli process-all <manifest> \

  --output <dir> \**Concurrency:** Multi-worker for GPU utilization

  --workers <N> \

  --start-from <work_id>---

```

### 3. Redis

**Ejemplo completo:****Role 1:** Celery message broker (task queue)  

```bash**Role 2:** Result backend (job status, metadata)  

python -m modules.tts.cli process-all \**Persistence:** Job metadata, progress tracking, voice profiles

  outputs/manifests/franz-kafka_manifest.json \

  --output outputs/kafka \**Why not PostgreSQL?**  

  --workers 1 \Redis provides sufficient persistence for a solo project without 

  --start-from 1the overhead of relational schema management.

```

---

**Parámetros:**

- `--workers 1`: Procesamiento secuencial (única opción actual)### 4. MinIO

- `--start-from N`: Empezar desde la obra N (para reanudar)**Purpose:** S3-compatible local object storage  

**Stores:**

**Ejemplo para reanudar desde obra #25:**- Audio chunks (intermediate)

```bash- Final merged audio files

python -m modules.tts.cli process-all \- Voice sample uploads

  outputs/manifests/franz-kafka_manifest.json \- Model checkpoints (optional)

  --output outputs/kafka \

  --workers 1 \**Why MinIO?**  

  --start-from 25Maintains S3 API compatibility (easy migration to cloud if needed) 

```while operating cost-free locally.



**Tiempo estimado:**---

- Obra pequeña (<1K líneas): ~2 min

- Obra mediana (1-3K líneas): ~3-5 min### 5. Piper TTS Engine

- Obra grande (>5K líneas): ~8-15 min**Integration:** Direct Python import (piper-tts library)  

- Kafka completo (54 obras): ~4.5 horas**Runtime:** ONNX Runtime (CPU/GPU compatible)  

**Capabilities:**

---- Open-source, no licensing restrictions

- Multi-language synthesis (EN/ES/PT-BR)

### 4. Prueba Rápida- High-quality neural voices

- Fast CPU inference

Genera audio de prueba con procesamiento completo (pausas, enhancement).

**Performance:** Lightweight and efficient

```bash

python -m modules.tts.cli test --text "tu texto aquí"---

```

## 🔄 Data Flow

**Ejemplo:**

```bash```

python -m modules.tts.cli test --text "Primera frase. Segunda frase. Diálogo -¿verdad?- final."1. User runs CLI → submits text file

```   ↓

2. CLI dispatches `chunk_text_task` to Celery

**Output:** `outputs/test/quick_test.wav`   ↓

3. Celery queues `synthesize_audio_task` per chunk

**Útil para:**   ↓

- Verificar pausas de puntuación4. Workers grab tasks from Redis, process on GPU

- Probar diálogos   ↓

- Confirmar calidad de audio5. Chunks saved to MinIO → task results to Redis

   ↓

---6. Final `merge_audio_task` combines chunks

   ↓

## 📁 Estructura de Outputs7. CLI polls Redis → downloads from MinIO

```

```

outputs/---

├── manifests/

│   └── autor_manifest.json        # Índice de obras## 📁 Project Structure

├── autor/

│   ├── 01_TITULO_OBRA/```

│   │   ├── work.mp3              # Audio final (128kbps)/

│   │   ├── text.txt              # Texto extraído├── cli.py                 # CLI entry point

│   │   └── metadata.json         # Metadatos├── config.py              # Redis/MinIO/TTS config

│   ├── 02_OTRA_OBRA/├── requirements.txt       # Dependencies

│   └── ...├── setup.sh               # venv setup script

└── test/│

    └── quick_test.wav            # Pruebas rápidas├── domain/                # Core business logic

```│   ├── tts_engine.py      # XTTS-v2 wrapper

│   ├── text_processor.py  # Chunking logic

---│   └── audio_merger.py    # Post-processing

│

## 🎯 Workflows Comunes├── tasks/                 # Celery task definitions

│   ├── __init__.py

### Procesar Nuevo Libro│   ├── text_tasks.py      # chunk_text_task

│   ├── tts_tasks.py       # synthesize_audio_task

```bash│   └── merge_tasks.py     # merge_audio_task

# 1. Parsear estructura│

python -m modules.tts.cli parse boocks/nuevo-libro.txt --verbose├── storage/               # MinIO client wrappers

│   └── minio_client.py

# 2. Probar una obra (ej: obra #1)│

python -m modules.tts.cli process-work \└── tests/                 # Unit & integration tests

  outputs/manifests/nuevo-libro_manifest.json 1 \    ├── test_tts.py

  --output outputs/nuevo-autor    └── test_tasks.py

```

# 3. Escuchar y verificar calidad

# (abrir outputs/nuevo-autor/01_TITULO/work.mp3)---



# 4. Si OK, procesar todo## � Implementation Status

python -m modules.tts.cli process-all \

  outputs/manifests/nuevo-libro_manifest.json \✅ **Environment Setup** - Python 3.11, dependencies installed  

  --output outputs/nuevo-autor \✅ **Core TTS** - Piper TTS integration (license-free)  

  --workers 1✅ **Text Pipeline** - Text chunking & processing logic  

```✅ **Storage Layer** - MinIO client wrapper  

✅ **CLI Interface** - Command-line tools  

---✅ **Audio Merging** - Chunk combination with pydub  

✅ **Celery Tasks** - Async task definitions  

### Reanudar Batch Interrumpido⏳ **Testing** - Piper model download & integration  

⏳ **Redis/MinIO** - Service configuration needed  

```bash⏳ **Monitoring** - Celery Flower setup pending

# 1. Ver última obra completada

ls outputs/kafka/ | tail -5---



# 2. Reanudar desde siguiente (ej: última fue #24)## 📈 Performance & Scaling

python -m modules.tts.cli process-all \

  outputs/manifests/franz-kafka_manifest.json \**Local Scaling:**

  --output outputs/kafka \- Add Celery workers (`celery -A tasks worker -c 4`)

  --workers 1 \- Batch size optimization per GPU memory

  --start-from 25- Chunk-level parallelism (10+ chunks simultaneously)

```

**GPU Utilization:**

---- Direct CUDA access (no virtualization overhead)

- Mixed precision (FP16) for 2x speedup

### Regenerar Obra Específica- Model caching in GPU memory



```bash**Storage:**

# 1. Eliminar obra existente- MinIO automatic cleanup (retention policies)

rm -rf outputs/kafka/50_LA_VERDAD_SOBRE_SANCHO_PANZA- Compress old jobs to archives



# 2. Regenerar---

python -m modules.tts.cli process-work \

  outputs/manifests/franz-kafka_manifest.json 50 \**Next Steps:** Setup venv → Install dependencies → Configure services

  --output outputs/kafka# ArcaTTS

```

---

### Limpiar Outputs

```bash
# Eliminar todos los audios de un autor
rm -rf outputs/kafka/*

# Eliminar obra específica
rm -rf outputs/kafka/50_TITULO_OBRA

# Eliminar manifest (para regenerar)
rm outputs/manifests/franz-kafka_manifest.json
```

---

## 🎛️ Configuración del Sistema

### Voz y Calidad

**Modelo TTS:** Piper `es_MX-claude-high` (Español México)
- Sample Rate: 22050 Hz
- Calidad: noise_scale=0.667, noise_w_scale=0.8
- Licencia: MIT (open source)

**Audio Enhancement (6 etapas):**
1. Spectral Boost: 3-8 kHz (claridad)
2. Dynamic EQ: 6-9 kHz de-essing (sibilantes)
3. Vocal Presence: 1-4 kHz (intimidad)
4. Humanization: Variaciones de 20ms
5. Multi-band Limiter: Compresión suave
6. Normalization: -3 dB target

**Conversión MP3:**
- Bitrate: 128 kbps
- Ahorro: ~75% (4.2 MB WAV → 1.0 MB MP3)
- Auto-cleanup: Elimina WAVs temporales

### Pausas de Puntuación (RAE)

```
Coma (,)          → 0.3s
Punto y coma (;)  → 0.5s
Dos puntos (:)    → 0.5s
Punto (.)         → 0.7s
Interrogación (?) → 0.6s
Exclamación (!)   → 0.6s
Puntos suspensivos → 0.8s
Diálogo -¿...?-   → 0.4s antes y después
Título            → 2.0s después
Número romano     → 2.0s después
```

**Nota:** Los saltos de línea (`\n`) se ignoran (son solo formato).

### Números Romanos

Conversión automática a ordinales españoles:
```
I → Primero       XI → Undécimo
II → Segundo      XII → Duodécimo
III → Tercero     ...
X → Décimo        XX → Vigésimo
```

---

## 🔍 Verificación y Debugging

### Verificar Manifest

```bash
cat outputs/manifests/franz-kafka_manifest.json | head -50
```

### Contar Obras Completadas

```bash
ls outputs/kafka/ | wc -l
```

### Ver Última Obra Procesada

```bash
ls -lt outputs/kafka/ | head -5
```

### Verificar Calidad de Audio

```bash
# Generar prueba específica
python -m modules.tts.cli test --text "Texto de prueba. Con puntos, comas; y diálogos -¿verdad?- finales."

# Escuchar: outputs/test/quick_test.wav
```

### Tamaño de Archivos

```bash
# Ver tamaño total de outputs
du -sh outputs/kafka/

# Ver tamaño de obra específica
du -sh outputs/kafka/50_TITULO_OBRA/
```

---

## ⚠️ Solución de Problemas

### Error: "Model not found"

```bash
# Verificar que existe el modelo
ls -lh models/piper/es_MX-claude-high.onnx
```

### Error: "ffmpeg not found"

```bash
# Instalar FFmpeg
choco install ffmpeg -y

# Verificar instalación
ffmpeg -version
```

### Audio sin pausas de puntuación

El sistema usa silence chunks WAV, NO múltiples puntos.
Verificar con comando test:

```bash
python -m modules.tts.cli test --text "Prueba. Con puntos."
```

### Batch interrumpido

Usa `--start-from` para reanudar:

```bash
python -m modules.tts.cli process-all \
  outputs/manifests/libro_manifest.json \
  --output outputs/autor \
  --workers 1 \
  --start-from 25
```

---

## 📊 Métricas de Referencia

### Franz Kafka (53,403 líneas, 54 obras)

- **Tiempo total:** ~4.5 horas (secuencial)
- **Tamaño output:** ~500-800 MB (MP3 128kbps)
- **Obra más pequeña:** ~1 MB
- **Obra más grande:** ~20-30 MB

### Estimaciones por Tamaño

| Líneas | Tiempo | MP3 Size |
|--------|--------|----------|
| 100    | 2 min  | ~1 MB    |
| 500    | 5 min  | ~4-5 MB  |
| 1000   | 8 min  | ~8-10 MB |
| 5000   | 30 min | ~40-50 MB|

---

## 🎓 Mejores Prácticas

1. **Siempre probar primero:**
   ```bash
   python -m modules.tts.cli process-work manifest.json 1 --output test
   ```

2. **Verificar manifest antes de batch:**
   ```bash
   cat outputs/manifests/libro_manifest.json | grep '"title"'
   ```

3. **Monitorear progreso:**
   ```bash
   watch -n 10 'ls outputs/kafka/ | wc -l'
   ```

4. **Dejar corriendo en terminal separada:**
   - Usar `tmux` o `screen` para sesiones persistentes
   - O simplemente dejar la terminal abierta

5. **Backup de manifests:**
   ```bash
   cp outputs/manifests/*.json backups/
   ```

---

## 🚫 Limitaciones Actuales

- ❌ Procesamiento paralelo (workers>1) no implementado
- ❌ Detección de capítulos no implementada
- ❌ Sin interfaz web
- ❌ Sin API REST
- ✅ Solo procesamiento secuencial
- ✅ Solo almacenamiento local

---

## 📝 Formato de Archivo de Entrada

Tu archivo `.txt` debe tener esta estructura:

```
TÍTULO DEL LIBRO
Autor: Nombre del Autor

ÍNDICE
$PRIMERA OBRA (1920)
$SEGUNDA OBRA (1922)
$TERCERA OBRA (1925)
FIN DEL ÍNDICE

[CONTENIDO DE LAS OBRAS]

PRIMERA OBRA

[Texto de la primera obra...]

SEGUNDA OBRA

[Texto de la segunda obra...]
```

**Requisitos:**
- Sección `ÍNDICE` ... `FIN DEL ÍNDICE`
- Marcador `$` antes de cada título en índice
- Año entre paréntesis `(YYYY)` opcional
- Títulos de obras deben aparecer en el contenido

---

## 🎉 ¡Listo!

Ahora tienes todo lo necesario para generar audiolibros sin ayuda.

**Comando más común:**
```bash
python -m modules.tts.cli process-all \
  outputs/manifests/tu-libro_manifest.json \
  --output outputs/tu-autor \
  --workers 1 \
  --start-from 1
```

**Para dudas técnicas:** Ver `.github/instructions/project-reference.instructions.md`

---

**Última actualización:** Enero 2025  
**Versión:** 1.0  
**Licencia:** MIT (Piper TTS), Proprietary (código del proyecto)
