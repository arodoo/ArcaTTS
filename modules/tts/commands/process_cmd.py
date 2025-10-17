"""
Process Work Command - Generate audio for single work.
"""
import click
from pathlib import Path
import json

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
    manifest = _load_manifest(manifest_file)
    work = _find_work(manifest, work_id)
    
    if not work:
        click.echo(f"Work #{work_id} not found")
        return
    
    click.echo(f"Processing: {work.title}")
    
    extractor = WorkExtractor(manifest.source_file)
    output_dir = Path(output)
    
    work_file = extractor.save_work(work, output_dir)
    click.echo(f"Extracted: {work_file}")
    
    _synthesize_work(work, extractor, output_dir, language)


def _load_manifest(path: str) -> Manifest:
    """Load manifest from JSON."""
    with open(path, 'r', encoding='utf-8') as f:
        return Manifest.from_dict(json.load(f))


def _find_work(manifest: Manifest, work_id: int):
    """Find work by ID."""
    return next((w for w in manifest.works if w.id == work_id), None)


def _synthesize_work(work, extractor, output_dir, language):
    """Generate and merge audio."""
    work_dir = output_dir / work.folder_name
    
    processor = EnhancedTextProcessor()
    text = extractor.extract(work)
    chunks = processor.prepare_work_text(text, add_title_pause=True)
    
    click.echo(f"Chunks: {len(chunks)}")
    
    _generate_chunks(chunks, work_dir, language)
    _merge_audio(work_dir)


def _generate_chunks(chunks, work_dir, language):
    """Generate TTS audio chunks with silence support."""
    engine = TTSEngine(language=language)
    silence_gen = SilenceGenerator()
    
    for i, chunk in enumerate(chunks):
        click.echo(f"[{i+1}/{len(chunks)}]")
        
        if chunk.startswith('<silence:'):
            duration = float(chunk.split(':')[1].rstrip('>'))
            silence_gen.generate_silence(
                duration,
                str(work_dir / f"chunk_{i:03d}.wav")
            )
        else:
            engine.synthesize(chunk, str(work_dir / f"chunk_{i:03d}.wav"))


def _merge_audio(work_dir):
    """Merge chunks and convert to MP3."""
    click.echo("Merging...")
    
    merger = WavMerger()
    chunks = sorted(work_dir.glob("chunk_*.wav"))
    wav_file = work_dir / "work.wav"
    
    merger.merge(
        input_files=[str(f) for f in chunks],
        output_file=str(wav_file)
    )
    
    click.echo("Converting to MP3...")
    converter = Mp3Converter(bitrate="128k")
    mp3_file = converter.convert(
        wav_path=str(wav_file),
        cleanup=True
    )
    
    if mp3_file:
        click.echo("Cleaning temp files...")
        converter.cleanup_chunks(work_dir)
        click.echo(f"Complete: {mp3_file}")
    else:
        click.echo(f"Warning: MP3 conversion failed. WAV: {wav_file}")



