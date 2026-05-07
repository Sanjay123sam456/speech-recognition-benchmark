"""
Whisper ASR Engine Wrapper
Handles transcription using OpenAI Whisper (local)
"""

import whisper
import time
import os
import sys
import shutil
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")


def ensure_ffmpeg_available():
    """Add imageio-ffmpeg's bundled binary to PATH when system ffmpeg is absent."""
    if shutil.which("ffmpeg"):
        return

    try:
        import imageio_ffmpeg
    except ImportError:
        return

    ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()
    tools_dir = Path(__file__).resolve().parents[2] / "tools"
    tools_dir.mkdir(exist_ok=True)
    shim_path = tools_dir / "ffmpeg.exe"

    if not shim_path.exists():
        shutil.copy2(ffmpeg_path, shim_path)

    os.environ["PATH"] = str(tools_dir) + os.pathsep + os.environ.get("PATH", "")


class WhisperEngine:
    """Wrapper for OpenAI Whisper ASR"""
    
    def __init__(self, model_size="base"):
        """
        Initialize Whisper model
        
        Args:
            model_size: One of ['tiny', 'base', 'small', 'medium', 'large']
        """
        ensure_ffmpeg_available()
        print(f"Loading Whisper {model_size} model...")
        self.model = whisper.load_model(model_size)
        self.model_size = model_size
        print(f"✓ Whisper {model_size} loaded")
    
    def transcribe(self, audio_path):
        """
        Transcribe audio file using Whisper
        
        Args:
            audio_path: Path to audio file
            
        Returns:
            dict with transcript, latency, status
        """
        start_time = time.time()
        
        try:
            # Transcribe
            result = self.model.transcribe(
                audio_path,
                language="hi",  # Hindi
                task="transcribe"
            )
            
            latency = time.time() - start_time
            
            return {
                "transcript": result["text"].strip(),
                "latency": latency,
                "confidence": None,  # Whisper doesn't provide confidence scores
                "segments": result.get("segments", []),
                "status": "success",
                "model": f"whisper-{self.model_size}"
            }
        
        except Exception as e:
            return {
                "transcript": "",
                "latency": time.time() - start_time,
                "confidence": None,
                "segments": [],
                "status": f"error: {str(e)}",
                "model": f"whisper-{self.model_size}"
            }


if __name__ == "__main__":
    # Test the engine
    print("Testing Whisper Engine...")
    engine = WhisperEngine(model_size="small")
    
    # Test file path (adjust as needed)
    test_file = "data/audio/03_whitefield_normal.ogg"  # Try file 03
    
    if os.path.exists(test_file):
        result = engine.transcribe(test_file)
        print(f"\nStatus: {result['status']}")
        print(f"Transcript: {result['transcript']}")
        print(f"Latency: {result['latency']:.2f}s")
    else:
        print(f"Test file not found: {test_file}")
