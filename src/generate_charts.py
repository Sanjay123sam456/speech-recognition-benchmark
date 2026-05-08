import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os

# ============================================================
# Load Data
# ============================================================

results_df = pd.read_csv('results/metrics/comparison_by_condition.csv')

# Create output directory
os.makedirs('results/charts', exist_ok=True)

# Models and colors
models = ['Deepgram', 'Google Cloud', 'Whisper Small', 'Whisper Base']

colors = {
    'Deepgram': '#2ecc71',
    'Google Cloud': '#3498db',
    'Whisper Small': '#f39c12',
    'Whisper Base': '#e74c3c'
}

conditions = ['Normal (Quiet)', 'Metro + Phone', 'Metro + Earphone']

# ============================================================
# Chart 1: Condition-wise Approximate WER
# ============================================================

x = np.arange(len(conditions))
width = 0.2

fig, ax = plt.subplots(figsize=(12, 6))

for i, model in enumerate(models):
    model_data = results_df[results_df['Model'] == model]
    wer_values = model_data['WER (%)'].values

    bars = ax.bar(
        x + (i - 1.5) * width,
        wer_values,
        width,
        label=model,
        color=colors[model],
        edgecolor='black'
    )

    # Labels
    for bar in bars:
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width()/2,
            height + 0.5,
            f'{height:.1f}%',
            ha='center',
            va='bottom',
            fontsize=9
        )

ax.set_ylabel('Normalized Approximate WER (%)', fontsize=13, fontweight='bold')
ax.set_title('Condition-wise Normalized Approximate WER Comparison', fontsize=15, fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(conditions, fontsize=11)
ax.legend()
ax.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig('results/charts/wer_by_condition.png', dpi=300)
plt.close()

print("✅ Created: wer_by_condition.png")

# ============================================================
# Chart 2: Condition-wise Locality Accuracy
# ============================================================

fig, ax = plt.subplots(figsize=(12, 6))

for i, model in enumerate(models):
    model_data = results_df[results_df['Model'] == model]
    locality_values = model_data['Locality Extraction Accuracy (%)'].values

    bars = ax.bar(
        x + (i - 1.5) * width,
        locality_values,
        width,
        label=model,
        color=colors[model],
        edgecolor='black'
    )

    for bar in bars:
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width()/2,
            height + 0.3,
            f'{height:.1f}%',
            ha='center',
            va='bottom',
            fontsize=9
        )

ax.set_ylabel('Locality Extraction Accuracy (%)', fontsize=13, fontweight='bold')
ax.set_title('Condition-wise Locality Extraction Accuracy', fontsize=15, fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(conditions, fontsize=11)
ax.legend()
ax.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig('results/charts/locality_by_condition.png', dpi=300)
plt.close()

print("✅ Created: locality_by_condition.png")

# ============================================================
# Chart 3: Latency Comparison
# ============================================================

avg_latency = []

for model in models:
    model_data = results_df[results_df['Model'] == model]
    avg_latency.append(model_data['Avg Latency (s)'].mean())

plt.figure(figsize=(10, 6))

bars = plt.bar(
    models,
    avg_latency,
    color=[colors[m] for m in models],
    edgecolor='black'
)

for bar in bars:
    height = bar.get_height()
    plt.text(
        bar.get_x() + bar.get_width()/2,
        height + 0.1,
        f'{height:.2f}s',
        ha='center',
        fontsize=10
    )

plt.ylabel('Average Latency (s)', fontsize=13, fontweight='bold')
plt.title('Average Inference Latency', fontsize=15, fontweight='bold')
plt.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig('results/charts/latency_comparison.png', dpi=300)
plt.close()

print("✅ Created: latency_comparison.png")

# ============================================================
# Chart 4: Noise Degradation
# ============================================================

degradation_scores = []

for model in models:
    normal = results_df[
        (results_df['Model'] == model) &
        (results_df['Condition'] == 'Normal (Quiet)')
    ]['WER (%)'].values[0]

    metro_phone = results_df[
        (results_df['Model'] == model) &
        (results_df['Condition'] == 'Metro + Phone')
    ]['WER (%)'].values[0]

    metro_earphone = results_df[
        (results_df['Model'] == model) &
        (results_df['Condition'] == 'Metro + Earphone')
    ]['WER (%)'].values[0]

    noisy_avg = (metro_phone + metro_earphone) / 2
    degradation = noisy_avg - normal

    degradation_scores.append(degradation)

plt.figure(figsize=(10, 6))

bars = plt.bar(
    models,
    degradation_scores,
    color=[colors[m] for m in models],
    edgecolor='black'
)

for bar in bars:
    height = bar.get_height()
    plt.text(
        bar.get_x() + bar.get_width()/2,
        height + 0.3,
        f'+{height:.1f}%',
        ha='center',
        fontsize=10
    )

plt.ylabel('WER Increase (%)', fontsize=13, fontweight='bold')
plt.title('Noise Robustness Degradation', fontsize=15, fontweight='bold')
plt.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig('results/charts/degradation.png', dpi=300)
plt.close()

print("✅ Created: degradation.png")

# ============================================================
# Chart 5: Combined Overview
# ============================================================

avg_wer = []
avg_locality = []

for model in models:
    model_data = results_df[results_df['Model'] == model]

    avg_wer.append(model_data['WER (%)'].mean())
    avg_locality.append(model_data['Locality Extraction Accuracy (%)'].mean())

fig, axes = plt.subplots(1, 3, figsize=(18, 6))

# WER
axes[0].bar(
    models,
    avg_wer,
    color=[colors[m] for m in models],
    edgecolor='black'
)

axes[0].set_title('Average Normalized Approximate WER', fontweight='bold')
axes[0].set_ylabel('WER (%)')
axes[0].tick_params(axis='x', rotation=15)
axes[0].grid(axis='y', alpha=0.3)

# Locality
axes[1].bar(
    models,
    avg_locality,
    color=[colors[m] for m in models],
    edgecolor='black'
)

axes[1].set_title('Average Locality Extraction Accuracy', fontweight='bold')
axes[1].set_ylabel('Accuracy (%)')
axes[1].tick_params(axis='x', rotation=15)
axes[1].grid(axis='y', alpha=0.3)

# Latency
axes[2].bar(
    models,
    avg_latency,
    color=[colors[m] for m in models],
    edgecolor='black'
)

axes[2].set_title('Average Latency', fontweight='bold')
axes[2].set_ylabel('Latency (s)')
axes[2].tick_params(axis='x', rotation=15)
axes[2].grid(axis='y', alpha=0.3)

plt.suptitle(
    'ASR Benchmark Overview',
    fontsize=18,
    fontweight='bold'
)

plt.tight_layout()

plt.savefig('results/charts/combined_overview.png', dpi=300)

plt.close()

print("✅ Created: combined_overview.png")

# ============================================================
# Finished
# ============================================================

print("\n" + "=" * 60)
print("🎉 ALL UPDATED CHARTS GENERATED!")
print("=" * 60)

print("\nGenerated charts:")
print("1. wer_by_condition.png")
print("2. locality_by_condition.png")
print("3. latency_comparison.png")
print("4. degradation.png")
print("5. combined_overview.png")