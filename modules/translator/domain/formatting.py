"""
Formatting preservation helpers.
Extension for TranslationPostProcessor.
"""
import re


class FormattingPreserver:
    """Maintain text structure."""

    @staticmethod
    def preserve_formatting(
        original: str,
        translated: str
    ) -> str:
        """Match original text structure."""
        result = translated

        if original.startswith('—'):
            result = FormattingPreserver._ensure_dialogue_dash(
                result
            )

        if original.isupper():
            result = result.upper()
        elif original[0].isupper():
            result = result[0].upper() + result[1:]

        return result

    @staticmethod
    def _ensure_dialogue_dash(text: str) -> str:
        """Add dialogue dash if missing."""
        if not text.startswith('—'):
            return f'—{text.lstrip("-—")}'
        return text

    @staticmethod
    def preserve_whitespace(
        original: str,
        translated: str
    ) -> str:
        """Match leading/trailing whitespace."""
        leading = len(original) - len(original.lstrip())
        trailing = len(original) - len(original.rstrip())

        result = translated.strip()
        result = ' ' * leading + result + ' ' * trailing

        return result

    @staticmethod
    def preserve_line_breaks(
        original: str,
        translated: str
    ) -> str:
        """Preserve line breaks from original text."""
        orig_lines = original.split('\n')
        
        if len(orig_lines) == 1:
            return translated
        
        trans_clean = translated.replace('\n', ' ').strip()
        trans_words = trans_clean.split()
        
        if not trans_words:
            return translated
        
        orig_word_counts = [
            len(line.split()) for line in orig_lines
        ]
        total_orig_words = sum(orig_word_counts)
        
        if total_orig_words == 0:
            return translated
        
        result_lines = []
        word_idx = 0
        
        for orig_count in orig_word_counts:
            if orig_count == 0:
                result_lines.append('')
                continue
            
            ratio = orig_count / total_orig_words
            words_for_line = max(
                1,
                round(len(trans_words) * ratio)
            )
            
            end_idx = min(
                word_idx + words_for_line,
                len(trans_words)
            )
            
            line_words = trans_words[word_idx:end_idx]
            result_lines.append(' '.join(line_words))
            word_idx = end_idx
        
        if word_idx < len(trans_words):
            remaining = ' '.join(trans_words[word_idx:])
            if result_lines:
                result_lines[-1] += ' ' + remaining
            else:
                result_lines.append(remaining)
        
        return '\n'.join(result_lines)
