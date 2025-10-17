"""
Punctuation Pauser with Manual Equalizer Configuration.
"""
import re
from modules.tts.domain.text.pause_config import PauseConfig


class PunctuationPauser:
    """
    Converts punctuation to silence markers.
    
    Uses PauseConfig equalizer for timing control.
    """
    
    def __init__(self):
        """Initialize with configured pause durations."""
        self.config = PauseConfig
    
    def add_pauses(self, text: str) -> str:
        """
        Replace punctuation with <silence:X> markers.
        
        Uses safe temporary markers without punctuation.
        Preserves §PAUSEXXXX§ markers from other modules.
        
        Args:
            text: Input text with punctuation
            
        Returns:
            Text with punctuation converted to silence markers
        """
        # Convert punctuation to temp markers
        text = text.replace('...', '§ELLIPSIS§')
        text = text.replace('—', '§EMDASH§')
        text = text.replace('–', '§ENDASH§')
        text = text.replace(';', '§SEMICOLON§')
        text = text.replace(':', '§COLON§')
        text = text.replace(',', '§COMMA§')
        text = text.replace('¿', '')
        text = text.replace('¡', '')
        text = text.replace('?', '§QUESTION§')
        text = text.replace('!', '§EXCLAMATION§')
        text = text.replace('.', '§PERIOD§')
        
        # Convert temp markers to silence tags
        text = text.replace('§ELLIPSIS§', 
            f"<silence:{self.config.get_pause_seconds('...')}>")
        text = text.replace('§EMDASH§', 
            f"<silence:{self.config.get_pause_seconds('—')}>")
        text = text.replace('§ENDASH§', 
            f"<silence:{self.config.get_pause_seconds('–')}>")
        text = text.replace('§SEMICOLON§', 
            f"<silence:{self.config.get_pause_seconds(';')}>")
        text = text.replace('§COLON§', 
            f"<silence:{self.config.get_pause_seconds(':')}>")
        text = text.replace('§COMMA§', 
            f"<silence:{self.config.get_pause_seconds(',')}>")
        text = text.replace('§QUESTION§', 
            f"<silence:{self.config.get_pause_seconds('?')}>")
        text = text.replace('§EXCLAMATION§', 
            f"<silence:{self.config.get_pause_seconds('!')}>")
        text = text.replace('§PERIOD§', 
            f"<silence:{self.config.get_pause_seconds('.')}>")
        
        # Convert structural pause markers (from title/roman)
        text = text.replace('§PAUSE2000§', '<silence:2.0>')
        text = text.replace('§PAUSE500§', '<silence:0.5>')
        
        return text
    
    def convert_to_piper_format(self, text: str) -> str:
        """
        Legacy compatibility method.
        
        Now conversion happens in add_pauses().
        
        Args:
            text: Input text
            
        Returns:
            Unchanged text
        """
        return text
