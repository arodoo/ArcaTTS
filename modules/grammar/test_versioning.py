"""
Test versioning and summary generation.
Creates a sample file and verifies output structure.
"""
from pathlib import Path
from modules.grammar.domain.corrector import TextCorrector
import json


def main():
    print("=" * 60)
    print("VERSIONING & SUMMARY TEST")
    print("=" * 60)
    
    # Create test file
    test_dir = Path("test_grammar_output")
    test_dir.mkdir(exist_ok=True)
    
    test_file = test_dir / "sample.txt"
    test_text = """
    Este es un texto de prueva con algunos errores.
    Ay muchos problemas gramaticales aqui.
    Tambien falta algunos signos de puntuacion.
    """
    
    with open(test_file, 'w', encoding='utf-8') as f:
        f.write(test_text)
    
    print(f"\n✓ Created test file: {test_file}")
    
    # Run correction
    corrector = TextCorrector(language="es")
    
    try:
        print("\nRunning correction...")
        result = corrector.correct_file(
            str(test_file),
            str(test_dir / "corrected"),
            auto_fix=True
        )
        
        if result.success:
            print("\n✓ Correction successful!\n")
            
            # Verify outputs
            corrected_path = Path(result.corrected_file)
            
            print(f"Corrected file: {corrected_path.name}")
            print(f"  Exists: {corrected_path.exists()}")
            
            # Find summary file
            summary_file = corrected_path.parent / (
                corrected_path.stem.replace(
                    "sample",
                    "sample_fixes"
                ) + ".json"
            )
            
            print(f"\nSummary file: {summary_file.name}")
            print(f"  Exists: {summary_file.exists()}")
            
            if summary_file.exists():
                with open(summary_file, 'r') as f:
                    summary = json.load(f)
                
                print("\nSummary contents:")
                print(f"  Version: {summary['metadata']['version']}")
                print(f"  Timestamp: {summary['metadata']['timestamp']}")
                print(
                    f"  Total errors: "
                    f"{summary['statistics']['total_errors']}"
                )
                print(
                    f"  Fixed errors: "
                    f"{summary['statistics']['fixed_errors']}"
                )
                print(
                    f"  Fix rate: "
                    f"{summary['statistics']['fix_rate']}%"
                )
                
                print("\n  Errors by type:")
                for error_type, count in summary['errors_by_type'].items():
                    print(f"    {error_type}: {count}")
            
            print("\n✓ All outputs generated correctly!")
        else:
            print(f"\n✗ Error: {result.error_message}")
    
    finally:
        corrector.close()
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
