"""
Quick test of grammar correction.
Tests with a small Spanish text sample.
"""
from modules.grammar.domain.corrector import TextCorrector


def main():
    # Test text with intentional errors
    test_text = """
    Este es un texto de prueva con algunos errores.
    Ay muchos problemas gramaticales aqui.
    Tambien falta algunos signos de puntuacion
    
    ¿Podra el corrector arreglar estos problemas?
    """
    
    print("=" * 60)
    print("GRAMMAR CORRECTION TEST")
    print("=" * 60)
    
    corrector = TextCorrector(language="es")
    
    try:
        # Check for errors
        errors = corrector.checker.check_text(test_text)
        
        print(f"\nFound {len(errors)} errors:\n")
        
        for i, error in enumerate(errors[:10], 1):
            print(f"{i}. [{error.error_type.value}]")
            print(f"   Message: {error.message}")
            print(f"   Original: '{error.original_text}'")
            if error.suggested_replacement:
                print(
                    f"   Suggested: "
                    f"'{error.suggested_replacement}'"
                )
            print()
        
        if len(errors) > 10:
            print(f"... and {len(errors) - 10} more errors")
    
    finally:
        corrector.close()
    
    print("\n" + "=" * 60)
    print("Test complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
