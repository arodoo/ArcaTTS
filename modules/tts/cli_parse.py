"""
Manifest Parser CLI
Extract work structure from large text files.

Usage:
  python -m modules.tts.cli parse <file>
"""
import click
from pathlib import Path
from modules.tts.domain.manifest_parser import ManifestParser


@click.group()
def parse_commands():
    """Manifest parsing commands."""
    pass


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
    help='Show detailed information'
)
def parse(input_file: str, output: str, verbose: bool):
    """Parse book file and generate manifest."""
    click.echo(f"📖 Parsing: {input_file}")
    click.echo("━" * 50)
    
    # Parse file
    parser = ManifestParser(input_file)
    manifest = parser.parse()
    
    # Display results
    click.echo(f"\n✓ Author: {manifest.author}")
    click.echo(f"✓ Total works detected: {manifest.total_works}")
    click.echo(f"✓ Source lines: {len(parser.lines):,}")
    
    if verbose:
        click.echo("\n📚 Works detected:")
        click.echo("━" * 70)
        for work in manifest.works:
            year_str = f"({work.year})" if work.year else ""
            lines = f"{work.estimated_lines:,} lines"
            click.echo(
                f"  {work.id:2d}. {work.title[:40]:40s} "
                f"{year_str:8s} {lines:>12s}"
            )
    
    # Save manifest
    output_dir = Path(output)
    filename = Path(input_file).stem
    manifest_path = output_dir / f"{filename}_manifest.json"
    
    manifest.save(manifest_path)
    
    click.echo(f"\n💾 Manifest saved: {manifest_path}")
    click.echo("━" * 50)
    click.echo("\n✅ Parsing complete!")
    click.echo("\nNext steps:")
    click.echo("  1. Review manifest.json")
    click.echo("  2. Test with one work:")
    click.echo(f"     python -m modules.tts.cli process-work "
               f"--manifest {manifest_path} --work-id 1")


if __name__ == '__main__':
    parse()
