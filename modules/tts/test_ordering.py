"""Test to detect order issues in audio generation."""
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


def test_ordering():
    """Test with numbered sentences to detect jumps."""
    
    # Numbered sentences to track order
    text = """
Oración uno. Esta es la primera oración.
Oración dos. Esta es la segunda oración.
Oración tres. Esta es la tercera oración.
Oración cuatro. Esta es la cuarta oración.
Oración cinco. Esta es la quinta oración.
Oración seis. Esta es la sexta oración.
Oración siete. Esta es la séptima oración.
Oración ocho. Esta es la octava oración.
Oración nueve. Esta es la novena oración.
Oración diez. Esta es la décima oración.
    """.strip()
    
    output_dir = Path("outputs/test/ordering")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    processor = EnhancedTextProcessor()
    chunks = processor.prepare_work_text(text, add_title_pause=False)
    
    print(f"\nGenerated {len(chunks)} chunks:")
    print("=" * 70)
    for i, chunk in enumerate(chunks):
        if chunk.startswith('<silence:'):
            duration = chunk.split(':')[1].rstrip('>')
            print(f"Chunk {i}: SILENCE {duration}s")
        else:
            # Show first 100 chars
            preview = chunk.replace('\n', ' ')[:100]
            print(f"Chunk {i}: {preview}...")
    
    print("\n" + "=" * 70)
    print("Generating audio...")
    print("=" * 70)
    
    engine = TTSEngine(language="es_mx")
    silence_gen = SilenceGenerator()
    
    for i, chunk in enumerate(chunks):
        chunk_path = output_dir / f"chunk_{i:03d}.wav"
        
        if chunk.startswith('<silence:'):
            duration = float(chunk.split(':')[1].rstrip('>'))
            silence_gen.generate_silence(duration, str(chunk_path))
        else:
            engine.synthesize(chunk, str(chunk_path))
    
    print("\nMerging chunks...")
    merger = WavMerger()
    chunk_files = sorted(output_dir.glob("chunk_*.wav"))
    
    print(f"Merging {len(chunk_files)} files in order:")
    for f in chunk_files:
        print(f"  {f.name}")
    
    wav_file = output_dir / "ordering_test.wav"
    merger.merge(
        input_files=[str(f) for f in chunk_files],
        output_file=str(wav_file)
    )
    
    print("\nConverting to MP3...")
    converter = Mp3Converter(bitrate="128k")
    mp3_file = converter.convert(
        wav_path=str(wav_file),
        cleanup=False
    )
    
    print("\n" + "=" * 70)
    print("TEST COMPLETE!")
    print("=" * 70)
    print(f"\nMP3: {mp3_file}")
    print("\nListen and verify order:")
    print("Should hear: uno, dos, tres, cuatro, cinco, seis, siete, ocho, nueve, diez")
    print("If order is wrong, we have a chunking/merging bug")


if __name__ == "__main__":
    test_ordering()
