"""
PAUSE EQUALIZER - Manual Configuration
======================================

Adjust pause durations (in milliseconds) for Spanish punctuation.
Based on RAE (Real Academia Española) recommendations.

Simply edit the values in PAUSE_DURATIONS to customize.
All changes apply immediately without touching other code.

RAE Guidelines:
- Pausa breve (brief):       200-400ms  (comma, parenthesis)
- Pausa media (medium):       500-800ms  (semicolon, colon)
- Pausa larga (long):         800-1200ms (period, question, exclamation)
- Pausa muy larga (very long): 1500-2500ms (paragraph, title)
"""


class PauseConfig:
    """
    Centralized pause duration configuration.
    All values in milliseconds (ms).
    """
    
    # ============================================================
    # PAUSE DURATIONS (Edit these values directly)
    # ============================================================
    
    PAUSE_DURATIONS = {
        # BASIC PUNCTUATION (Puntuación básica)
        ',':   500,   # Comma (Coma) - RAE: pausa breve
        '.':   1000,  # Period (Punto) - RAE: pausa larga
        ';':   800,   # Semicolon (Punto y coma) - RAE: pausa media
        ':':   800,   # Colon (Dos puntos) - RAE: pausa media
        '...': 1200,  # Ellipsis (Puntos suspensivos) - RAE: pausa prolongada
        
        # QUESTIONS & EXCLAMATIONS (Interrogación y exclamación)
        '?':   1000,  # Question mark (Interrogación) - RAE: pausa larga
        '!':   1000,  # Exclamation mark (Exclamación) - RAE: pausa larga
        '¿':   0,     # Opening question (no pause before)
        '¡':   0,     # Opening exclamation (no pause before)
        
        # DASHES & HYPHENS (Guiones y rayas)
        '—':   600,   # Em dash (Raya) - RAE: pausa breve-media
        '–':   400,   # En dash (Guión largo) - pausa breve
        '-':   0,     # Hyphen (Guión corto) - no pause
        
        # PARENTHESES & BRACKETS (Paréntesis y corchetes)
        '(':   400,   # Opening parenthesis - pausa breve
        ')':   400,   # Closing parenthesis - pausa breve
        '[':   400,   # Opening bracket
        ']':   400,   # Closing bracket
        '{':   300,   # Opening brace
        '}':   300,   # Closing brace
        
        # QUOTES (Comillas)
        '"':   300,   # Double quote
        "'":   0,     # Single quote (apostrophe) - no pause
        '«':   300,   # Opening guillemet
        '»':   300,   # Closing guillemet
        
        # SPECIAL (Especiales)
        '/':   200,   # Slash (Barra) - pausa muy breve
        '\\':  200,   # Backslash
        '&':   200,   # Ampersand
        '@':   0,     # At sign - no pause
        '#':   0,     # Hash - no pause
        '*':   300,   # Asterisk
        '+':   200,   # Plus
        '=':   200,   # Equals
    }
    
    # ============================================================
    # STRUCTURAL PAUSES (Don't edit - for chunking only)
    # ============================================================
    
    STRUCTURAL_PAUSES = {
        'title':     2000,  # After title
        'paragraph': 1500,  # Between paragraphs
        'chapter':   2500,  # Between chapters
        'roman':     2000,  # After Roman numerals
    }
    
    # ============================================================
    # CONVERSION METHOD
    # ============================================================
    
    @classmethod
    def get_pause_ms(cls, punctuation: str) -> int:
        """
        Get pause duration in milliseconds for punctuation.
        
        Args:
            punctuation: Single punctuation character
            
        Returns:
            Duration in milliseconds (0 = no pause)
        """
        return cls.PAUSE_DURATIONS.get(punctuation, 0)
    
    @classmethod
    def get_pause_seconds(cls, punctuation: str) -> float:
        """
        Get pause duration in seconds for punctuation.
        
        Args:
            punctuation: Single punctuation character
            
        Returns:
            Duration in seconds (0.0 = no pause)
        """
        ms = cls.get_pause_ms(punctuation)
        return ms / 1000.0
    
    @classmethod
    def ms_to_periods(cls, milliseconds: int) -> str:
        """
        Convert milliseconds to Piper periods.
        
        Piper pauses ~200ms per period naturally.
        
        Args:
            milliseconds: Pause duration in ms
            
        Returns:
            String of periods (e.g., "..." for 600ms)
        """
        if milliseconds <= 0:
            return ''
        
        # Each period ≈ 200ms in Piper
        period_count = max(1, round(milliseconds / 200))
        return '.' * period_count
    
    @classmethod
    def get_all_punctuation(cls) -> list:
        """Get list of all configured punctuation marks."""
        return list(cls.PAUSE_DURATIONS.keys())
    
    @classmethod
    def print_config(cls):
        """Print current configuration (for debugging)."""
        print("=" * 60)
        print("CURRENT PAUSE CONFIGURATION")
        print("=" * 60)
        
        for punct, ms in sorted(
            cls.PAUSE_DURATIONS.items(),
            key=lambda x: x[1],
            reverse=True
        ):
            seconds = ms / 1000.0
            periods = cls.ms_to_periods(ms)
            print(f"  '{punct}' -> {ms:4d}ms ({seconds:.2f}s) [{periods}]")
        
        print("=" * 60)


# ============================================================
# USAGE EXAMPLES (for testing)
# ============================================================

if __name__ == "__main__":
    # Print current configuration
    PauseConfig.print_config()
    
    # Example: Get pause for comma
    comma_pause = PauseConfig.get_pause_seconds(',')
    print(f"\nComma pause: {comma_pause}s")
    
    # Example: Convert to periods
    periods = PauseConfig.ms_to_periods(800)
    print(f"800ms = '{periods}'")
