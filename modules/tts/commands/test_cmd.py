"""
Test Command - Quick TTS test.
"""
import click
from pathlib import Path

from modules.tts.domain.tts_engine import TTSEngine


@click.command()
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
        click.echo(f"Audio: {output_path}")
    else:
        click.echo("Failed")
