"""
Silence Generator - Add pauses to audio.
"""
import numpy as np
import wave
from pathlib import Path


class SilenceGenerator:
    """Generate silence segments for audio."""
    
    def __init__(self, sample_rate: int = 22050):
        self.sample_rate = sample_rate
    
    def generate_silence(
        self, 
        duration_seconds: float,
        output_path: str
    ) -> str:
        """Create silence WAV file."""
        num_samples = int(self.sample_rate * duration_seconds)
        silence = np.zeros(num_samples, dtype=np.int16)
        
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        
        with wave.open(output_path, 'wb') as f:
            f.setnchannels(1)
            f.setsampwidth(2)
            f.setframerate(self.sample_rate)
            f.writeframes(silence.tobytes())
        
        return output_path
    
    def insert_pause_after_title(
        self, 
        text: str,
        pause_seconds: float = 2.0
    ) -> str:
        """Add pause marker after title."""
        lines = text.split('\n')
        
        if not lines:
            return text
        
        title = lines[0].strip()
        rest = '\n'.join(lines[1:])
        
        pause_marker = f"<silence:{pause_seconds}>"
        
        return f"{title}\n{pause_marker}\n{rest}"
