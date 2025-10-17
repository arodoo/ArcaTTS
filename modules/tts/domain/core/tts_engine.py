from typing import Optional
from pathlib import Path
from piper import PiperVoice
from piper.config import SynthesisConfig
import wave
import re
import numpy as np


class TTSEngine:
    """
    Simple Piper TTS wrapper.
    Processes <silence:X> markers for precise pauses.
    """
    
    MODEL_PATHS = {
        "es": "models/piper/es_MX-claude-high.onnx",
        "es_mx": "models/piper/es_MX-claude-high.onnx",
        "es_es": "models/piper/es_ES-sharvard-medium.onnx",
    }
    
    def __init__(self, language: str = "es_mx"):
        self.language = language
        self.voice = None
    
    def load_model(self) -> None:
        """Load Piper voice model."""
        model_path = Path(self.MODEL_PATHS.get(
            self.language,
            self.MODEL_PATHS["es"]
        ))
        
        config_path = model_path.with_suffix('.onnx.json')
        
        if not model_path.exists():
            raise FileNotFoundError(
                f"Model not found: {model_path}"
            )
        
        self.voice = PiperVoice.load(
            str(model_path),
            use_cuda=False,
            config_path=str(config_path)
        )
    
    def synthesize(
        self,
        text: str,
        output_path: str
    ) -> bool:
        """
        Generate audio from text with silence markers.
        
        Processes <silence:X> markers as real silence.
        Uses slower speed (1.2) for clarity.
        """
        if not self.voice:
            self.load_model()
        
        try:
            Path(output_path).parent.mkdir(
                parents=True,
                exist_ok=True
            )
            
            # Split text on silence markers
            pattern = r'<silence:([\d.]+)>'
            parts = re.split(pattern, text)
            
            audio_segments = []
            i = 0
            
            while i < len(parts):
                part = parts[i]
                
                # Check if this is a duration
                if i > 0 and re.match(r'[\d.]+$', part):
                    # Generate silence
                    duration = float(part)
                    silence_bytes = self._generate_silence(duration)
                    audio_segments.append(silence_bytes)
                    i += 1
                else:
                    # Generate speech
                    if part.strip():
                        speech_bytes = self._synthesize_text(part.strip())
                        audio_segments.append(speech_bytes)
                    i += 1
            
            # Combine all segments
            audio_data = b''.join(audio_segments)
            
            with wave.open(output_path, 'wb') as f:
                f.setnchannels(1)
                f.setsampwidth(2)
                f.setframerate(self.voice.config.sample_rate)
                f.writeframes(audio_data)
            
            # Apply audio enhancement
            self._enhance_audio(output_path)
            
            return True
            
        except Exception as e:
            print(f"TTS Error: {e}")
            return False
    
    def _synthesize_text(self, text: str) -> bytes:
        """Generate speech audio for text."""
        config = SynthesisConfig(
            length_scale=1.2,
            noise_scale=0.667,
            noise_w_scale=0.8,
            normalize_audio=True,
            volume=1.0
        )
        
        chunks = list(self.voice.synthesize(text, config))
        return b''.join([
            chunk.audio_int16_bytes 
            for chunk in chunks
        ])
    
    def _generate_silence(self, duration: float) -> bytes:
        """Generate silence audio."""
        sample_rate = self.voice.config.sample_rate
        num_samples = int(sample_rate * duration)
        silence = np.zeros(num_samples, dtype=np.int16)
        return silence.tobytes()
    
    def _enhance_audio(self, audio_path: str) -> None:
        """Apply audio enhancements."""
        try:
            from ..audio.audio_enhancer import AudioEnhancer
            enhancer = AudioEnhancer()
            enhancer.enhance(audio_path, audio_path)
        except Exception as e:
            print(f"Enhancement warning: {e}")

