"""Test expressiveness improvements."""
from pathlib import Path
from modules.tts.domain.tts_engine import TTSEngine
from modules.tts.domain.enhanced_text_processor import (
    EnhancedTextProcessor
)
from modules.tts.domain.silence_generator import (
    SilenceGenerator
)
from modules.tts.domain.wav_merger import WavMerger
from modules.tts.domain.mp3_converter import Mp3Converter


def generate_test(text: str, name: str):
    """Generate audio with current settings."""
    output_dir = Path(f"outputs/test/expressiveness_{name}")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    processor = EnhancedTextProcessor()
    chunks = processor.prepare_work_text(text, add_title_pause=False)
    
    print(f"\n{name.upper()}:")
    print(f"Chunks: {len(chunks)}")
    for i, c in enumerate(chunks):
        print(f"  {i}: {repr(c)[:60]}")
    
    engine = TTSEngine(language="es_mx")
    silence_gen = SilenceGenerator()
    
    for i, chunk in enumerate(chunks):
        chunk_path = output_dir / f"chunk_{i:03d}.wav"
        
        if chunk.startswith('<silence:'):
            duration = float(chunk.split(':')[1].rstrip('>'))
            silence_gen.generate_silence(duration, str(chunk_path))
        else:
            engine.synthesize(chunk, str(chunk_path))
    
    merger = WavMerger()
    chunks_files = sorted(output_dir.glob("chunk_*.wav"))
    wav_file = output_dir / f"{name}.wav"
    
    merger.merge(
        input_files=[str(f) for f in chunks_files],
        output_file=str(wav_file)
    )
    
    converter = Mp3Converter(bitrate="128k")
    mp3_file = converter.convert(
        wav_path=str(wav_file),
        cleanup=False
    )
    
    print(f"✓ Generated: {mp3_file}")


def main():
    """Test all improvements."""
    tests = {
        "questions": """
¿QUÉ estás haciendo?
¿CÓMO puedo ayudarte?
¿DÓNDE está mi libro?
¿POR QUÉ no me escuchas?
        """.strip(),
        
        "exclamations": """
¡¡QUÉ hermoso día!!
¡¡NO puedo creerlo!!
¡¡AY, QUÉ dolor!!
¡¡DIOS mío, es increíble!!
        """.strip(),
        
        "ellipsis": """
No sé qué decir... quizás mañana...
Me pregunto si... tal vez no debería...
Es posible que... aunque no estoy seguro...
        """.strip(),
        
        "mixed": """
¡¡Escucha!! ¿DÓNDE estabas?
No lo sé... ¿tal vez en casa?
¡¡NO me digas ESO!!
        """.strip()
    }
    
    for name, text in tests.items():
        generate_test(text, name)
    
    print("\n" + "=" * 60)
    print("ALL TESTS COMPLETE!")
    print("=" * 60)
    print("\nCheck outputs/test/expressiveness_* for results")


if __name__ == "__main__":
    main()
