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
        '...': 0.8,    # Puntos suspensivos (legacy)
        '?': 0.7,      # Interrogación (increased)
        '!': 0.7,      # Exclamación (increased)
        '—': 0.4,      # Guión largo
        '(': 0.3,      # Paréntesis abierto
        ')': 0.3,      # Paréntesis cerrado
    }
    
    def add_pauses(self, text: str) -> str:
        """Add SSML-style pauses after punctuation."""
        result = text
        
        # Handle ellipsis: replace with silence marker
        # (periods cause audio distortion)
        result = re.sub(r'\.\.\.', '<silence:0.8>', result)
        
        # Dialogue dashes: -palabra- pattern
        # Match: space or start, dash, content, dash, space or end
        result = re.sub(
            r'(\s|^)(-[^-]+-)(\s|$)',
            r'\1<break:0.4>\2<break:0.4>\3',
            result
        )
        
        # Add prosodic markers for questions/exclamations
        # Spanish upside-down marks indicate rising intonation
        result = self._add_prosodic_markers(result)
        
        # Handle punctuation (including end of string)
        result = re.sub(r'([.?!;:,—])(\s+|$)', 
                       lambda m: self._get_pause(m.group(1), m.group(2)), 
                       result)
        
        return result
    
    def _add_prosodic_markers(self, text: str) -> str:
        """Add emphasis for questions and exclamations.
        
        Uses repetition and strategic spacing to signal
        rising intonation for Piper TTS engine.
        """
        # Question words get emphasis via repetition
        question_words = [
            r'\b(qué|quién|quiénes|cuál|cuáles|cuándo)',
            r'\b(dónde|cómo|por qué|para qué|cuánto|cuánta)',
            r'\b(cuántos|cuántas|adónde)'
        ]
        
        for pattern in question_words:
            # Add slight pause before question word
            text = re.sub(
                pattern,
                r' \1',
                text,
                flags=re.IGNORECASE
            )
        
        # Exclamation words get exclamatory marker
        exclamation_words = [
            r'\b(ay|oh|ah|eh|uf|vaya|caray|cielos)',
            r'\b(dios|santo|qué|cuánto|cuánta|cuántos)',
            r'\b(muy|tan|tanto|tanta)'
        ]
        
        for pattern in exclamation_words:
            # Emphasize within exclamations
            text = re.sub(
                f'¡([^!]*{pattern}[^!]*)!',
                r'¡\1!',
                text,
                flags=re.IGNORECASE
            )
        
        return text
    
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
