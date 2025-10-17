import numpy as np
from scipy import signal


class AudioFilters:
    """Professional audio filters for TTS."""
    
    def __init__(self, sample_rate: int = 22050):
        self.sample_rate = sample_rate
    
    def spectral_boost(self, audio: np.ndarray) -> np.ndarray:
        """High-shelf boost for clarity (3-8kHz)."""
        nyq = self.sample_rate / 2
        b, a = signal.butter(2, 3000/nyq, 'high')
        highs = signal.filtfilt(b, a, audio)
        return audio + (highs * 0.15)
    
    def add_presence(self, audio: np.ndarray) -> np.ndarray:
        """Vocal presence boost (1-4kHz)."""
        nyq = self.sample_rate / 2
        sos = signal.butter(
            2, [1000/nyq, 4000/nyq],
            'bandpass', output='sos'
        )
        presence = signal.sosfilt(sos, audio)
        return audio + (presence * 0.12)
    
    def soft_limiter(self, audio: np.ndarray) -> np.ndarray:
        """Soft-knee limiter with smooth transitions."""
        threshold = 0.8
        ratio = 4.0
        
        mask = np.abs(audio) > threshold
        compressed = audio.copy()
        
        excess = np.abs(audio[mask]) - threshold
        compressed[mask] = np.sign(audio[mask]) * (
            threshold + excess / ratio
        )
        
        # Smooth with Hann window
        kernel = np.hanning(11) / np.hanning(11).sum()
        smoothed = signal.convolve(
            compressed, kernel, mode='same'
        )
        
        return audio * 0.3 + smoothed * 0.7
    
    def normalize(
        self, audio: np.ndarray, target: float = 0.95
    ) -> np.ndarray:
        """Normalize to target peak level."""
        peak = np.abs(audio).max()
        return audio * (target / peak) if peak > 0 else audio
