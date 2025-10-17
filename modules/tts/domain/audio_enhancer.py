import numpy as np
import wave
from pathlib import Path
from .prosody_enhancer import ProsodyEnhancer
from .intelligent_deesser import IntelligentDeEsser
from .audio_filters import AudioFilters


class AudioEnhancer:
    """
    Modern TTS audio processor using community
    best practices for maximum naturalness.
    """
    
    def __init__(self):
        self.sample_rate = 22050
        self.prosody_enhancer = ProsodyEnhancer()
        self.deesser = IntelligentDeEsser()
        self.filters = AudioFilters()
    
    def enhance(
        self, 
        input_path: str, 
        output_path: str = None,
        add_prosody: bool = True
    ) -> str:
        """Apply modern enhancement pipeline."""
        with wave.open(input_path, 'rb') as wf:
            params = wf.getparams()
            frames = wf.readframes(params.nframes)
            self.sample_rate = params.framerate
        
        samples = np.frombuffer(frames, dtype=np.int16)
        audio = samples.astype(np.float32) / 32768.0
        
        # Modern enhancement chain
        enhanced = self.filters.spectral_boost(audio)
        enhanced = self.deesser.process(enhanced)
        enhanced = self.filters.add_presence(enhanced)
        
        if add_prosody:
            enhanced = self.prosody_enhancer.enhance(
                enhanced,
                add_micro_timing=True
            )
        
        enhanced = self.filters.soft_limiter(enhanced)
        enhanced = self.filters.normalize(enhanced)
        
        # Convert back to int16
        samples_out = (enhanced * 32767).astype(np.int16)
        
        output = output_path or input_path
        with wave.open(output, 'wb') as wf:
            wf.setparams(params)
            wf.writeframes(samples_out.tobytes())
        
        return output
