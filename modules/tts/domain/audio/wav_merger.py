"""
Native WAV Merger - No ffmpeg required.
"""
from pathlib import Path
from typing import List
import wave
import numpy as np


class WavMerger:
    """Merge WAV files using wave module."""
    
    def merge(
        self, 
        input_files: List[str], 
        output_file: str
    ) -> bool:
        """Concatenate WAV files."""
        try:
            data_chunks = []
            params = None
            
            for input_file in input_files:
                with wave.open(input_file, 'rb') as wav:
                    if params is None:
                        params = wav.getparams()
                    
                    frames = wav.readframes(wav.getnframes())
                    data_chunks.append(frames)
            
            Path(output_file).parent.mkdir(
                parents=True, 
                exist_ok=True
            )
            
            with wave.open(output_file, 'wb') as output:
                output.setparams(params)
                output.writeframes(b''.join(data_chunks))
            
            return True
            
        except Exception as e:
            print(f"Merge error: {e}")
            return False
