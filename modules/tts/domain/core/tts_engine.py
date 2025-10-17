from typing import Optional
from pathlib import Path
from piper import PiperVoice
from piper.config import SynthesisConfig
import wave


class TTSEngine:
    """
    Simple Piper TTS wrapper.
    Focused on quality and correct pacing.
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
        Generate audio from text.
        
        Uses slower speed (1.2) for better comprehension.
        Quality-focused parameters.
        """
        if not self.voice:
            self.load_model()
        
        try:
            Path(output_path).parent.mkdir(
                parents=True,
                exist_ok=True
            )
            
            # Simple, quality-focused configuration
            config = SynthesisConfig(
                length_scale=1.2,      # Slower for clarity
                noise_scale=0.667,     # Natural variance
                noise_w_scale=0.8,     # Smooth transitions
                normalize_audio=True,
                volume=1.0
            )
            
            chunks = list(self.voice.synthesize(text, config))
            audio_data = b''.join([
                chunk.audio_int16_bytes 
                for chunk in chunks
            ])
            
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
    
    def _enhance_audio(self, audio_path: str) -> None:
        """Apply audio enhancements."""
        try:
            from ..audio.audio_enhancer import AudioEnhancer
            enhancer = AudioEnhancer()
            enhancer.enhance(audio_path, audio_path)
        except Exception as e:
            print(f"Enhancement warning: {e}")

