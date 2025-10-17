"""
Process All Command - Batch process entire collection.
"""
import click
from pathlib import Path
import json
from concurrent.futures import (
    ProcessPoolExecutor, as_completed
)

from modules.tts.domain.core.tts_engine import TTSEngine
from modules.tts.domain.core.enhanced_text_processor import (
    EnhancedTextProcessor
)
from modules.tts.domain.work.work_processor import WorkExtractor
from modules.tts.domain.manifest.manifest import Manifest
from modules.tts.domain.audio.wav_merger import WavMerger
from modules.tts.domain.audio.mp3_converter import Mp3Converter
from modules.tts.domain.audio.silence_generator import (
    SilenceGenerator
)


@click.command()
@click.argument('manifest_file', type=click.Path(exists=True))
@click.option('--output', '-o', default='outputs/works')
@click.option('--language', '-l', default='es_MX')
@click.option('--workers', '-w', default=1, type=int)
@click.option('--start-from', default=1, type=int)
def process_all(
    manifest_file: str,
    output: str,
    language: str,
    workers: int,
    start_from: int
):
    """Process all works in manifest."""
    with open(manifest_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    manifest = Manifest.from_dict(data)
    works_to_process = [w for w in manifest.works if w.id >= start_from]
    
    click.echo(f"Collection: {manifest.author}")
    click.echo(f"Works to process: {len(works_to_process)}")
    click.echo(f"Workers: {workers}")
    click.echo("=" * 60)
    
    if workers == 1:
        _process_sequential(works_to_process, manifest, output, language)
    else:
        _process_parallel(works_to_process, manifest, output, language, workers)


def _process_sequential(works, manifest, output, language):
    """Process works one by one."""
    for i, work in enumerate(works, 1):
        click.echo(f"\n[{i}/{len(works)}] {work.title}")
        _process_single_work(work, manifest.source_file, output, language)


def _process_parallel(works, manifest, output, language, workers):
    """Process works in parallel."""
    click.echo("Parallel processing not yet implemented.")
    click.echo("Using sequential mode...")
    _process_sequential(works, manifest, output, language)


def _process_single_work(work, source_file, output, language):
    """Process one work (for parallel execution)."""
    try:
        output_dir = Path(output)
        work_dir = output_dir / work.folder_name
        
        extractor = WorkExtractor(source_file)
        extractor.save_work(work, output_dir)
        
        processor = EnhancedTextProcessor()
        text = extractor.extract(work)
        chunks = processor.prepare_work_text(text, add_title_pause=True)
        
        _generate_audio_chunks(chunks, work_dir, language)
        _merge_and_convert(work_dir)
        
        click.echo(f"  ✓ Complete: {work.folder_name}")
        return True
        
    except Exception as e:
        click.echo(f"  ✗ Error: {work.title} - {e}")
        return False


def _generate_audio_chunks(chunks, work_dir, language):
    """Generate all audio chunks."""
    engine = TTSEngine(language=language)
    silence_gen = SilenceGenerator()
    
    for i, chunk in enumerate(chunks):
        if chunk.startswith('<silence:'):
            duration = float(chunk.split(':')[1].rstrip('>'))
            silence_gen.generate_silence(
                duration,
                str(work_dir / f"chunk_{i:03d}.wav")
            )
        else:
            engine.synthesize(chunk, str(work_dir / f"chunk_{i:03d}.wav"))


def _merge_and_convert(work_dir):
    """Merge chunks and convert to MP3."""
    merger = WavMerger()
    chunks = sorted(work_dir.glob("chunk_*.wav"))
    wav_file = work_dir / "work.wav"
    
    merger.merge(
        input_files=[str(f) for f in chunks],
        output_file=str(wav_file)
    )
    
    converter = Mp3Converter(bitrate="128k")
    converter.convert(wav_path=str(wav_file), cleanup=True)
    converter.cleanup_chunks(work_dir)

