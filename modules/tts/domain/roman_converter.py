"""
Roman Numeral Converter - To Spanish ordinals.
"""
import re


class RomanConverter:
    """Convert Roman numerals to Spanish words."""
    
    ROMAN_TO_NUM = {
        'I': 1, 'II': 2, 'III': 3, 'IV': 4, 'V': 5,
        'VI': 6, 'VII': 7, 'VIII': 8, 'IX': 9, 'X': 10,
        'XI': 11, 'XII': 12, 'XIII': 13, 'XIV': 14, 'XV': 15,
        'XVI': 16, 'XVII': 17, 'XVIII': 18, 'XIX': 19, 'XX': 20
    }
    
    NUM_TO_SPANISH = {
        1: 'Primero', 2: 'Segundo', 3: 'Tercero',
        4: 'Cuarto', 5: 'Quinto', 6: 'Sexto',
        7: 'Séptimo', 8: 'Octavo', 9: 'Noveno',
        10: 'Décimo', 11: 'Undécimo', 12: 'Duodécimo',
        13: 'Decimotercero', 14: 'Decimocuarto',
        15: 'Decimoquinto', 16: 'Decimosexto',
        17: 'Decimoséptimo', 18: 'Decimoctavo',
        19: 'Decimonoveno', 20: 'Vigésimo'
    }
    
    def convert_line(self, text: str) -> str:
        """Convert Roman numerals in text."""
        pattern = r'^([IVX]+)\s*$'
        
        lines = text.split('\n')
        converted = []
        
        for line in lines:
            match = re.match(pattern, line.strip())
            
            if match:
                roman = match.group(1)
                num = self.ROMAN_TO_NUM.get(roman)
                
                if num:
                    spanish = self.NUM_TO_SPANISH.get(num, roman)
                    converted.append(
                        f"{spanish}\n<silence:2.0>"
                    )
                else:
                    converted.append(line)
            else:
                converted.append(line)
        
        return '\n'.join(converted)
