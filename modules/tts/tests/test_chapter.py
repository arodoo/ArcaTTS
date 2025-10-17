"""
ÚNICO TEST DEL SISTEMA
Genera el Capítulo I de "DESCRIPCIÓN DE UNA LUCHA"
para validar todo el pipeline.
"""
from pathlib import Path
from modules.tts.domain.core.enhanced_text_processor import (
    EnhancedTextProcessor
)
from modules.tts.domain.core.tts_engine import TTSEngine
from modules.tts.domain.audio.silence_generator import (
    SilenceGenerator
)
from modules.tts.domain.audio.wav_merger import WavMerger
from modules.tts.domain.audio.mp3_converter import Mp3Converter


def main():
    """Generate Chapter I audio."""
    
    # Read Chapter I from book
    book_path = Path("boocks/franz-kafka.txt")
    with open(book_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Chapter I: lines 76-200 (approx)
    chapter_text = ''.join(lines[75:200])
    
    # Setup
    output_dir = Path("outputs/test_chapter")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print("=" * 70)
    print("GENERATING CHAPTER I - DESCRIPCIÓN DE UNA LUCHA")
    print("=" * 70)
    
    # Process text
    processor = EnhancedTextProcessor(chunk_size=500)
    chunks = processor.prepare_work_text(
        chapter_text,
        add_title_pause=True
    )
    
    print(f"\nText processed into {len(chunks)} chunks")
    
    # Generate audio
    engine = TTSEngine(language="es_mx")
    silence_gen = SilenceGenerator()
    
    print("\nGenerating audio chunks...")
    for i, chunk in enumerate(chunks, 1):
        print(f"  [{i}/{len(chunks)}]", end=" ")
        
        chunk_path = output_dir / f"chunk_{i:03d}.wav"
        
        if chunk.startswith('<silence:'):
            duration = float(chunk.split(':')[1].rstrip('>'))
            print(f"Silence {duration}s")
            silence_gen.generate_silence(
                duration,
                str(chunk_path)
            )
        else:
            print(f"{len(chunk)} chars")
            engine.synthesize(chunk, str(chunk_path))
    
    # Merge
    print("\nMerging chunks...")
    merger = WavMerger()
    chunk_files = sorted(output_dir.glob("chunk_*.wav"))
    wav_file = output_dir / "chapter_I.wav"
    
    merger.merge(
        input_files=[str(f) for f in chunk_files],
        output_file=str(wav_file)
    )
    
    # Convert to MP3
    print("Converting to MP3...")
    converter = Mp3Converter(bitrate="128k")
    mp3_file = converter.convert(
        wav_path=str(wav_file),
        cleanup=True
    )
    
    # Cleanup chunks
    converter.cleanup_chunks(output_dir)
    
    print("\n" + "=" * 70)
    print("CHAPTER I COMPLETE!")
    print("=" * 70)
    print(f"\nAudio: {mp3_file}")
    print(f"Size: {Path(mp3_file).stat().st_size / (1024*1024):.1f} MB")
    print("\nListen and verify:")
    print("  ✓ Speed is comfortable (not too fast)")
    print("  ✓ Pauses sound natural (RAE-compliant)")
    print("  ✓ No content jumps or missing text")
    print("  ✓ No distortion on '...' or ';'")


if __name__ == "__main__":
    main()
