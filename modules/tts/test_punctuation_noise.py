"""Test punctuation noise WITHOUT audio enhancer."""
from pathlib import Path
from modules.tts.domain.enhanced_text_processor import (
    EnhancedTextProcessor
)
from modules.tts.domain.silence_generator import (
    SilenceGenerator
)
from modules.tts.domain.wav_merger import WavMerger
from modules.tts.domain.mp3_converter import Mp3Converter
from piper import PiperVoice
from piper.config import SynthesisConfig
import wave


def synthesize_raw(text: str, output_path: str):
    """Synthesize WITHOUT audio enhancer."""
    model_path = "models/piper/es_MX-claude-high.onnx"
    config_path = "models/piper/es_MX-claude-high.onnx.json"
    
    voice = PiperVoice.load(
        model_path,
        use_cuda=False,
        config_path=config_path
    )
    
    config = SynthesisConfig(
        length_scale=1.0,
        noise_scale=0.667,
        noise_w_scale=0.8,
        normalize_audio=True,
        volume=1.0
    )
    
    chunks = list(voice.synthesize(text, config))
    audio_data = b''.join([
        chunk.audio_int16_bytes 
        for chunk in chunks
    ])
    
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    
    with wave.open(output_path, 'wb') as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(voice.config.sample_rate)
        f.writeframes(audio_data)


def test_punctuation_noise():
    """Test if noise comes from Piper or enhancer."""
    output_dir = Path("outputs/test/punctuation_noise")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    tests = {
        "ellipsis": "No sé qué decir... quizás mañana.",
        "semicolon": "Es importante; sin embargo, no urgente.",
        "period": "Esto es una oración. Esta es otra.",
        "comma": "Uno, dos, tres, cuatro.",
    }
    
    processor = EnhancedTextProcessor()
    silence_gen = SilenceGenerator()
    
    for name, text in tests.items():
        print(f"\n{name.upper()}:")
        print(f"Original: {text}")
        
        chunks = processor.prepare_work_text(text, add_title_pause=False)
        print(f"Chunks: {len(chunks)}")
        for i, c in enumerate(chunks):
            print(f"  {i}: {repr(c)[:80]}")
        
        # Generate chunks
        for i, chunk in enumerate(chunks):
            chunk_path = output_dir / f"{name}_chunk_{i:03d}.wav"
            
            if chunk.startswith('<silence:'):
                duration = float(chunk.split(':')[1].rstrip('>'))
                silence_gen.generate_silence(duration, str(chunk_path))
            else:
                # RAW synthesis, NO enhancer
                synthesize_raw(chunk, str(chunk_path))
        
        # Merge
        merger = WavMerger()
        chunk_files = sorted(output_dir.glob(f"{name}_chunk_*.wav"))
        wav_file = output_dir / f"{name}_raw.wav"
        
        merger.merge(
            input_files=[str(f) for f in chunk_files],
            output_file=str(wav_file)
        )
        
        # Convert to MP3
        converter = Mp3Converter(bitrate="128k")
        mp3_file = converter.convert(
            wav_path=str(wav_file),
            cleanup=False
        )
        
        print(f"✓ Generated: {mp3_file}")
    
    print("\n" + "=" * 60)
    print("RAW AUDIO TESTS COMPLETE (no enhancer)")
    print("=" * 60)
    print("\nCheck outputs/test/punctuation_noise/")
    print("If noise persists, it's from Piper, not enhancer")


if __name__ == "__main__":
    test_punctuation_noise()
