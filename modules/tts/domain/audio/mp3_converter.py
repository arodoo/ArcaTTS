"""
MP3 Converter - WAV to MP3 with cleanup.
"""
from pathlib import Path
from pydub import AudioSegment


class Mp3Converter:
    """Convert WAV to MP3 and manage temp files."""
    
    def __init__(self, bitrate: str = "128k"):
        self.bitrate = bitrate
    
    def convert(
        self, 
        wav_path: str, 
        mp3_path: str = None,
        cleanup: bool = True
    ) -> str:
        """Convert WAV to MP3."""
        wav_file = Path(wav_path)
        
        if mp3_path is None:
            mp3_path = wav_file.with_suffix('.mp3')
        else:
            mp3_path = Path(mp3_path)
        
        try:
            audio = AudioSegment.from_wav(str(wav_file))
            audio.export(
                str(mp3_path),
                format="mp3",
                bitrate=self.bitrate,
                parameters=["-q:a", "2"]
            )
            
            if cleanup and wav_file.exists():
                wav_file.unlink()
            
            return str(mp3_path)
            
        except Exception as e:
            print(f"MP3 conversion error: {e}")
            return None
    
    def cleanup_chunks(self, work_dir: Path) -> None:
        """Remove temporary WAV chunks."""
        for chunk in work_dir.glob("chunk_*.wav"):
            chunk.unlink()
