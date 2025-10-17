from typing import Dict
from .context_analyzer import ContextType


class SynthesisParams:
    """Synthesis parameters for Piper TTS."""
    
    def __init__(
        self, noise_scale: float,
        noise_w_scale: float
    ):
        self.noise_scale = noise_scale
        self.noise_w_scale = noise_w_scale


class SynthesisOptimizer:
    """
    Dynamic expressiveness adjustment.
    Higher variance = more expressive/natural.
    Speed is NOT modified (controlled by user).
    """
    
    CONTEXT_PARAMS: Dict[ContextType, SynthesisParams] = {
        "question": SynthesisParams(0.75, 0.85),
        "exclamation": SynthesisParams(0.8, 0.9),
        "dialogue": SynthesisParams(0.72, 0.82),
        "narrative": SynthesisParams(0.667, 0.8),
        "pause": SynthesisParams(0.5, 0.5)
    }
    
    def optimize(
        self, context: ContextType
    ) -> SynthesisParams:
        """Get optimal parameters for context."""
        return self.CONTEXT_PARAMS.get(
            context, self.CONTEXT_PARAMS["narrative"]
        )
