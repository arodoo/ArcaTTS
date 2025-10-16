#!/usr/bin/env python3
"""Simple Piper TTS test script."""

from piper import PiperVoice
import wave
from pathlib import Path

# Create output directory
output_dir = Path("outputs/test")
output_dir.mkdir(parents=True, exist_ok=True)

# Test with Spanish voice (using downloaded model)
print("Loading Piper Spanish voice...")
try:
    model_path = Path("models/piper/es_ES-sharvard-medium.onnx").absolute()
    config_path = model_path.with_suffix('.onnx.json')
    
    print(f"Model: {model_path}")
    print(f"Config: {config_path}")
    print(f"Model exists: {model_path.exists()}")
    print(f"Config exists: {config_path.exists()}")
    
    voice = PiperVoice.load(
        str(model_path),
        use_cuda=False,
        config_path=str(config_path)
    )
    
    output_file = output_dir / "piper_test_es.wav"
    
    print("Generating Spanish audio...")
    text = "Hola mundo, esta es una prueba de Piper"
    
    # Synthesize returns an iterable of audio chunks
    audio_chunks = list(voice.synthesize(text))
    
    # Combine all audio data
    audio_data = b''.join([chunk.audio_int16_bytes for chunk in audio_chunks])
    
    # Write to WAV file
    with wave.open(str(output_file), 'wb') as f:
        f.setnchannels(1)  # Mono
        f.setsampwidth(2)  # 16-bit
        f.setframerate(voice.config.sample_rate)
        f.writeframes(audio_data)
    
    print(f"Success! Audio saved to: {output_file}")
    print(f"File size: {output_file.stat().st_size / 1024:.1f} KB")
    
except Exception as e:
    print(f"Error: {e}")
    print("\nTrying alternative approach...")
    
    # Try loading with full model path
    import os
    print(f"Current dir: {os.getcwd()}")
    print("Available models in models/piper/:")
    if Path("models/piper").exists():
        for item in Path("models/piper").iterdir():
            print(f"  - {item.name}")
