import os
from dataclasses import dataclass
from typing import Optional
from dotenv import load_dotenv

load_dotenv()


@dataclass
class RedisConfig:
    host: str = os.getenv("REDIS_HOST", "localhost")
    port: int = int(os.getenv("REDIS_PORT", "6379"))
    db: int = int(os.getenv("REDIS_DB", "0"))
    
    @property
    def url(self) -> str:
        return f"redis://{self.host}:{self.port}/{self.db}"


@dataclass
class MinIOConfig:
    endpoint: str = os.getenv(
        "MINIO_ENDPOINT", 
        "localhost:9000"
    )
    access_key: str = os.getenv(
        "MINIO_ACCESS_KEY", 
        "minioadmin"
    )
    secret_key: str = os.getenv(
        "MINIO_SECRET_KEY", 
        "minioadmin"
    )
    secure: bool = os.getenv(
        "MINIO_SECURE", 
        "false"
    ).lower() == "true"
    
    bucket_chunks: str = "audio-chunks"
    bucket_outputs: str = "final-outputs"
    bucket_metadata: str = "book-metadata"


@dataclass
class TTSConfig:
    model_name: str = "tts_models/multilingual/multi-dataset/xtts_v2"
    device: str = os.getenv("TTS_DEVICE", "cuda")
    language: str = os.getenv("DEFAULT_LANGUAGE", "es")
    chunk_size: int = int(os.getenv("CHUNK_SIZE", "500"))


redis_config = RedisConfig()
minio_config = MinIOConfig()
tts_config = TTSConfig()
