"""
Deepgram ASR Engine Wrapper
Handles transcription using Deepgram API
"""

from deepgram import DeepgramClient
import os
import time
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")


class DeepgramEngine:
    """Wrapper for Deepgram ASR API"""
    
    def __init__(self):
        api_key = os.getenv("DEEPGRAM_API_KEY")
        if not api_key:
            raise ValueError("DEEPGRAM_API_KEY not found in .env file")
        
        # SDK v7 initialization with config
        self.client = DeepgramClient(api_key=api_key)
        self.model_name = "nova-2"
    
    def transcribe(self, audio_path):
        """
        Transcribe audio file using Deepgram
        
        Args:
            audio_path: Path to audio file
            
        Returns:
            dict with transcript, latency, confidence, status
        """
        start_time = time.time()
        
        try:
            # Read audio file
            with open(audio_path, "rb") as file:
                buffer_data = file.read()
            
            # Transcribe
            response = self.client.listen.v1.media.transcribe_file(
                request=buffer_data,
                model=self.model_name,
                language="hi",
                smart_format=True,
            )
            
            latency = time.time() - start_time
            
            # Extract results
            result = response.results.channels[0].alternatives[0]
            
            return {
                "transcript": result.transcript,
                "latency": latency,
                "confidence": getattr(result, 'confidence', None),
                "words": getattr(result, 'words', []),
                "status": "success",
                "model": self.model_name
            }
        
        except Exception as e:
            return {
                "transcript": "",
                "latency": time.time() - start_time,
                "confidence": None,
                "words": [],
                "status": f"error: {str(e)}",
                "model": self.model_name
            }


if __name__ == "__main__":
    # Test the engine
    print("Testing Deepgram Engine...")
    
    try:
        engine = DeepgramEngine()
        print("✓ Engine initialized")
    except Exception as e:
        print(f"✗ Initialization failed: {e}")
        exit(1)
    
    # Test file path
    test_file = "data/audio/01_indiranagar_normal.ogg"
    
    if os.path.exists(test_file):
        print(f"\nTranscribing: {test_file}")
        result = engine.transcribe(test_file)
        print(f"\nStatus: {result['status']}")
        print(f"Transcript: {result['transcript']}")
        print(f"Latency: {result['latency']:.2f}s")
        print(f"Confidence: {result['confidence']}")
    else:
        print(f"✗ Test file not found: {test_file}")
        print("Make sure you're running from the project root directory")
