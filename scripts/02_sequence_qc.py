import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Set publication style
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.size'] = 11

master_path = '/Users/vimalkansotia/Downloads/Bioinformatics/data/processed/master_metadata.csv'
fig_dir = '/Users/vimalkansotia/Downloads/Bioinformatics/results/figures'
table_dir = '/Users/vimalkansotia/Downloads/Bioinformatics/results/tables'

df = pd.read_csv(master_path)

print("="*60)
print("PHASE 3 — SEQUENCE QUALITY CONTROL & METADATA SUMMARY")
print("="*60)

# 1. Figure 01: Sequence Length Distribution
plt.figure(figsize=(8, 5))
sns.histplot(df['sequence_length'], bins=15, color='#2b5c8f', kde=True)
plt.title('Figure 1: Distribution of PCV3 Sequence Lengths (N=500)', fontsize=14, fontweight='bold', pad=15)
plt.xlabel('Sequence Length (bp)', fontsize=12)
plt.ylabel('Frequency', fontsize=12)
plt.axvline(df['sequence_length'].mean(), color='#e74c3c', linestyle='--', linewidth=2, label=f"Mean: {df['sequence_length'].mean():.2f} bp")
plt.axvline(df['sequence_length'].median(), color='#2ecc71', linestyle=':', linewidth=2, label=f"Median: {df['sequence_length'].median():.1f} bp")
plt.legend(frameon=True, facecolor='white', framealpha=0.9)
plt.tight_layout()
plt.savefig(os.path.join(fig_dir, 'fig01_sequence_length_distribution.png'), dpi=300)
plt.close()

# 2. Figure 02: GC Content Distribution
plt.figure(figsize=(8, 5))
sns.histplot(df['gc_content'], bins=20, color='#27ae60', kde=True)
plt.title('Figure 2: Distribution of PCV3 Genome GC Content (%)', fontsize=14, fontweight='bold', pad=15)
plt.xlabel('GC Content (%)', fontsize=12)
plt.ylabel('Frequency', fontsize=12)
plt.axvline(df['gc_content'].mean(), color='#e74c3c', linestyle='--', linewidth=2, label=f"Mean: {df['gc_content'].mean():.2f}%")
plt.legend(frameon=True, facecolor='white', framealpha=0.9)
plt.tight_layout()
plt.savefig(os.path.join(fig_dir, 'fig02_gc_content_distribution.png'), dpi=300)
plt.close()

# 3. Figure 03: Samples by Country
plt.figure(figsize=(10, 6))
country_counts = df['country'].value_counts()
sns.barplot(x=country_counts.values, y=country_counts.index, palette='viridis')
plt.title('Figure 3: Geographic Distribution of PCV3 Sequences by Country (N=500)', fontsize=14, fontweight='bold', pad=15)
plt.xlabel('Number of Sequences', fontsize=12)
plt.ylabel('Country / Region', fontsize=12)
for i, v in enumerate(country_counts.values):
    plt.text(v + 1, i, str(v), va='center', fontsize=10, fontweight='bold')
plt.xlim(0, max(country_counts.values) + 10)
plt.tight_layout()
plt.savefig(os.path.join(fig_dir, 'fig03_samples_by_country.png'), dpi=300)
plt.close()

# 4. Figure 04: Samples by Year
plt.figure(figsize=(10, 5))
year_counts = df['year'].astype(int).value_counts().sort_index()
sns.barplot(x=year_counts.index, y=year_counts.values, color='#3498db')
plt.title('Figure 4: Temporal Distribution of PCV3 Sequences by Collection Year', fontsize=14, fontweight='bold', pad=15)
plt.xlabel('Collection Year', fontsize=12)
plt.ylabel('Number of Sequences', fontsize=12)
plt.xticks(rotation=45)
for i, v in enumerate(year_counts.values):
    plt.text(i, v + 1, str(v), ha='center', fontsize=9, fontweight='bold')
plt.ylim(0, max(year_counts.values) + 15)
plt.tight_layout()
plt.savefig(os.path.join(fig_dir, 'fig04_samples_by_year.png'), dpi=300)
plt.close()

# Save QC summary table
qc_summary = pd.DataFrame([{
    'Total Sequences': len(df),
    'Min Length (bp)': df['sequence_length'].min(),
    'Max Length (bp)': df['sequence_length'].max(),
    'Mean Length (bp)': round(df['sequence_length'].mean(), 2),
    'Median Length (bp)': round(df['sequence_length'].median(), 1),
    'Mean GC (%)': round(df['gc_content'].mean(), 2),
    'Min GC (%)': round(df['gc_content'].min(), 2),
    'Max GC (%)': round(df['gc_content'].max(), 2),
    'Sequences with Ambiguous Bases': (df['ambiguous_bases'] > 0).sum(),
    'Total Ambiguous Bases': df['ambiguous_bases'].sum(),
    'Unique Countries': df['country'].nunique(),
    'Collection Year Range': f"{int(df['year'].min())} - {int(df['year'].max())}"
}])

qc_summary.to_csv(os.path.join(table_dir, 'table00_qc_summary.csv'), index=False)
print("QC figures (01-04) and table00_qc_summary.csv generated successfully.")
