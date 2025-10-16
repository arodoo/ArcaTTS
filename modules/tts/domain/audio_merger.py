from pathlib import Path
from typing import List
from pydub import AudioSegment


class AudioMerger:
    """Merge audio chunks into final output."""
    
    def __init__(self, format: str = "mp3"):
        self.format = format
    
    def merge_chunks(
        self,
        chunk_paths: List[str],
        output_path: str
    ) -> bool:
        """Combine audio files sequentially."""
        try:
            combined = self._load_and_combine(chunk_paths)
            self._export_audio(combined, output_path)
            return True
        except Exception as e:
            print(f"Merge error: {e}")
            return False
    
    def _load_and_combine(
        self, 
        paths: List[str]
    ) -> AudioSegment:
        """Load and concatenate audio chunks."""
        combined = AudioSegment.empty()
        
        for path in paths:
            chunk = AudioSegment.from_file(path)
            combined += chunk
        
        return combined
    
    def _export_audio(
        self,
        audio: AudioSegment,
        output_path: str
    ) -> None:
        """Export merged audio to file."""
        Path(output_path).parent.mkdir(
            parents=True, 
            exist_ok=True
        )
        
        audio.export(
            output_path,
            format=self.format,
            bitrate="128k"
        )


class ChapterMerger:
    """Merge chapter chunks with metadata."""
    
    def __init__(self):
        self.merger = AudioMerger()
    
    def merge_chapter(
        self,
        chunk_paths: List[str],
        output_path: str,
        normalize: bool = True
    ) -> bool:
        """Merge with optional normalization."""
        if normalize:
            chunk_paths = self._normalize_chunks(chunk_paths)
        
        return self.merger.merge_chunks(chunk_paths, output_path)
    
    def _normalize_chunks(
        self, 
        paths: List[str]
    ) -> List[str]:
        """Normalize audio levels (placeholder)."""
        return paths
