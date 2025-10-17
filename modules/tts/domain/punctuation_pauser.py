"""
Punctuation Pauser - Add RAE-compliant pauses.
"""
import re


class PunctuationPauser:
    """Insert pauses for Spanish punctuation marks."""
    
    PAUSES = {
        ',': 0.5,      # Coma (RAE: pausa breve)
        ';': 0.8,      # Punto y coma (RAE: pausa media)
        ':': 0.8,      # Dos puntos (RAE: pausa media)
        '.': 1.0,      # Punto seguido (RAE: pausa larga)
        '...': 1.2,    # Puntos suspensivos (RAE: pausa prolongada)
        '?': 1.0,      # Interrogación (RAE: pausa larga)
        '!': 1.0,      # Exclamación (RAE: pausa larga)
        '—': 0.6,      # Guión largo (RAE: pausa breve-media)
        '(': 0.4,      # Paréntesis abierto
        ')': 0.4,      # Paréntesis cerrado
    }
    
    def add_pauses(self, text: str) -> str:
        """Add SSML-style pauses after punctuation."""
        result = text
        
        # Handle ellipsis FIRST (before other punctuation)
        # Replace ... with break marker
        result = re.sub(r'\.\.\.', '<break:0.8>', result)
        
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
        
        Conservative approach: only emphasize key words,
        don't duplicate punctuation (causes audio breaks).
        """
        # QUESTIONS: Emphasize question words only
        question_words = [
            r'\b(qué|quién|quiénes|cuál|cuáles|cuándo)',
            r'\b(dónde|cómo|por qué|para qué)',
            r'\b(cuánto|cuánta|cuántos|cuántas|adónde)'
        ]
        
        for pattern in question_words:
            text = re.sub(
                pattern,
                lambda m: m.group(0).upper(),
                text,
                flags=re.IGNORECASE
            )
        
        # EXCLAMATIONS: Emphasize interjections
        # Pattern: ¡word! -> ¡WORD!
        text = re.sub(
            r'¡([^!]{1,15})!',
            lambda m: f"¡{m.group(1).upper()}!",
            text
        )
        
        return text
    
    def _get_pause(self, punct: str, spacing: str = ' ') -> str:
        """Get pause marker for punctuation."""
        duration = self.PAUSES.get(punct, 0.3)
        space = ' ' if spacing else ''
        return f"{punct}<break:{duration}>{space}"
    
    def convert_to_piper_format(self, text: str) -> str:
        """Convert break markers to periods for Piper.
        
        Piper pauses naturally at periods. We add extra periods
        for longer pauses based on RAE recommendations:
        - 0.4-0.5s = 1-2 periods  (comma, parenthesis)
        - 0.6-0.8s = 3-4 periods  (semicolon, colon, dash)
        - 1.0s     = 5 periods    (period, question, exclamation)
        - 1.2s     = 6 periods    (ellipsis)
        - 2.0s+    = silence chunk (title, paragraph)
        """
        # Map durations to period counts (RAE-compliant)
        period_map = {
            '0.4': '..',
            '0.5': '..',
            '0.6': '...',
            '0.8': '....',
            '1.0': '.....',
            '1.2': '......',
        }
        
        result = text
        for duration, periods in period_map.items():
            result = result.replace(
                f'<break:{duration}>',
                f' {periods} '
            )
        
        # Long silences (>=2s) stay as <silence:X>
        # for chunk separation
        result = re.sub(
            r'<break:([2-9]\d*\.?\d*)>',
            r'<silence:\1>',
            result
        )
        
        return result
