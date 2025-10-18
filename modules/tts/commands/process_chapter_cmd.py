"""
Process Command - Full chapter processing.
"""
import click
from pathlib import Path

from modules.tts.domain.core.tts_engine import TTSEngine
from modules.tts.domain.core.text_processor import ChapterProcessor


@click.command()
@click.argument('input_file', type=click.Path(exists=True))
@click.option('--language', '-l', default='es')
@click.option('--output-dir', '-o', default='outputs')
def process(input_file: str, language: str, output_dir: str):
    """Generate audio from text file."""
    click.echo(f"Processing {input_file}...")
    
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    engine = TTSEngine(language=language)
    processor = ChapterProcessor()
    
    with open(input_file, 'r', encoding='utf-8') as f:
        text = f.read()
    
    chunks = processor.prepare_chapter(text)
    click.echo(f"Split into {len(chunks)} chunks")
    
    for i, chunk in enumerate(chunks):
        output_file = output_path / f"chunk_{i:03d}.wav"
        click.echo(f"Generating chunk {i+1}/{len(chunks)}...")
        
        engine.synthesize(
            text=chunk,
            output_path=str(output_file)
        )
    
    click.echo("Complete!")
