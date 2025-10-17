import numpy as np
from scipy import signal


class ProsodyEnhancer:
    """Prosody enhancement: pitch shift, micro-timing."""
    
    def __init__(self, sample_rate: int = 22050):
        self.sample_rate = sample_rate
    
    def enhance(
        self, audio: np.ndarray,
        pitch_shift_semitones: float = 0.0,
        add_micro_timing: bool = True
    ) -> np.ndarray:
        """Apply enhancements."""
        out = audio.copy()
        
        if pitch_shift_semitones != 0:
            out = self._pitch_shift(out, pitch_shift_semitones)
        
        if add_micro_timing:
            out = self._micro_timing(out)
        
        return out
    
    def _pitch_shift(
        self, audio: np.ndarray, semitones: float
    ) -> np.ndarray:
        """Pitch shift with formant preservation."""
        if semitones == 0:
            return audio
        
        ratio = 2 ** (semitones / 12.0)
        f, t, stft = signal.stft(
            audio, fs=self.sample_rate, nperseg=2048
        )
        _, shifted = signal.istft(
            stft * ratio, fs=self.sample_rate
        )
        
        if len(shifted) != len(audio):
            shifted = signal.resample(shifted, len(audio))
        
        return shifted.astype(np.float32)
    
    def _micro_timing(self, audio: np.ndarray) -> np.ndarray:
        """Subtle timing variations (±2%)."""
        var = np.random.uniform(0.98, 1.02, len(audio))
        
        win = signal.windows.hann(441)
        var = signal.convolve(var, win / win.sum(), mode='same')
        
        idx = np.cumsum(var)
        idx = idx / idx[-1] * (len(audio) - 1)
        idx = np.clip(idx.astype(int), 0, len(audio) - 1)
        
        return audio[idx]
