"""
Compare audio quality with and without enhancements.
"""
from modules.tts.domain.tts_engine import TTSEngine
from pathlib import Path


def test_quality_comparison():
    """Generate two versions: normal and enhanced."""
    
    text = """
    En un lugar de la Mancha, de cuyo nombre no quiero acordarme,
    no ha mucho tiempo que vivía un hidalgo de los de lanza en astillero,
    adarga antigua, rocín flaco y galgo corredor.
    """
    
    output_dir = Path("outputs/test")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print("Generating NORMAL version (no enhancements)...")
    engine_normal = TTSEngine(language="es", enhance_quality=False)
    engine_normal.synthesize(
        text=text,
        output_path=str(output_dir / "normal_quality.wav")
    )
    print("✓ Normal: outputs/test/normal_quality.wav")
    
    print("\nGenerating ENHANCED version (with improvements)...")
    engine_enhanced = TTSEngine(language="es", enhance_quality=True)
    engine_enhanced.synthesize(
        text=text,
        output_path=str(output_dir / "enhanced_quality.wav"),
        speed=0.95  # Slightly slower for clarity
    )
    print("✓ Enhanced: outputs/test/enhanced_quality.wav")
    
    print("\n" + "="*50)
    print("Comparison ready!")
    print("="*50)
    print("\nListen to both files to hear the difference:")
    print("1. normal_quality.wav   - Standard Piper output")
    print("2. enhanced_quality.wav - Professional-grade processing")
    print("\nEnhancements applied (community best practices):")
    print("  ✓ Spectral enhancement (clarity boost)")
    print("  ✓ Dynamic EQ (de-essing for smoothness)")
    print("  ✓ Vocal presence (1-4kHz intimacy)")
    print("  ✓ Micro-humanization (natural variations)")
    print("  ✓ Multi-band limiting (preserves dynamics)")
    print("  ✓ Optimized synthesis parameters")
    print("\nBased on research:")
    print("  • Neural TTS post-processing techniques")
    print("  • Natural speech pattern analysis")
    print("  • Professional audio engineering practices")


if __name__ == "__main__":
    test_quality_comparison()
