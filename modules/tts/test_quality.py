"""
Test comparativo de calidad de audio.
Compara técnicas antiguas vs nuevas mejoras.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from modules.tts.domain.tts_engine import TTSEngine


def test_quality_comparison():
    """Genera audios para comparar calidad."""
    
    test_texts = {
        "question": "¿Cómo estás hoy? ¿Qué tal tu día?",
        "exclamation": "¡Qué maravilla! ¡Es increíble!",
        "dialogue": "—No lo sé —dijo ella— quizás mañana.",
        "narrative": "Era una tarde tranquila de verano.",
        "ellipsis": "Y entonces... todo cambió."
    }
    
    engine = TTSEngine(enhance_quality=True)
    
    print("Generando audios de prueba...")
    print("=" * 60)
    
    for name, text in test_texts.items():
        output_path = f"outputs/test/quality_{name}.wav"
        
        print(f"\n{name.upper()}: {text}")
        success = engine.synthesize(text, output_path)
        
        if success:
            print(f"  ✓ Generado: {output_path}")
        else:
            print(f"  ✗ Error generando {name}")
    
    print("\n" + "=" * 60)
    print("PRUEBA COMPLETADA")
    print("\nEscucha los archivos en outputs/test/")
    print("Compara:")
    print("  - Entonación de preguntas")
    print("  - Expresividad de exclamaciones")
    print("  - Naturalidad de diálogos")
    print("  - Pausas en puntos suspensivos")


if __name__ == "__main__":
    test_quality_comparison()
