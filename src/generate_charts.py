import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os

# Create output directory
os.makedirs('results/charts', exist_ok=True)

# Set style
plt.style.use('seaborn-v0_8-darkgrid')
colors = {
    'Deepgram': '#2ecc71',      # Green (winner)
    'Google Cloud': '#3498db',   # Blue
    'Whisper Small': '#e67e22',  # Orange
    'Whisper Base': '#e74c3c'    # Red (worst)
}

# ============================================================
# Chart 1: WER Comparison (Bar Chart)
# ============================================================
models = ['Deepgram', 'Google Cloud', 'Whisper Small', 'Whisper Base']
wer = [86.88, 93.26, 95.41, 99.72]

plt.figure(figsize=(10, 6))
bars = plt.bar(models, wer, color=[colors[m] for m in models], edgecolor='black', linewidth=1.5)

# Add value labels on bars
for i, (bar, value) in enumerate(zip(bars, wer)):
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1, 
             f'{value}%', ha='center', va='bottom', fontsize=12, fontweight='bold')

plt.ylabel('Word Error Rate (%)', fontsize=14, fontweight='bold')
plt.title('Word Error Rate Comparison\n(Lower is Better)', fontsize=16, fontweight='bold')
plt.ylim(0, 105)
plt.xticks(rotation=15, ha='right', fontsize=12)
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig('results/charts/wer_comparison.png', dpi=300, bbox_inches='tight')
plt.close()
print("✅ Created: results/charts/wer_comparison.png")

# ============================================================
# Chart 2: Locality Accuracy Comparison (Bar Chart)
# ============================================================
locality_acc = [21.67, 11.67, 6.67, 1.67]

plt.figure(figsize=(10, 6))
bars = plt.bar(models, locality_acc, color=[colors[m] for m in models], edgecolor='black', linewidth=1.5)

# Add value labels on bars
for i, (bar, value) in enumerate(zip(bars, locality_acc)):
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5, 
             f'{value}%', ha='center', va='bottom', fontsize=12, fontweight='bold')

plt.ylabel('Locality Extraction Accuracy (%)', fontsize=14, fontweight='bold')
plt.title('Locality Extraction Accuracy\n(Higher is Better)', fontsize=16, fontweight='bold')
plt.ylim(0, 25)
plt.xticks(rotation=15, ha='right', fontsize=12)
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig('results/charts/locality_accuracy.png', dpi=300, bbox_inches='tight')
plt.close()
print("✅ Created: results/charts/locality_accuracy.png")

# ============================================================
# Chart 3: Latency Comparison (Bar Chart)
# ============================================================
latency = [3.34, 1.41, 6.14, 7.34]

plt.figure(figsize=(10, 6))
bars = plt.bar(models, latency, color=[colors[m] for m in models], edgecolor='black', linewidth=1.5)

# Add value labels on bars
for i, (bar, value) in enumerate(zip(bars, latency)):
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.2, 
             f'{value}s', ha='center', va='bottom', fontsize=12, fontweight='bold')

plt.ylabel('Average Latency (seconds)', fontsize=14, fontweight='bold')
plt.title('Processing Speed Comparison\n(Lower is Better)', fontsize=16, fontweight='bold')
plt.ylim(0, 8)
plt.xticks(rotation=15, ha='right', fontsize=12)
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig('results/charts/latency_comparison.png', dpi=300, bbox_inches='tight')
plt.close()
print("✅ Created: results/charts/latency_comparison.png")

# ============================================================
# Chart 4: Noise Impact (Grouped Bar Chart)
# ============================================================
normal_wer = [78.74, 87.95, 90.95, 95.95]
noisy_wer = [86.88, 93.26, 95.41, 99.72]

x = np.arange(len(models))
width = 0.35

fig, ax = plt.subplots(figsize=(12, 6))
bars1 = ax.bar(x - width/2, normal_wer, width, label='Normal (Quiet)', 
               color='#95a5a6', edgecolor='black', linewidth=1.5)
bars2 = ax.bar(x + width/2, noisy_wer, width, label='Noisy (Metro)', 
               color='#34495e', edgecolor='black', linewidth=1.5)

# Add value labels
for bars in [bars1, bars2]:
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'{height:.1f}%', ha='center', va='bottom', fontsize=10, fontweight='bold')

ax.set_ylabel('Word Error Rate (%)', fontsize=14, fontweight='bold')
ax.set_title('Noise Impact on WER\n(Normal vs Metro Noise)', fontsize=16, fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(models, rotation=15, ha='right', fontsize=12)
ax.legend(fontsize=12, loc='upper left')
ax.set_ylim(0, 105)
ax.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig('results/charts/noise_impact.png', dpi=300, bbox_inches='tight')
plt.close()
print("✅ Created: results/charts/noise_impact.png")

# ============================================================
# Chart 5: Degradation Percentage (Bar Chart)
# ============================================================
degradation = [8.14, 5.31, 4.46, 3.77]

plt.figure(figsize=(10, 6))
bars = plt.bar(models, degradation, color=[colors[m] for m in models], edgecolor='black', linewidth=1.5)

# Add value labels on bars
for i, (bar, value) in enumerate(zip(bars, degradation)):
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.2, 
             f'+{value}%', ha='center', va='bottom', fontsize=12, fontweight='bold')

