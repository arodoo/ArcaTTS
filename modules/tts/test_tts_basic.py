# Simple TTS test
# Test basic audio generation with XTTS-v2

from modules.tts.domain.tts_engine import TTSEngine
from pathlib import Path


def test_tts_basic():
    """Test basic TTS functionality."""
    print("Initializing TTS engine...")
    
    engine = TTSEngine(language="es")
    
    print(f"Language: {engine.language}")
    print("Loading Piper voice model...")
    
    engine.load_model()
    
    print("Model loaded!")
    
    # Test with Kafka text sample
    test_text = """
    Algunas personas se levantaron casi a las doce; 
    después de hacer reverencias, darse las manos y 
    decir que todo había sido muy agradable.
    """
    
    output_dir = Path("outputs/test")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    output_file = output_dir / "kafka_sample.wav"
    
    print(f"\nGenerating audio...")
    print(f"Text: {test_text[:60]}...")
    
    success = engine.synthesize(
        text=test_text,
        output_path=str(output_file)
    )
    
    if success:
        file_size = output_file.stat().st_size
        print(f"\n✓ Audio generated!")
        print(f"  File: {output_file}")
        print(f"  Size: {file_size / 1024:.1f} KB")
    else:
        print("\n✗ Audio generation failed")


if __name__ == "__main__":
    test_tts_basic()
