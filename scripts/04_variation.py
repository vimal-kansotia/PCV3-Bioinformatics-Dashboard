import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from Bio import SeqIO
from collections import Counter
import os
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

aligned_fasta = BASE_DIR
fig_dir = BASE_DIR
table_dir = BASE_DIR

print("="*60)
print("PHASE 5 — GENOME VARIATION / SNP ANALYSIS")
print("="*60)

records = list(SeqIO.parse(aligned_fasta, "fasta"))
seq_ids = [r.id for r in records]
align_matrix = np.array([list(str(r.seq).upper()) for r in records])

seq_count, align_len = align_matrix.shape

snp_records = []
snp_positions = []
site_type_counts = {'Conserved': 0, 'Variable (Singleton)': 0, 'Parsimony-Informative': 0}

snp_density_window = 50
window_bins = range(0, align_len, snp_density_window)
window_snp_counts = [0] * len(window_bins)

for pos in range(align_len):
    col = align_matrix[:, pos]
    # Filter non-standard/gaps for frequency calculation
    valid = [c for c in col if c in "ATCG"]
    counts = Counter(valid)
    gap_count = sum(1 for c in col if c == '-')
    
    if len(counts) <= 1:
        site_type_counts['Conserved'] += 1
    else:
        snp_positions.append(pos + 1)
        win_idx = pos // snp_density_window
        if win_idx < len(window_snp_counts):
            window_snp_counts[win_idx] += 1
            
        states_gt1 = sum(1 for state, cnt in counts.items() if cnt >= 2)
        if states_gt1 >= 2:
            site_type_counts['Parsimony-Informative'] += 1
        else:
            site_type_counts['Variable (Singleton)'] += 1
            
        most_common = counts.most_common()
        ref_base = most_common[0][0] if len(most_common) > 0 else 'N'
        alt_bases = [f"{base}:{cnt}" for base, cnt in most_common[1:]]
        maf = (sum(counts.values()) - most_common[0][1]) / len(valid) if len(valid) > 0 else 0
        
        snp_records.append({
            'alignment_position': pos + 1,
            'ref_allele': ref_base,
            'ref_count': most_common[0][1] if len(most_common) > 0 else 0,
            'alt_alleles': ", ".join(alt_bases),
            'minor_allele_freq': round(maf, 4),
            'gap_count': gap_count,
            'is_parsimony_informative': (states_gt1 >= 2)
        })

df_snp = pd.DataFrame(snp_records)
df_snp.to_csv(os.path.join(table_dir, 'table01_snp_positions_summary.csv'), index=False)
print(f"SNP Summary Table saved with {len(df_snp)} variable positions.")

# 1. Figure 05: MSA Site Type Composition Bar Chart
plt.figure(figsize=(8, 5))
types = list(site_type_counts.keys())
values = list(site_type_counts.values())
colors = ['#2ecc71', '#f39c12', '#e74c3c']

bars = plt.bar(types, values, color=colors, edgecolor='black', width=0.5)
plt.title('Figure 5: Genomic Site Categorization across PCV3 Alignment (2,156 bp)', fontsize=14, fontweight='bold', pad=15)
plt.ylabel('Number of Alignment Positions', fontsize=12)
for bar in bars:
    yval = bar.get_height()
    pct = (yval / align_len) * 100
    plt.text(bar.get_x() + bar.get_width()/2, yval + 15, f"{yval}\n({pct:.1f}%)", ha='center', va='bottom', fontsize=10, fontweight='bold')

plt.ylim(0, max(values) + 150)
plt.tight_layout()
plt.savefig(os.path.join(fig_dir, 'fig05_msa_summary.png'), dpi=300)
plt.close()

# 2. Figure 06: SNP Density Plot across Genome Coordinates
plt.figure(figsize=(10, 5))
plt.plot(window_bins, window_snp_counts, color='#8e44ad', linewidth=2, marker='o', markersize=4)
plt.fill_between(window_bins, window_snp_counts, color='#8e44ad', alpha=0.2)
plt.title('Figure 6: Genome-wide SNP Variant Density (50 bp Sliding Window)', fontsize=14, fontweight='bold', pad=15)
plt.xlabel('Genomic Alignment Position (bp)', fontsize=12)
plt.ylabel('Number of Variable Sites / 50 bp', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
plt.savefig(os.path.join(fig_dir, 'fig06_variable_sites_snp_density.png'), dpi=300)
plt.close()

print("Figures 05 & 06 generated successfully.")
