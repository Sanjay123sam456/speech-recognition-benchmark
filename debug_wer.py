import pandas as pd

df = pd.read_csv("results/transcriptions/all_transcripts.csv")

print("Sample comparisons:")
print("="*80)

for i in range(min(3, len(df))):
    row = df.iloc[i]
    print(f"\nFile: {row['filename']}")
    print(f"Ground Truth: {row['ground_truth']}")
    print(f"Deepgram:     {row['deepgram_transcript']}")
    print(f"Whisper Base: {row['whisper_base_transcript']}")
    print(f"Whisper Small: {row['whisper_small_transcript']}")
    print("-"*80)