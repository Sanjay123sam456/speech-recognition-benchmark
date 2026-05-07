"""
Calculate Metrics
Computes WER, Locality Accuracy, and other metrics from benchmark results
Uses transliteration to handle script differences (Devanagari vs Roman)
"""

import pandas as pd
from jiwer import wer
import re
import os
from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate


# List of Bangalore localities in the dataset
LOCALITIES = [
    "Indiranagar", "Whitefield", "Koramangala", "Electronic City",
    "Marathahalli", "Jayanagar", "Rajajinagar", "Hebbal",
    "Yelahanka", "Banashankari", "HSR Layout", "BTM Layout",
    "Majestic", "Silk Board", "Bellandur", "Sarjapur",
    "Bommanahalli", "KR Puram", "Peenya", "Yeshwanthpur"
]


def transliterate_to_roman(text):
    """
    Convert Devanagari/other Indic scripts to Roman (ITRANS)
    
    Args:
        text: Input text (may be Devanagari, Roman, or mixed)
        
    Returns:
        Romanized text
    """
    if not text or pd.isna(text):
        return ""
    
    text = str(text)
    
    try:
        # Try to transliterate from Devanagari to Roman (ITRANS)
        romanized = transliterate(text, sanscript.DEVANAGARI, sanscript.ITRANS)
        return romanized
    except:
        # If transliteration fails, text is probably already in Roman
        return text


def normalize_text(text):
    """
    Normalize text for comparison - transliterate, remove punctuation, lowercase
    
    Args:
        text: Input text
        
    Returns:
        Normalized text
    """
    if not text or pd.isna(text):
        return ""
    
    # Convert to string
    text = str(text)
    
    # Transliterate to Roman script
    text = transliterate_to_roman(text)
    
    # Remove punctuation
    text = re.sub(r'[^\w\s]', '', text)
    
    # Convert to lowercase
    text = text.lower().strip()
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    
    return text


def extract_locality(text, localities):
    """
    Extract locality name from transcript
    
    Args:
        text: Transcript text
        localities: List of locality names
        
    Returns:
        Locality name if found, None otherwise
    """
    if not text or pd.isna(text):
        return None
    
    # Normalize text
    text_normalized = normalize_text(text)
    
    for loc in localities:
        # Normalize locality name
        loc_normalized = loc.lower()
        
        # Handle special cases
        loc_variations = [loc_normalized]
        
        # Add common variations
        if loc == "HSR Layout":
            loc_variations.extend(["hsr", "hsr layout", "h s r"])
        elif loc == "BTM Layout":
            loc_variations.extend(["btm", "btm layout", "b t m"])
        elif loc == "Electronic City":
            loc_variations.extend(["electronic city", "electronic", "elektronik"])
        elif loc == "Silk Board":
            loc_variations.extend(["silk board", "silkboard", "silk"])
        elif loc == "KR Puram":
            loc_variations.extend(["kr puram", "kr", "puram", "k r puram"])
        elif loc == "Indiranagar":
            loc_variations.extend(["indira nagar", "indiranagar"])
        
        for variation in loc_variations:
            if variation in text_normalized:
                return loc
    
    return None


def calculate_wer_for_model(df, transcript_col, ground_truth_col="ground_truth"):
    """
    Calculate Word Error Rate for a model
    Uses transliteration and normalization to handle script differences
    
    Args:
        df: DataFrame with results
        transcript_col: Column name with model predictions
        ground_truth_col: Column name with ground truth
        
    Returns:
        Average WER as percentage
    """
    wer_scores = []
    
    for _, row in df.iterrows():
        gt = normalize_text(row[ground_truth_col])
        pred = normalize_text(row[transcript_col])
        
        # Skip if either is empty
        if not gt or not pred:
            continue
            
        try:
            wer_score = wer(gt, pred)
            # Cap WER at 1.0 (100%)
            wer_score = min(wer_score, 1.0)
            wer_scores.append(wer_score)
        except Exception as e:
            # If WER calculation fails, count as 100% error
            wer_scores.append(1.0)
    
    avg_wer = (sum(wer_scores) / len(wer_scores) * 100) if wer_scores else 100.0
    return round(avg_wer, 2)


