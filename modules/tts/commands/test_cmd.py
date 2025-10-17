"""
Test Command - Quick TTS test.
"""
import click
from pathlib import Path

from modules.tts.domain.tts_engine import TTSEngine
from modules.tts.domain.enhanced_text_processor import (
    EnhancedTextProcessor
)
from modules.tts.domain.silence_generator import (
    SilenceGenerator
)
from modules.tts.domain.wav_merger import WavMerger


@click.command()
@click.option('--text', required=True, help='Test text')
@click.option('--language', '-l', default='es')
def test(text: str, language: str):
    """Quick TTS test with full processing."""
    click.echo("Testing TTS with enhancements...")
    
    output_dir = Path("outputs/test")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Process text with enhancements
    processor = EnhancedTextProcessor()
    chunks = processor.prepare_work_text(
        text, 
        add_title_pause=False
    )
    
    # Generate chunks
    engine = TTSEngine(language=language)
    silence_gen = SilenceGenerator()
    
    chunk_files = []
    for i, chunk in enumerate(chunks):
        chunk_path = output_dir / f"test_chunk_{i:03d}.wav"
        
        if chunk.startswith('<silence:'):
            duration = float(chunk.split(':')[1].rstrip('>'))
            silence_gen.generate_silence(duration, str(chunk_path))
        else:
            engine.synthesize(chunk, str(chunk_path))
        
        chunk_files.append(str(chunk_path))
    
    # Merge all chunks
    merger = WavMerger()
    output_path = output_dir / "quick_test.wav"
    merger.merge(chunk_files, str(output_path))
    
    # Cleanup chunks
    for chunk_file in chunk_files:
        Path(chunk_file).unlink()
    
    click.echo(f"Audio: {output_path}")
