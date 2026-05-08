import pandas as pd
from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate
import jellyfish

# Load results
df = pd.read_csv('results/transcriptions/all_transcripts.csv')

# Define conditions based on filename patterns
def get_condition(filename):
    if 'metro_phone' in filename:
        return 'Metro + Phone'
    elif 'metro_earphone' in filename:
        return 'Metro + Earphone'
    else:
        return 'Normal (Quiet)'

# Add condition column
df['condition'] = df['filename'].apply(get_condition)

# Transliteration function
def normalize_text(text):
    if pd.isna(text) or text == '':
        return ''
    try:
        # Try to transliterate from Devanagari to Roman
        romanized = transliterate(str(text), sanscript.DEVANAGARI, sanscript.ITRANS)
        return romanized.lower().strip()
    except Exception:
        return str(text).lower().strip()

# WER calculation using Jaro-Winkler
def calculate_wer(reference, hypothesis):
    ref_normalized = normalize_text(reference)
    hyp_normalized = normalize_text(hypothesis)
    
    if not ref_normalized or not hyp_normalized:
        return 100.0
    
    similarity = jellyfish.jaro_winkler_similarity(ref_normalized, hyp_normalized)
    wer = (1 - similarity) * 100
    return wer

# Locality extraction check
def check_locality_extracted(reference, hypothesis, locality_names):
    ref_normalized = normalize_text(reference)
    hyp_normalized = normalize_text(hypothesis)
    
    for locality in locality_names:
        locality_norm = normalize_text(locality)
        if locality_norm in ref_normalized and locality_norm in hyp_normalized:
            return True
    return False

# List of localities
localities = [
    'Indiranagar', 'Koramangala', 'Whitefield', 'Electronic City', 'Marathahalli',
    'Jayanagar', 'Rajajinagar', 'Hebbal', 'Yelahanka', 'Banashankari',
    'HSR Layout', 'BTM Layout', 'Majestic', 'Silk Board', 'Bellandur',
    'Sarjapur', 'Bommanahalli', 'KR Puram', 'Peenya', 'Yeshwanthpur'
]

# Models to evaluate
models = {
    'Deepgram': 'deepgram_transcript',
    'Google Cloud': 'google_transcript',
    'Whisper Base': 'whisper_base_transcript',
    'Whisper Small': 'whisper_small_transcript'
}

# Conditions
conditions = ['Normal (Quiet)', 'Metro + Phone', 'Metro + Earphone']

print("=" * 80)
print("CALCULATING METRICS BY CONDITION")
print("=" * 80)

# Store results
all_results = []

for condition in conditions:
    print(f"\n{'=' * 80}")
    print(f"CONDITION: {condition}")
    print(f"{'=' * 80}")
    
    # Filter data for this condition
    condition_df = df[df['condition'] == condition].copy()
    n_samples = len(condition_df)
    
    print(f"Samples: {n_samples}")
    print()
    
    for model_name, transcript_col in models.items():
        # Calculate WER
        wers = []
        for _, row in condition_df.iterrows():
            wer = calculate_wer(row['ground_truth'], row[transcript_col])
            wers.append(wer)
        
        avg_wer = sum(wers) / len(wers) if wers else 100.0
        
        # Calculate Locality Accuracy
        correct_extractions = 0
        for _, row in condition_df.iterrows():
            if check_locality_extracted(row['ground_truth'], row[transcript_col], localities):
                correct_extractions += 1
        
        locality_accuracy = (correct_extractions / n_samples) * 100 if n_samples > 0 else 0.0
        
        # Calculate Latency
        latency_col = f"{transcript_col.replace('_transcript', '_latency')}"
        avg_latency = condition_df[latency_col].mean() if latency_col in condition_df.columns else 0.0
        
        print(f"{model_name}:")
        print(f"  • WER: {avg_wer:.2f}%")
        print(f"  • Locality Extraction Accuracy: {locality_accuracy:.2f}%")
        print(f"  • Avg Latency: {avg_latency:.2f}s")
        print()
        
        # Store result
        all_results.append({
            'Condition': condition,
            'Model': model_name,
            'WER (%)': round(avg_wer, 2),
            'Locality Extraction Accuracy (%)': round(locality_accuracy, 2),
            'Avg Latency (s)': round(avg_latency, 2)
        })

# Create results dataframe
results_df = pd.DataFrame(all_results)

# Save to CSV
results_df.to_csv('results/metrics/comparison_by_condition.csv', index=False)
print("=" * 80)
print("✓ Results saved to: results/metrics/comparison_by_condition.csv")
print("=" * 80)

# Print summary tables
print("\n" + "=" * 80)
print("SUMMARY BY CONDITION")
print("=" * 80)

for condition in conditions:
    print(f"\n{condition}:")
    condition_results = results_df[results_df['Condition'] == condition]
    print(condition_results[['Model', 'WER (%)', 'Locality Extraction Accuracy (%)', 'Avg Latency (s)']].to_string(index=False))

# Calculate degradation
print("\n" + "=" * 80)
print("DEGRADATION ANALYSIS (Normal → Noisy)")
print("=" * 80)

for model_name in models.keys():
    normal_wer = results_df[(results_df['Condition'] == 'Normal (Quiet)') & 
                            (results_df['Model'] == model_name)]['WER (%)'].values[0]
    
    metro_phone_wer = results_df[(results_df['Condition'] == 'Metro + Phone') & 
                                  (results_df['Model'] == model_name)]['WER (%)'].values[0]
    
    metro_earphone_wer = results_df[(results_df['Condition'] == 'Metro + Earphone') & 
                                     (results_df['Model'] == model_name)]['WER (%)'].values[0]
    
    avg_noisy_wer = (metro_phone_wer + metro_earphone_wer) / 2
    degradation = avg_noisy_wer - normal_wer
    
    print(f"\n{model_name}:")
    print(f"  Normal: {normal_wer:.2f}%")
    print(f"  Metro+Phone: {metro_phone_wer:.2f}%")
    print(f"  Metro+Earphone: {metro_earphone_wer:.2f}%")
    print(f"  Avg Noisy: {avg_noisy_wer:.2f}%")
    print(f"  Degradation: {degradation:+.2f}%")

print("\n" + "=" * 80)
print("✓ Analysis complete!")
print("=" * 80)