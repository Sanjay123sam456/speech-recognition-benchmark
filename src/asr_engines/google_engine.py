"""
Google Cloud Speech-to-Text Engine Wrapper
Handles transcription using Google Cloud Speech API
Converts OGG to FLAC format for compatibility
"""

from google.cloud import speech
from pydub import AudioSegment
import os
import time
import io
import tempfile

class GoogleEngine:
    """Wrapper for Google Cloud Speech-to-Text API"""
    
    def __init__(self, credentials_path="google-credentials.json"):
        """
        Initialize Google Cloud Speech client
        
        Args:
            credentials_path: Path to service account JSON key
        """
        # Set credentials environment variable
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path
        
        # Initialize client
        self.client = speech.SpeechClient()
        self.model_name = "google-cloud-speech"
    
    def transcribe(self, audio_path):
        """
        Transcribe audio file using Google Cloud Speech
        Converts OGG to FLAC format automatically
        
        Args:
            audio_path: Path to audio file (.ogg)
            
        Returns:
            dict with transcript, latency, confidence, status
        """
        start_time = time.time()
        
        try:
            # Convert OGG to FLAC for Google Cloud compatibility
            audio = AudioSegment.from_ogg(audio_path)
            
            # Create temporary FLAC file
            with tempfile.NamedTemporaryFile(suffix=".flac", delete=False) as temp_file:
                temp_path = temp_file.name
                audio.export(temp_path, format="flac")
            
            # Read FLAC file
            with io.open(temp_path, "rb") as audio_file:
                content = audio_file.read()
            
            # Clean up temporary file
            os.unlink(temp_path)
            
            # Prepare audio for Google Cloud
            audio_obj = speech.RecognitionAudio(content=content)
            
            # Configure recognition
            config = speech.RecognitionConfig(
                encoding=speech.RecognitionConfig.AudioEncoding.FLAC,
                language_code="hi-IN",  # Hindi (India)
                enable_automatic_punctuation=True,
            )
            
            # Transcribe
            response = self.client.recognize(config=config, audio=audio_obj)
            
            latency = time.time() - start_time
            
            # Extract results
            if response.results:
                result = response.results[0].alternatives[0]
                
                return {
                    "transcript": result.transcript,
                    "latency": latency,
                    "confidence": result.confidence if hasattr(result, 'confidence') else None,
                    "status": "success",
                    "model": self.model_name
                }
            else:
                # No speech detected
                return {
                    "transcript": "",
                    "latency": latency,
                    "confidence": None,
                    "status": "no_speech_detected",
                    "model": self.model_name
                }
        
        except Exception as e:
            return {
                "transcript": "",
                "latency": time.time() - start_time,
                "confidence": None,
                "status": f"error: {str(e)}",
                "model": self.model_name
            }


if __name__ == "__main__":
    # Test the engine
    print("Testing Google Cloud Speech Engine...")
    print("(Converting OGG to FLAC format automatically)\n")
    
    try:
        engine = GoogleEngine()
        print("✓ Engine initialized")
    except Exception as e:
        print(f"✗ Initialization failed: {e}")
        print("Make sure google-credentials.json is in the project root")
        exit(1)
    
    # Test file path
    test_file = "data/audio/03_whitefield_normal.ogg"
    
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