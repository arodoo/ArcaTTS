# Project Structure

```
AudioLibros/01/
│
├── boocks/                      # Input text files
│   └── franz-kafka.txt          # Complete works (53K lines)
│
├── outputs/                     # Generated audio files
│   ├── 01-Book_Title/
│   │   ├── 01-Chapter_1.mp3
│   │   └── 02-Chapter_2.mp3
│   └── ...
│
├── domain/                      # Core business logic (DDD)
│   ├── __init__.py
│   ├── models.py                # Book, Chapter, BookType
│   ├── parser.py                # BookStructureParser
│   ├── text_processor.py        # Text chunking (TODO)
│   └── tts_engine.py            # XTTS-v2 wrapper (TODO)
│
├── tasks/                       # Celery task definitions
│   ├── __init__.py
│   ├── parsing_tasks.py         # parse_book_structure (TODO)
│   ├── tts_tasks.py             # synthesize_audio_chunk (TODO)
│   └── merge_tasks.py           # merge_chapter_audio (TODO)
│
├── storage/                     # MinIO client layer
│   ├── __init__.py
│   └── minio_client.py          # S3 operations (TODO)
│
├── tests/                       # Test suite
│   ├── __init__.py
│   ├── test_parser.py           # Parser tests (TODO)
│   └── test_tts.py              # TTS tests (TODO)
│
├── cli.py                       # CLI entry point (TODO)
├── config.py                    # Configuration
├── celeryconfig.py              # Celery setup (TODO)
│
├── requirements.txt             # Dependencies
├── setup.sh                     # Environment setup
├── .env.example                 # Config template
├── .env                         # Local config (git-ignored)
│
├── test_parser.py               # Quick parser test
└── README.md                    # Project documentation
```

## Layer Responsibilities

### Domain Layer (`domain/`)
**Pure business logic, no external dependencies**

- `models.py`: Book, Chapter data structures
- `parser.py`: Text structure analysis
- `text_processor.py`: Smart text chunking
- `tts_engine.py`: TTS abstraction

**Rules:**
- Max 60 lines per file
- No I/O operations
- No framework dependencies

### Tasks Layer (`tasks/`)
**Celery async operations**

- `parsing_tasks.py`: Extract book structure
- `tts_tasks.py`: Generate audio chunks
- `merge_tasks.py`: Combine audio files

**Rules:**
- Each task = 1 responsibility
- Retry logic for failures
- Progress tracking via Redis

### Storage Layer (`storage/`)
**External persistence**

- `minio_client.py`: S3-compatible operations
- Bucket management
- File upload/download

## Current Status

✅ **Completed:**
- Project structure
- Configuration system
- Domain models (Book, Chapter)
- Basic parser (structure detection)
- Requirements & setup script

🚧 **In Progress:**
- Chapter content extraction

⏳ **TODO:**
- Text chunking engine
- TTS integration
- Celery tasks
- CLI interface
- MinIO setup
- Redis configuration
