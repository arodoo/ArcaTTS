"""
TTS Module CLI
Generate audio from text files using XTTS-v2.

Usage:
  python -m modules.tts.cli parse <file>
  python -m modules.tts.cli process <file>
  python -m modules.tts.cli test --text "Sample text"
"""
import click
from pathlib import Path
import json
from modules.tts.domain.tts_engine import TTSEngine
from modules.tts.domain.text_processor import ChapterProcessor
from modules.tts.domain.manifest_parser import ManifestParser
from modules.tts.domain.work_processor import WorkExtractor
from modules.tts.domain.manifest import Manifest
from modules.tts.domain.wav_merger import WavMerger


@click.group()
def cli():
    """TTS audio generation tool."""
    pass


@cli.command()
@click.argument('input_file', type=click.Path(exists=True))
@click.option(
    '--output', '-o',
    default='outputs/manifests',
    help='Output directory for manifest'
)
@click.option(
    '--verbose', '-v',
    is_flag=True,
    help='Show detailed work information'
)
def parse(input_file: str, output: str, verbose: bool):
    """Parse book and generate work manifest."""
    click.echo(f"Parsing: {input_file}")
    click.echo("=" * 50)
    
    parser = ManifestParser(input_file)
    manifest = parser.parse()
    
    click.echo(f"\nAuthor: {manifest.author}")
    click.echo(f"Works detected: {manifest.total_works}")
    click.echo(f"Total lines: {len(parser.lines):,}")
    
    if verbose:
        click.echo("\nDetected works:")
        click.echo("=" * 70)
        for work in manifest.works:
            year = f"({work.year})" if work.year else ""
            lines = f"{work.estimated_lines:,} lines"
            click.echo(
                f"  {work.id:2d}. {work.title[:40]:40s} "
                f"{year:8s} {lines:>12s}"
            )
    
    output_dir = Path(output)
    filename = Path(input_file).stem
    manifest_path = output_dir / f"{filename}_manifest.json"
    
    manifest.save(manifest_path)
    
    click.echo(f"\nSaved: {manifest_path}")
    click.echo("\nParsing complete!")


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
@click.argument('manifest_file', type=click.Path(exists=True))
@click.argument('work_id', type=int)
@click.option('--output', '-o', default='outputs/works')
@click.option('--language', '-l', default='es_MX')
def process_work(
    manifest_file: str, 
    work_id: int, 
    output: str,
    language: str
):
    """Process single work to audio."""
    with open(manifest_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    manifest = Manifest.from_dict(data)
    work = next((w for w in manifest.works if w.id == work_id), None)
    
    if not work:
        click.echo(f"Work #{work_id} not found")
        return
    
    click.echo(f"Processing: {work.title}")
    click.echo(f"Lines: {work.estimated_lines:,}")
    
    extractor = WorkExtractor(manifest.source_file)
    output_dir = Path(output)
    
    work_file = extractor.save_work(work, output_dir)
    click.echo(f"Extracted: {work_file}")
    
    work_dir = output_dir / work.folder_name
    audio_file = work_dir / "work.wav"
    
    engine = TTSEngine(language=language)
    processor = ChapterProcessor()
    
    text = extractor.extract(work)
    chunks = processor.prepare_chapter(text)
    
    click.echo(f"Chunks: {len(chunks)}")
    
    for i, chunk in enumerate(chunks):
        chunk_file = work_dir / f"chunk_{i:03d}.wav"
        click.echo(f"[{i+1}/{len(chunks)}] Generating...")
        engine.synthesize(chunk, str(chunk_file))
    
    click.echo("Merging audio...")
    merger = WavMerger()
    chunk_files = sorted(work_dir.glob("chunk_*.wav"))
    merger.merge(
        input_files=[str(f) for f in chunk_files],
        output_file=str(audio_file)
    )
    
    click.echo(f"Complete: {audio_file}")


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
