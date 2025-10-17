"""
Parse Command - Generate work manifest from book.
"""
import click
from pathlib import Path

from modules.tts.domain.manifest.manifest_parser import (
    ManifestParser
)


@click.command()
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