def calculate_locality_accuracy(df, transcript_col, ground_truth_col="ground_truth"):
    """
    Calculate locality name extraction accuracy
    
    Args:
        df: DataFrame with results
        transcript_col: Column name with model predictions
        ground_truth_col: Column name with ground truth
        
    Returns:
        Accuracy percentage and detailed results
    """
    correct = 0
    total = 0
    failures = []
    
    for idx, row in df.iterrows():
        gt_text = str(row[ground_truth_col])
        pred_text = str(row[transcript_col])
        
        # Extract localities
        gt_locality = extract_locality(gt_text, LOCALITIES)
        pred_locality = extract_locality(pred_text, LOCALITIES)
        
        if gt_locality:  # Only count if ground truth has a locality
            total += 1
            if gt_locality == pred_locality:
                correct += 1
            else:
                failures.append({
                    "filename": row["filename"],
                    "expected": gt_locality,
                    "predicted": pred_locality,
                    "ground_truth": gt_text,
                    "transcript": pred_text
                })
    
    accuracy = (correct / total * 100) if total > 0 else 0
    return round(accuracy, 2), failures


def main():
    print("="*60)
    print("CALCULATING METRICS (with transliteration)")
    print("="*60)
    
    # Load results
    results_path = "results/transcriptions/all_transcripts.csv"
    
    if not os.path.exists(results_path):
        print(f"\nError: {results_path} not found")
        print("Please run 'python src/benchmark.py' first")
        return
    
    df = pd.read_csv(results_path)
    print(f"\n✓ Loaded {len(df)} results from {results_path}")
    
    # Calculate metrics for each model
    print("\n" + "="*60)
    print("Computing Metrics...")
    print("="*60)
    
    models = {
        "Deepgram": "deepgram_transcript",
        "Google Cloud": "google_transcript",
        "Whisper Base": "whisper_base_transcript",
        "Whisper Small": "whisper_small_transcript"
    }
    
    results = []
    
    for model_name, transcript_col in models.items():
        print(f"\n{model_name}:")
        
        # WER
        wer_score = calculate_wer_for_model(df, transcript_col)
        print(f"  • WER: {wer_score}%")
        
        # Locality Accuracy
        locality_acc, failures = calculate_locality_accuracy(df, transcript_col)
        print(f"  • Locality Accuracy: {locality_acc}%")
        
        # Average Latency
        latency_col = transcript_col.replace("_transcript", "_latency")
        avg_latency = df[latency_col].mean()
        print(f"  • Avg Latency: {avg_latency:.2f}s")
        
        results.append({
            "Model": model_name,
            "WER (%)": wer_score,
            "Locality Accuracy (%)": locality_acc,
            "Avg Latency (s)": round(avg_latency, 2)
        })
    
    # Create comparison table
    comparison_df = pd.DataFrame(results)
    
    # Display results
    print("\n" + "="*60)
    print("BENCHMARK RESULTS")
    print("="*60)
    print("\n" + comparison_df.to_string(index=False))
    print("\n" + "="*60)
    
    # Save metrics
    os.makedirs("results/metrics", exist_ok=True)
    metrics_path = "results/metrics/comparison.csv"
    comparison_df.to_csv(metrics_path, index=False)
    print(f"\n✓ Metrics saved to: {metrics_path}")
    
    # Find best model
    best_wer = comparison_df.loc[comparison_df["WER (%)"].idxmin()]
    best_locality = comparison_df.loc[comparison_df["Locality Accuracy (%)"].idxmax()]
    fastest = comparison_df.loc[comparison_df["Avg Latency (s)"].idxmin()]
    
    print("\n" + "="*60)
    print("KEY INSIGHTS")
    print("="*60)
    print(f"\n• Best WER: {best_wer['Model']} ({best_wer['WER (%)']}%)")
    print(f"• Best Locality Accuracy: {best_locality['Model']} ({best_locality['Locality Accuracy (%)']}%)")
    print(f"• Fastest: {fastest['Model']} ({fastest['Avg Latency (s)']}s avg)")
    
    print("\n✓ Analysis complete!")


if __name__ == "__main__":
    main()