"""Test with REAL book text to debug content loss."""
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


def test_real_book_text():
    """Test with actual text from DESCRIPCIÓN DE UNA LUCHA."""
    
    # Real text from lines 97-107 of franz-kafka.txt
    text = """
-disculpe que me dirija a usted, pero he estado hasta ahora sentado 
con mi novia en la habitación contigua desde las diez y media. ¡Esta sí 
que ha sido una noche, compañero! Comprendo: no está bien que se lo 
cuente; apenas nos conocemos. ¿No es así? Apenas si al llegar hemos 
cambiado unas palabras en la escalera. Con codo, le ruego que me 
disculpe, pero no soportaba ya la felicidad, era más fuerte que yo. Y 
como aquí no tengo aconocidos en quienes confiar...

Miré con tristeza su bello rostro arrebolado -el pastelillo de fruta que 
me había llevado a la boca no era gran cosa y le dije:
    """.strip()
    
    output_dir = Path("outputs/test/real_book")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    processor = EnhancedTextProcessor()
    chunks = processor.prepare_work_text(text, add_title_pause=False)
    
    print(f"\nGenerated {len(chunks)} chunks from real book text:")
    print("=" * 70)
    for i, chunk in enumerate(chunks):
        print(f"\nChunk {i}:")
        print(f"  Type: {'SILENCE' if chunk.startswith('<silence:') else 'TEXT'}")
        if chunk.startswith('<silence:'):
            duration = chunk.split(':')[1].rstrip('>')
            print(f"  Duration: {duration}s")
        else:
            print(f"  Content: {chunk[:100]}...")
            print(f"  Length: {len(chunk)} chars")
    
    engine = TTSEngine(language="es_mx")
    silence_gen = SilenceGenerator()
    
    print("\n" + "=" * 70)
    print("Generating audio chunks...")
    print("=" * 70)
    
    for i, chunk in enumerate(chunks):
        chunk_path = output_dir / f"chunk_{i:03d}.wav"
        
        if chunk.startswith('<silence:'):
            duration = float(chunk.split(':')[1].rstrip('>'))
            print(f"Chunk {i}: Silence {duration}s")
            silence_gen.generate_silence(duration, str(chunk_path))
        else:
            print(f"Chunk {i}: Synthesizing {len(chunk)} chars...")
            engine.synthesize(chunk, str(chunk_path))
    
    print("\n" + "=" * 70)
    print("Merging chunks...")
    print("=" * 70)
    
    merger = WavMerger()
    chunk_files = sorted(output_dir.glob("chunk_*.wav"))
    wav_file = output_dir / "real_book_test.wav"
    
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
    print(f"\nWAV: {wav_file}")
    print(f"MP3: {mp3_file}")
    print("\nListen carefully and compare to original text above.")
    print("Check if ANY content is missing or skipped.")


if __name__ == "__main__":
    test_real_book_text()
