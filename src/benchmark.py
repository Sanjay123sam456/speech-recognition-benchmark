"""
Main Benchmark Script
Runs all ASR engines on audio dataset and saves results
"""

import pandas as pd
import os
import sys
from pathlib import Path
from tqdm import tqdm

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from asr_engines.deepgram_engine import DeepgramEngine
from asr_engines.whisper_engine import WhisperEngine
from asr_engines.google_engine import GoogleEngine

def main():
    print("="*60)
    print("ASR BENCHMARK - Starting Evaluation")
    print("="*60)
    
    # Load ground truth labels
    labels_path = "data/labels/labels.csv"
    if not os.path.exists(labels_path):
        print(f"Error: {labels_path} not found")
        return
    
    labels_df = pd.read_csv(labels_path)
    print(f"\n✓ Loaded {len(labels_df)} audio samples from labels.csv")
    
    # Initialize ASR engines
    print("\n" + "="*60)
    print("Initializing ASR Engines...")
    print("="*60)
    
    try:
        deepgram = DeepgramEngine()
        print("✓ Deepgram initialized")
    except Exception as e:
        print(f"✗ Deepgram initialization failed: {e}")
        print("  Check your .env file and DEEPGRAM_API_KEY")
        return
    
    whisper_base = WhisperEngine(model_size="base")
    whisper_small = WhisperEngine(model_size="small")
    print("✓ Whisper models loaded")
    google = GoogleEngine()
    print("✓ Google Cloud Speech initialized")
    
    # Store all results
    all_results = []
    
    # Process each audio file
    print("\n" + "="*60)
    print("Processing Audio Files...")
    print("="*60)
    
    for idx, row in tqdm(labels_df.iterrows(), total=len(labels_df), desc="Overall Progress"):
        filename = row['filename']
        ground_truth = row['transcript']
        audio_path = f"data/audio/{filename}"
        
        print(f"\n[{idx+1}/{len(labels_df)}] {filename}")
        
        if not os.path.exists(audio_path):
            print(f"  ⚠️  File not found: {audio_path}")
            continue
        
        # Run Deepgram
        print("  • Deepgram...", end=" ", flush=True)
        dg_result = deepgram.transcribe(audio_path)
        print(f"✓ ({dg_result['latency']:.2f}s)")
        
        # Run Whisper Base
        print("  • Whisper Base...", end=" ", flush=True)
        wb_result = whisper_base.transcribe(audio_path)
        print(f"✓ ({wb_result['latency']:.2f}s)")
        
        # Run Whisper Small
        print("  • Whisper Small...", end=" ", flush=True)
        ws_result = whisper_small.transcribe(audio_path)
        print(f"✓ ({ws_result['latency']:.2f}s)")

        # Run Google Cloud Speech
        print("  • Google Cloud...", end=" ", flush=True)
        google_result = google.transcribe(audio_path)
        print(f"✓ ({google_result['latency']:.2f}s)")
        
        # Store results
        all_results.append({
            "filename": filename,
            "ground_truth": ground_truth,
            
            # Deepgram
            "deepgram_transcript": dg_result["transcript"],
            "deepgram_latency": dg_result["latency"],
            "deepgram_confidence": dg_result["confidence"],
            "deepgram_status": dg_result["status"],
            
            # Whisper Base
            "whisper_base_transcript": wb_result["transcript"],
            "whisper_base_latency": wb_result["latency"],
            "whisper_base_status": wb_result["status"],
            
            # Whisper Small
            "whisper_small_transcript": ws_result["transcript"],
            "whisper_small_latency": ws_result["latency"],
            "whisper_small_status": ws_result["status"],

            # Google Cloud Speech
            "google_transcript": google_result["transcript"],
            "google_latency": google_result["latency"],
            "google_confidence": google_result["confidence"],
            "google_status": google_result["status"],
        })
        
        print(f"  Ground Truth: {ground_truth}")
        print(f"  Deepgram:     {dg_result['transcript']}")
        print(f"  Google Cloud:  {google_result['transcript']}")
        print(f"  Whisper Base: {wb_result['transcript']}")
        print(f"  Whisper Small: {ws_result['transcript']}")
        
    
    # Save results
    print("\n" + "="*60)
    print("Saving Results...")
    print("="*60)
    
    results_df = pd.DataFrame(all_results)
    
    # Create results directory if it doesn't exist
    os.makedirs("results/transcriptions", exist_ok=True)
    
    output_path = "results/transcriptions/all_transcripts.csv"
    results_df.to_csv(output_path, index=False)
    
    print(f"\n✓ Results saved to: {output_path}")
    print(f"✓ Total samples processed: {len(results_df)}")
    
    print("\n" + "="*60)
    print("BENCHMARK COMPLETE!")
    print("="*60)
    print("\nNext step: Run 'python src/calculate_metrics_by_condition.py' to analyze results")


if __name__ == "__main__":
    main()
