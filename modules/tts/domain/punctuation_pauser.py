"""
Punctuation Pauser - Add RAE-compliant pauses.
"""
import re


class PunctuationPauser:
    """Insert pauses for Spanish punctuation marks."""
    
    PAUSES = {
        ',': 0.3,      # Coma
        ';': 0.5,      # Punto y coma
        ':': 0.5,      # Dos puntos
        '.': 0.7,      # Punto seguido
        '...': 0.8,    # Puntos suspensivos
        '?': 0.6,      # Interrogación
        '!': 0.6,      # Exclamación
        '—': 0.4,      # Guión largo
        '(': 0.3,      # Paréntesis abierto
        ')': 0.3,      # Paréntesis cerrado
    }
    
    def add_pauses(self, text: str) -> str:
        """Add SSML-style pauses after punctuation."""
        result = text
        
        # Handle ellipsis first (before other periods)
        result = re.sub(r'\.\.\.', '...<break:0.8>', result)
        
        # Dialogue dashes: add pause after opening/closing
        # Pattern: -palabra... palabra-
        result = re.sub(r'-([¿¡])', r'<break:0.4>-\1', result)  # -¿
        result = re.sub(r'([?!])-', r'\1-<break:0.4>', result)  # ?-
        
        # Handle punctuation (including end of string)
        result = re.sub(r'([.?!;:,—])(\s+|$)', 
                       lambda m: self._get_pause(m.group(1), m.group(2)), 
                       result)
        
        return result
    
    def _get_pause(self, punct: str, spacing: str = ' ') -> str:
        """Get pause marker for punctuation."""
        duration = self.PAUSES.get(punct, 0.3)
        space = ' ' if spacing else ''
        return f"{punct}<break:{duration}>{space}"
    
    def convert_to_piper_format(self, text: str) -> str:
        """Convert break markers to silence chunks.
        
        Converts <break:X> to <silence:X> for proper
        WAV silence generation. Piper reads multiple 
        periods aloud, so we use silence chunks instead.
        """
        # Convert break markers to silence markers
        result = re.sub(
            r'<break:([\d.]+)>',
            r'<silence:\1>',
            text
        )
        
        return result
