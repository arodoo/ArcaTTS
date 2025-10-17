import numpy as np
from scipy.signal import lfilter


class BreathInserter:
    """
    Inserts natural breathing sounds.
    Based on prosody research (150-300ms, -20dB).
    """
    
    def __init__(self, sample_rate: int = 22050):
        self.sample_rate = sample_rate
        self.duration_ms = 200
        self.amplitude = 0.03
    
    def create_breath(self) -> np.ndarray:
        """Generate natural breath sound."""
        n = int(self.sample_rate * self.duration_ms / 1000)
        
        # Pink noise (more natural)
        breath = self._pink_noise(n)
        
        # Apply envelope
        envelope = self._envelope(n)
        
        return (breath * envelope * self.amplitude
                ).astype(np.float32)
    
    def _pink_noise(self, samples: int) -> np.ndarray:
        """Generate pink noise (1/f spectrum)."""
        white = np.random.randn(samples)
        
        # Filter coefficients
        b = [0.049922035, -0.095993537, 0.050612699]
        a = [1.0, -2.494956002, 2.017265875]
        
        pink = lfilter(b, a, white)
        return pink / np.max(np.abs(pink))
    
    def _envelope(self, samples: int) -> np.ndarray:
        """Natural breath amplitude envelope."""
        attack_n = int(samples * 0.3)
        decay_n = samples - attack_n
        
        # Quick rise
        attack = np.linspace(0, 1, attack_n) ** 0.5
        
        # Slower fall
        decay = np.linspace(1, 0, decay_n) ** 2
        
        return np.concatenate([attack, decay])
