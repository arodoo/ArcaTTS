from typing import Optional
from pathlib import Path
from piper import PiperVoice
from piper.config import SynthesisConfig
import wave
from .context_analyzer import ContextAnalyzer
from .synthesis_optimizer import SynthesisOptimizer


class TTSEngine:
    """Piper TTS wrapper for audio generation."""
    
    MODEL_PATHS = {
        "es": "models/piper/es_MX-claude-high.onnx",
        "es_mx": "models/piper/es_MX-claude-high.onnx",
        "es_es": "models/piper/es_ES-sharvard-medium.onnx",
        "en": "models/piper/en_US-lessac-medium.onnx",
        "pt": "models/piper/pt_BR-faber-medium.onnx"
    }
    
    def __init__(
        self, 
        language: str = "es",
        enhance_quality: bool = True
    ):
        self.language = language
        self.voice = None
        self.enhance_quality = enhance_quality
        self.context_analyzer = ContextAnalyzer()
        self.optimizer = SynthesisOptimizer()
    
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
        output_path: str,
        speaker_wav: Optional[str] = None,
        speed: float = 1.0,
        sentence_silence: float = 0.2
    ) -> bool:
        """
        Generate audio with context-aware synthesis.
        Uses dynamic parameters for naturalness.
        """
        if not self.voice:
            self.load_model()
        
        try:
            Path(output_path).parent.mkdir(
                parents=True,
                exist_ok=True
            )
            
            # Analyze text context
            context = self.context_analyzer.analyze(text)
            params = self.optimizer.optimize(context)
            
            # Configure with optimized parameters
            # NOTE: length_scale should be 1.0/speed for normal pacing
            # Context params only adjust noise (expressiveness)
            config = SynthesisConfig(
                length_scale=1.0 / speed,
                noise_scale=params.noise_scale,
                noise_w_scale=params.noise_w_scale,
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
            
            # Post-process for quality
            if self.enhance_quality:
                self._enhance_audio(output_path)
            
            return True
        except Exception as e:
            print(f"TTS Error: {e}")
            return False
    
    def _enhance_audio(self, audio_path: str) -> None:
        """Apply audio enhancements."""
        try:
            from modules.tts.domain.audio_enhancer import (
                AudioEnhancer
            )
            enhancer = AudioEnhancer()
            enhancer.enhance(audio_path, audio_path)
        except Exception as e:
            print(f"Enhancement warning: {e}")

