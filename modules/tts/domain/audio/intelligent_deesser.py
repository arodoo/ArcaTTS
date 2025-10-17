import numpy as np
from scipy import signal


class IntelligentDeEsser:
    """
    Adaptive de-esser using spectral analysis.
    Reduces sibilance (5-10kHz) without loss.
    """
    
    def __init__(self, sample_rate: int = 22050):
        self.sample_rate = sample_rate
        self.freq_min = 5000
        self.freq_max = 10000
        self.threshold_db = -20
        self.reduction_db = 6
    
    def process(self, audio: np.ndarray) -> np.ndarray:
        """Apply intelligent de-essing."""
        mask = self._detect(audio)
        return self._reduce(audio, mask) if np.any(mask) else audio
    
    def _detect(self, audio: np.ndarray) -> np.ndarray:
        """Detect frames with excess sibilance."""
        f, t, stft = signal.stft(
            audio, fs=self.sample_rate, nperseg=1024
        )
        
        idx = np.where(
            (f >= self.freq_min) & (f <= self.freq_max)
        )[0]
        
        energy = np.sum(np.abs(stft[idx, :]) ** 2, axis=0)
        thresh = 10 ** (self.threshold_db / 10)
        return energy > thresh
    
    def _reduce(
        self, audio: np.ndarray, mask: np.ndarray
    ) -> np.ndarray:
        """Apply frequency-selective reduction."""
        f, t, stft = signal.stft(
            audio, fs=self.sample_rate, nperseg=1024
        )
        
        idx = np.where(
            (f >= self.freq_min) & (f <= self.freq_max)
        )[0]
        
        factor = 10 ** (-self.reduction_db / 20)
        
        for frame in np.where(mask)[0]:
            if frame < stft.shape[1]:
                stft[idx, frame] *= factor
        
        _, proc = signal.istft(stft, fs=self.sample_rate)
        
        diff = len(audio) - len(proc)
        if diff > 0:
            proc = np.pad(proc, (0, diff))
        elif diff < 0:
            proc = proc[:len(audio)]
        
        return proc.astype(np.float32)
