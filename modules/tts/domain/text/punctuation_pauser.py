"""
Punctuation Pauser - Minimal text cleanup.
"""
import re


class PunctuationPauser:
    """Minimal text processing for Piper TTS."""
    
    def add_pauses(self, text: str) -> str:
        """
        Minimal processing - let Piper handle pauses naturally.
        Only add prosodic markers for questions/exclamations.
        """
        result = text
        
        # Add prosodic markers for expressiveness
        result = self._add_prosodic_markers(result)
        
        return result
    
    def _add_prosodic_markers(self, text: str) -> str:
        """Add emphasis for questions and exclamations.
        
        Conservative approach: only emphasize key words.
        """
        # QUESTIONS: Emphasize question words
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
        
        # EXCLAMATIONS: Emphasize short exclamations
        text = re.sub(
            r'¡([^!]{1,15})!',
            lambda m: f"¡{m.group(1).upper()}!",
            text
        )
        
        return text
    
    def convert_to_piper_format(self, text: str) -> str:
        """
        No conversion needed - Piper handles punctuation natively.
        Only mark long silences (>=2s) for chunk separation.
        """
        return text
