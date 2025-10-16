"""
TTS Module CLI
Generate audio from text files using XTTS-v2.

Usage:
  python -m modules.tts.cli process <file> [--language es]
  python -m modules.tts.cli test --text "Sample text"
"""
import click
from pathlib import Path
from modules.tts.domain.tts_engine import TTSEngine
from modules.tts.domain.text_processor import ChapterProcessor
from modules.tts.domain.parser import BookStructureParser


@click.group()
def cli():
    """TTS audio generation tool."""
    pass


@cli.command()
@click.argument('input_file', type=click.Path(exists=True))
@click.option(
    '--language', '-l',
    default='es',
    help='Language code (es, en, pt)'
)
@click.option(
    '--output-dir', '-o',
    default='outputs',
    help='Output directory for audio files'
)
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
    
    click.echo("✓ Complete!")


@cli.command()
@click.option('--text', required=True, help='Test text')
@click.option('--language', '-l', default='es')
def test(text: str, language: str):
    """Quick TTS test."""
    click.echo("Testing TTS engine...")
    
    engine = TTSEngine(language=language)
    output_path = Path("outputs/test/quick_test.wav")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    success = engine.synthesize(text, str(output_path))
    
    if success:
        click.echo(f"✓ Audio: {output_path}")
    else:
        click.echo("✗ Failed")


if __name__ == '__main__':
    cli()