plt.ylabel('WER Degradation (%)', fontsize=14, fontweight='bold')
plt.title('WER Degradation from Normal to Noisy Conditions\n(Lower is Better)', 
          fontsize=16, fontweight='bold')
plt.ylim(0, 10)
plt.xticks(rotation=15, ha='right', fontsize=12)
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig('results/charts/degradation.png', dpi=300, bbox_inches='tight')
plt.close()
print("✅ Created: results/charts/degradation.png")

# ============================================================
# Chart 6: Overall Performance Radar/Spider Chart (BONUS!)
# ============================================================
from math import pi

categories = ['Accuracy\n(100-WER)', 'Locality\nExtraction', 'Speed\n(10-Latency)', 'Noise\nRobustness']
N = len(categories)

# Normalize metrics to 0-100 scale
def normalize(values, reverse=False):
    if reverse:
        return [100 - v for v in values]
    return values

# Prepare data (normalized to 0-100)
deepgram_scores = [100-86.88, 21.67, 10-3.34, 100-8.14]
google_scores = [100-93.26, 11.67, 10-1.41, 100-5.31]
whisper_small_scores = [100-95.41, 6.67, 10-6.14, 100-4.46]
whisper_base_scores = [100-99.72, 1.67, 10-7.34, 100-3.77]

# Angles for radar chart
angles = [n / float(N) * 2 * pi for n in range(N)]
angles += angles[:1]

# Close the plot
deepgram_scores += deepgram_scores[:1]
google_scores += google_scores[:1]
whisper_small_scores += whisper_small_scores[:1]
whisper_base_scores += whisper_base_scores[:1]

fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(projection='polar'))

ax.plot(angles, deepgram_scores, 'o-', linewidth=2, label='Deepgram', color=colors['Deepgram'])
ax.fill(angles, deepgram_scores, alpha=0.25, color=colors['Deepgram'])

ax.plot(angles, google_scores, 'o-', linewidth=2, label='Google Cloud', color=colors['Google Cloud'])
ax.fill(angles, google_scores, alpha=0.25, color=colors['Google Cloud'])

ax.set_xticks(angles[:-1])
ax.set_xticklabels(categories, size=12, fontweight='bold')
ax.set_ylim(0, 100)
ax.set_title('Overall Performance Comparison\n(Larger area = Better)', 
             size=16, fontweight='bold', pad=20)
ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1), fontsize=12)
ax.grid(True)

plt.tight_layout()
plt.savefig('results/charts/overall_performance_radar.png', dpi=300, bbox_inches='tight')
plt.close()
print("✅ Created: results/charts/overall_performance_radar.png")

# ============================================================
# Chart 7: Combined Overview (3 Metrics in 1)
# ============================================================
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18, 6))

# WER
ax1.bar(models, wer, color=[colors[m] for m in models], edgecolor='black', linewidth=1.5)
ax1.set_ylabel('WER (%)', fontsize=12, fontweight='bold')
ax1.set_title('Word Error Rate', fontsize=14, fontweight='bold')
ax1.set_ylim(0, 105)
ax1.tick_params(axis='x', rotation=45)
ax1.grid(axis='y', alpha=0.3)

# Locality Accuracy
ax2.bar(models, locality_acc, color=[colors[m] for m in models], edgecolor='black', linewidth=1.5)
ax2.set_ylabel('Accuracy (%)', fontsize=12, fontweight='bold')
ax2.set_title('Locality Extraction', fontsize=14, fontweight='bold')
ax2.set_ylim(0, 25)
ax2.tick_params(axis='x', rotation=45)
ax2.grid(axis='y', alpha=0.3)

# Latency
ax3.bar(models, latency, color=[colors[m] for m in models], edgecolor='black', linewidth=1.5)
ax3.set_ylabel('Latency (s)', fontsize=12, fontweight='bold')
ax3.set_title('Processing Speed', fontsize=14, fontweight='bold')
ax3.set_ylim(0, 8)
ax3.tick_params(axis='x', rotation=45)
ax3.grid(axis='y', alpha=0.3)

plt.suptitle('ASR Benchmark - Complete Overview', fontsize=18, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig('results/charts/combined_overview.png', dpi=300, bbox_inches='tight')
plt.close()
print("✅ Created: results/charts/combined_overview.png")

print("\n" + "="*60)
print("🎉 ALL CHARTS GENERATED SUCCESSFULLY!")
print("="*60)
print("\nGenerated charts:")
print("  1. wer_comparison.png")
print("  2. locality_accuracy.png")
print("  3. latency_comparison.png")
print("  4. noise_impact.png")
print("  5. degradation.png")
print("  6. overall_performance_radar.png")
print("  7. combined_overview.png")
print("\n📁 All saved in: results/charts/")