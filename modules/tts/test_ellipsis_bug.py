"""Test ellipsis bug with exact production text."""
from pathlib import Path
from modules.tts.domain.enhanced_text_processor import (
    EnhancedTextProcessor
)
from modules.tts.domain.tts_engine import TTSEngine
from modules.tts.domain.silence_generator import (
    SilenceGenerator
)
from modules.tts.domain.wav_merger import WavMerger
from modules.tts.domain.mp3_converter import Mp3Converter


def test_ellipsis_production():
    """Test exact text that causes noise."""
    text = """como aquí no tengo aconocidos en 
quienes confiar... y también porque 
me gustaría hacer una pregunta: 
¿puede usted ayudarme? ¡Necesito ayuda!"""
    
    output_dir = Path("outputs/test/ellipsis_bug")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    processor = EnhancedTextProcessor()
    chunks = processor.prepare_work_text(
        text,
        add_title_pause=False
    )
    
    print(f"\nGenerated {len(chunks)} chunks:")
    for i, chunk in enumerate(chunks):
        print(f"{i}: {repr(chunk)[:80]}")
    
    engine = TTSEngine(language="es_mx")
    silence_gen = SilenceGenerator()
    
    print("\nGenerating audio...")
    for i, chunk in enumerate(chunks):
        chunk_path = output_dir / f"chunk_{i:03d}.wav"
        
        if chunk.startswith('<silence:'):
            duration = float(chunk.split(':')[1].rstrip('>'))
            print(f"  Silence {i}: {duration}s")
            silence_gen.generate_silence(duration, str(chunk_path))
        else:
            print(f"  Synth {i}: {chunk[:50]}...")
            engine.synthesize(chunk, str(chunk_path))
    
    print("\nMerging chunks...")
    merger = WavMerger()
    chunks_files = sorted(output_dir.glob("chunk_*.wav"))
    wav_file = output_dir / "ellipsis_test.wav"
    
    merger.merge(
        input_files=[str(f) for f in chunks_files],
        output_file=str(wav_file)
    )
    
    print("\nConverting to MP3...")
    converter = Mp3Converter(bitrate="128k")
    mp3_file = converter.convert(
        wav_path=str(wav_file),
        cleanup=False
    )
    
    print(f"\nTest complete!")
    print(f"WAV: {wav_file}")
    print(f"MP3: {mp3_file}")


if __name__ == "__main__":
    test_ellipsis_production()
