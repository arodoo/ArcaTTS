"""
Grammar Module CLI
Detects and corrects grammar errors in text files.

Usage:
  python -m modules.grammar.cli check <file> [--language es]
  python -m modules.grammar.cli correct <file> [--output path]
"""
import click
from pathlib import Path
from modules.grammar.domain.corrector import TextCorrector


# Global corrector singleton per language
_CORRECTORS = {}


def get_corrector(language: str) -> TextCorrector:
    """Get or create corrector for language."""
    if language not in _CORRECTORS:
        _CORRECTORS[language] = TextCorrector(language)
    return _CORRECTORS[language]


@click.group()
def cli():
    """Grammar correction tool."""
    pass


@cli.command()
@click.argument('input_file', type=click.Path(exists=True))
@click.option(
    '--language', '-l',
    default='es',
    help='Language code (es, en, pt)'
)
@click.option(
    '--verbose', '-v',
    is_flag=True,
    help='Show detailed error information'
)
def check(input_file: str, language: str, verbose: bool):
    """Check file for grammar errors without fixing."""
    click.echo(f"Checking {input_file}...")
    
    corrector = get_corrector(language)
    
    try:
        # Read file
        with open(input_file, 'r', encoding='utf-8') as f:
            text = f.read()
        
        # Check errors
        errors = corrector.checker.check_text(text)
        
        # Display results
        click.echo(f"\n✓ Found {len(errors)} issues\n")
        
        if verbose and errors:
            for i, error in enumerate(errors[:20], 1):
                click.echo(f"{i}. {error.error_type.value}")
                click.echo(f"   {error.message}")
                click.echo(f"   Original: {error.original_text}")
                if error.suggested_replacement:
                    click.echo(
                        f"   Suggested: "
                        f"{error.suggested_replacement}"
                    )
                click.echo()
            
            if len(errors) > 20:
                click.echo(
                    f"... and {len(errors) - 20} more"
                )
        
        click.echo(
            f"Run 'correct' command to fix errors."
        )
    
    except Exception as e:
        click.echo(f"\n✗ Error: {e}", err=True)


@cli.command()
@click.argument('input_file', type=click.Path(exists=True))
@click.option(
    '--output-dir', '-o',
    default='boocks_corrected',
    help='Output directory (default: boocks_corrected/)'
)
@click.option(
    '--language', '-l',
    default='es',
    help='Language code (es, en, pt)'
)
@click.option(
    '--no-fix',
    is_flag=True,
    help='Only detect, do not apply corrections'
)
@click.option(
    '--version', '-v',
    help='Custom version name (default: timestamp)'
)
def correct(
    input_file: str,
    output_dir: str,
    language: str,
    no_fix: bool,
    version: str
):
    """Correct grammar errors and save versioned file."""
    input_path = Path(input_file)
    
    click.echo(f"Processing {input_file}...")
    click.echo(f"Output directory: {output_dir}")
    
    corrector = get_corrector(language)
    
    try:
        result = corrector.correct_file(
            str(input_path),
            output_dir,
            auto_fix=not no_fix,
            version=version
        )
        
        if result.success:
            click.echo("\n✓ Correction complete!\n")
            click.echo(f"Total errors: {result.total_errors}")
            click.echo(f"Fixed: {result.fixed_errors}")
            click.echo(
                f"Fix rate: "
                f"{(result.fixed_errors/result.total_errors*100):.1f}%"
                if result.total_errors > 0 else "N/A"
            )
            click.echo(f"\nOutput file: {result.corrected_file}")
            
            # Find summary file
            corrected_path = Path(result.corrected_file)
            summary_file = corrected_path.parent / (
                corrected_path.stem.replace(
                    input_path.stem,
                    f"{input_path.stem}_fixes"
                ) + ".json"
            )
            
            if summary_file.exists():
                click.echo(f"Summary: {summary_file}")
        else:
            click.echo(
                f"\n✗ Error: {result.error_message}",
                err=True
            )
    
    except Exception as e:
        click.echo(f"\n✗ Error: {e}", err=True)


if __name__ == '__main__':
    cli()
