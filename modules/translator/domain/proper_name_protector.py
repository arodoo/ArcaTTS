"""
Protect proper names during translation.
Post-processes to restore original names.
"""
import re
from typing import Dict, List, Tuple


class ProperNameProtector:
    """Preserve proper names in translation."""
    
    NAME_PATTERNS = [
        re.compile(r'\b([A-ZÁÉÍÓÚÑ][A-ZÁÉÍÓÚÑ]+(?:\s+[A-ZÁÉÍÓÚÑ][A-ZÁÉÍÓÚÑ]+)+)\b'),
        re.compile(r'\b([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)+)\b'),
    ]
    
    KNOWN_NAMES = [
        "FRANZ KAFKA",
        "Franz Kafka",
        "Karl Rossmann",
        "Nueva York",
        "América",
    ]

    def extract_names(self, text: str) -> List[str]:
        """Find all proper names in text."""
        names = []
        
        for known_name in self.KNOWN_NAMES:
            if known_name in text:
                names.append(known_name)
        
        for pattern in self.NAME_PATTERNS:
            for match in pattern.finditer(text):
                name = match.group(1)
                if (name not in names and 
                    self._is_likely_proper_name(name, text)):
                    names.append(name)
        
        return names

    def restore_names(
        self,
        original: str,
        translated: str
    ) -> str:
        """Restore proper names from original."""
        names = self.extract_names(original)
        result = translated
        
        corruption_map = {
            "FRANZ KAFKA": ["FRANÇA KAFKA", "Françesco Kaffka", "Francesco Kaffka"],
            "Karl Rossmann": ["Karl Rossmann", "Carlos Rossmann"],
            "Nueva York": ["Nueva York", "Nova York"],
        }
        
        for name in names:
            if name in corruption_map:
                for corrupted in corruption_map[name]:
                    if corrupted in result or corrupted.rstrip('.') in result:
                        clean_corrupt = corrupted.rstrip('.')
                        result = result.replace(clean_corrupt, name)
                        result = result.replace(corrupted, name)
            
            words = name.split()
            
            if len(words) >= 2:
                last_word = words[-1]
                
                pattern = re.compile(
                    rf'\b\w+(?:\s+\w+)*\s+{re.escape(last_word)}\b\.?',
                    re.IGNORECASE
                )
                
                match = pattern.search(result)
                if match and self._is_likely_match(name, match.group()):
                    result = result.replace(
                        match.group().rstrip('.'),
                        name,
                        1
                    )
            else:
                pattern = re.compile(
                    rf'\b\w{{2,{len(name)+10}}}\b',
                    re.IGNORECASE
                )
                
                potential_match = pattern.search(result)
                if (potential_match and 
                    self._is_similar(name, potential_match.group())):
                    result = result.replace(
                        potential_match.group(),
                        name,
                        1
                    )
        
        return result

    def _is_likely_match(self, original: str, candidate: str) -> bool:
        """Check if candidate is likely the same name."""
        orig_words = original.split()
        cand_words = candidate.rstrip('.').split()
        
        if len(orig_words) != len(cand_words):
            return False
        
        for orig_word, cand_word in zip(orig_words, cand_words):
            if not self._is_similar(orig_word, cand_word):
                return False
        
        return True

    def _is_similar(self, str1: str, str2: str) -> bool:
        """Check if strings are similar (fuzzy match)."""
        if str1.lower() == str2.lower():
            return True
        
        if len(str1) == 0 or len(str2) == 0:
            return False
        
        common = sum(
            c1.lower() == c2.lower()
            for c1, c2 in zip(str1, str2)
        )
        similarity = common / max(len(str1), len(str2))
        
        return similarity > 0.6

    def _is_likely_proper_name(
        self,
        candidate: str,
        context: str
    ) -> bool:
        """Check if candidate is a proper name."""
        if len(candidate) < 3:
            return False
        
        words = candidate.split()
        if len(words) > 1:
            return True
        
        if self._is_sentence_start(candidate, context):
            return False
        
        return True

    def _is_sentence_start(
        self,
        word: str,
        text: str
    ) -> bool:
        """Check if word starts a sentence."""
        pattern = re.compile(
            rf'(?:^|[.!?]\s+)({re.escape(word)})\b'
        )
        return bool(pattern.search(text))
