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
        
        result = re.sub(r'\.\.\.', '...<break:0.8>', result)
        result = re.sub(r'([.?!;:,—])\s+', 
                       lambda m: self._get_pause(m.group(1)), 
                       result)
        
        result = re.sub(r'\n\n+', '<break:1.0>\n', result)
        
        return result
    
    def _get_pause(self, punct: str) -> str:
        """Get pause marker for punctuation."""
        duration = self.PAUSES.get(punct, 0.3)
        return f"{punct}<break:{duration}> "
    
    def convert_to_piper_format(self, text: str) -> str:
        """Convert break markers to actual pauses.
        
        Piper doesn't support SSML, so we add explicit
        silence using repeated periods for natural pauses.
        RAE timing: coma 0.3s, punto 0.7s, etc.
        """
        pause_map = {
            '<break:0.3>': ' ',
            '<break:0.4>': '. ',
            '<break:0.5>': '.. ',
            '<break:0.6>': '... ',
            '<break:0.7>': '.... ',
            '<break:0.8>': '..... ',
            '<break:1.0>': '....... ',
        }
        
        result = text
        for marker, replacement in pause_map.items():
            result = result.replace(marker, replacement)
        
        return result
