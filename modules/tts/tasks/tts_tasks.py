from infrastructure.celery.celeryconfig import app
from modules.tts.domain.core.tts_engine import TTSEngine
from modules.tts.domain.audio_merger import ChapterMerger
from modules.tts.storage.minio_client import MinIOClient
from pathlib import Path
from typing import List


@app.task(name='tts.synthesize_chunk')
def synthesize_chunk(
    text: str,
    chunk_id: str,
    language: str = "es",
    speaker_wav: str = None
) -> str:
    """Generate audio for single text chunk."""
    engine = TTSEngine(language=language)
    
    output_dir = Path("outputs/temp/chunks")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    output_path = output_dir / f"{chunk_id}.wav"
    
    success = engine.synthesize(
        text=text,
        output_path=str(output_path),
        speaker_wav=speaker_wav
    )
    
    if success:
        return str(output_path)
    
    raise Exception(f"TTS failed for chunk {chunk_id}")


@app.task(name='tts.merge_chapter')
def merge_chapter(
    chunk_paths: List[str],
    chapter_name: str,
    output_bucket: str = None
) -> str:
    """Merge audio chunks into chapter file."""
    merger = ChapterMerger()
    
    output_dir = Path("outputs/temp")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    output_path = output_dir / f"{chapter_name}.mp3"
    
    success = merger.merge_chapter(
        chunk_paths=chunk_paths,
        output_path=str(output_path)
    )
    
    if not success:
        raise Exception(f"Merge failed: {chapter_name}")
    
    if output_bucket:
        storage = MinIOClient()
        storage.upload_file(
            str(output_path),
            f"{chapter_name}.mp3",
            output_bucket
        )
    
    return str(output_path)
