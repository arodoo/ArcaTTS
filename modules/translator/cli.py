"""
CLI for translator module.
Direct translation interface.
"""
import click
from pathlib import Path

from .infrastructure.m2m100_adapter import M2M100Adapter
from .application.translation_service import (
    TranslationService
)
from .infrastructure.disk_cache import DiskCacheRepository


@click.group()
def cli():
    """Translation module CLI."""
    pass


@cli.command()
@click.argument('input_file', type=click.Path(exists=True))
@click.argument('output_file', type=click.Path())
@click.option(
    '--source',
    '-s',
    help='Source language (auto-detect if omitted)'
)
@click.option('--target', '-t', required=True)
@click.option('--use-gpu/--no-gpu', default=True)
def translate(
    input_file,
    output_file,
    source,
    target,
    use_gpu
):
    """Translate text file."""
    click.echo(f"\nLoading text from {input_file}...")

    with open(input_file, 'r', encoding='utf-8') as f:
        text = f.read()

    words = len(text.split())
    click.echo(f"Text loaded: {words:,} words")

    device = "GPU" if use_gpu else "CPU"
    click.echo(f"Using device: {device}")

    translator = M2M100Adapter(
        use_gpu=use_gpu,
        model_size="418M"
    )
    service = TranslationService(translator)
    cache = DiskCacheRepository()

    translation = service.translate_text(
        text,
        target_language=target,
        source_language=source
    )

    cache.save(translation)
    click.echo(f"\nCached: {translation.translation_id}")
    click.echo(f"Glossary terms: {len(translation.glossary)}")

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(translation.final_translation)

    click.echo(f"Saved to {output_file}\n")


if __name__ == '__main__':
    cli()
