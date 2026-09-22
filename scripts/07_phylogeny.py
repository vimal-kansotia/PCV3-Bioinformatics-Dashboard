import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from Bio import SeqIO, Phylo
from Bio.Phylo.BaseTree import BranchColor

# Publication plot settings
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.size'] = 10

aligned_fasta = '/Users/vimalkansotia/Downloads/Bioinformatics/data/processed/aligned_sequences_unique_ids.fasta'
master_path = '/Users/vimalkansotia/Downloads/Bioinformatics/data/processed/master_metadata.csv'
tree_dir = '/Users/vimalkansotia/Downloads/Bioinformatics/results/trees'
fig_dir = '/Users/vimalkansotia/Downloads/Bioinformatics/results/figures'

print("="*60)
print("PHASE 11, 12, 13 — PHYLOGENETICS & GENETIC DISTANCE VISUALIZATION")
print("="*60)

tree_file = os.path.join(tree_dir, 'pcv3_iqtree.treefile')
log_file = os.path.join(tree_dir, 'pcv3_iqtree.log')

if not os.path.exists(tree_file):
    print("Tree file not found yet. Please wait for IQ-TREE task to complete.")
    exit(1)

selected_model = "GTR+F+I+G4"
if os.path.exists(log_file):
    with open(log_file, 'r') as f:
        for line in f:
            if "Best-fit model according to" in line or "Best-fit model:" in line:
                parts = line.strip().split()
                if len(parts) > 0 and parts[-1] not in ['BIC', 'AIC', 'AICc']:
                    selected_model = parts[-1]

print(f"IQ-TREE Phylogenetic Tree Loaded!")
print(f"Selected Substitution Model (ModelFinder): {selected_model}")
print(f"Tree File Path: {tree_file}")

# Load Master Metadata for Tree Annotation
df_master = pd.read_csv(master_path)
meta_lookup = {}
for _, row in df_master.iterrows():
    meta_lookup[row['seq_id']] = row

# Read Newick Tree
tree = Phylo.read(tree_file, "newick")

# Colors for Country & Year Annotation
top_countries = df_master['country'].value_counts().head(8).index
palette_country = sns.color_palette("tab10", len(top_countries) + 1)
country_color_map = {}
for i, c in enumerate(top_countries):
    r, g, b = palette_country[i]
    country_color_map[c] = BranchColor(int(r*255), int(g*255), int(b*255))
country_color_map['Other'] = BranchColor(128, 128, 128)

# Color terminal branches by country
for leaf in tree.get_terminals():
    clean_name = leaf.name.split('_dup')[0] if leaf.name else ''
    info = meta_lookup.get(clean_name, {})
    cntry = info.get('country', 'Other')
    leaf.color = country_color_map.get(cntry, country_color_map['Other'])

# Plot Figure 14: Phylogenetic Tree Colored by Country
fig = plt.figure(figsize=(12, 10))
ax = fig.add_subplot(1, 1, 1)
Phylo.draw(tree, do_show=False, axes=ax, show_confidence=False, label_func=lambda x: '')
plt.title(f'Figure 14: Maximum Likelihood Phylogenetic Tree of PCV3 Genomes\n(IQ-TREE 3 ModelFinder: {selected_model}, Bootstrap: 1000 UFBoot Replicates)', fontsize=13, fontweight='bold', pad=15)
plt.xlabel('Substitution Rate (substitutions per site)', fontsize=11)
plt.ylabel('Phylogenetic Taxa', fontsize=11)

# Add Legend for Countries
legend_elements = [plt.Line2D([0], [0], color=(c.red/255, c.green/255, c.blue/255), lw=4, label=cnt) for cnt, c in country_color_map.items()]
plt.legend(handles=legend_elements, loc='upper left', bbox_to_anchor=(1.02, 1), title='Country / Region', frameon=True)
plt.tight_layout()
plt.savefig(os.path.join(fig_dir, 'fig14_phylo_tree_country.png'), dpi=300)
plt.close()

# Plot Figure 15: Phylogenetic Tree Colored by Year
min_year = df_master['year'].min()
max_year = df_master['year'].max()
cmap_year = plt.cm.viridis

for leaf in tree.get_terminals():
    clean_name = leaf.name.split('_dup')[0] if leaf.name else ''
    info = meta_lookup.get(clean_name, {})
    yr = info.get('year', min_year)
    norm_yr = (yr - min_year) / (max_year - min_year) if max_year > min_year else 0.5
    r, g, b, _ = cmap_year(norm_yr)
    leaf.color = BranchColor(int(r*255), int(g*255), int(b*255))

fig = plt.figure(figsize=(12, 10))
ax = fig.add_subplot(1, 1, 1)
Phylo.draw(tree, do_show=False, axes=ax, show_confidence=False, label_func=lambda x: '')
plt.title(f'Figure 15: Maximum Likelihood Phylogenetic Tree Annotated by Collection Year ({int(min_year)} - {int(max_year)})', fontsize=13, fontweight='bold', pad=15)
plt.xlabel('Substitution Rate (substitutions per site)', fontsize=11)
plt.ylabel('Phylogenetic Taxa', fontsize=11)

sm = plt.cm.ScalarMappable(cmap=cmap_year, norm=plt.Normalize(vmin=min_year, vmax=max_year))
sm.set_array([])
cbar = plt.colorbar(sm, ax=ax, orientation='vertical', pad=0.02)
cbar.set_label('Collection Year', fontsize=11)

plt.tight_layout()
plt.savefig(os.path.join(fig_dir, 'fig15_phylo_tree_year.png'), dpi=300)
plt.close()

# 3. Pairwise Genetic Distance Calculation & Heatmap (Figure 16)
records = list(SeqIO.parse(aligned_fasta, "fasta"))
align_matrix = np.array([list(str(r.seq).upper()) for r in records])
n_seqs, align_len = align_matrix.shape

# Subsample 100 representative sequences for clear, legible distance heatmap
np.random.seed(42)
sub_indices = np.sort(np.random.choice(n_seqs, 100, replace=False))
sub_matrix = align_matrix[sub_indices, :]

p_dist_matrix = np.zeros((100, 100))
for i in range(100):
    for j in range(i+1, 100):
        valid_mask = (sub_matrix[i, :] != '-') & (sub_matrix[j, :] != '-')
        diffs = np.sum(sub_matrix[i, valid_mask] != sub_matrix[j, valid_mask])
        dist = diffs / np.sum(valid_mask) if np.sum(valid_mask) > 0 else 0
        p_dist_matrix[i, j] = dist
        p_dist_matrix[j, i] = dist

plt.figure(figsize=(10, 8))
sns.heatmap(p_dist_matrix, cmap="YlOrRd", cbar_kws={'label': 'Pairwise p-Distance (substitutions / site)'})
plt.title('Figure 16: Pairwise Genetic Distance Heatmap (Subsampled N=100 Representative PCV3 Genomes)', fontsize=13, fontweight='bold', pad=15)
plt.xlabel('Sequence Index', fontsize=11)
plt.ylabel('Sequence Index', fontsize=11)
plt.tight_layout()
plt.savefig(os.path.join(fig_dir, 'fig16_genetic_distance_heatmap.png'), dpi=300)
plt.close()

mean_dist = np.mean(p_dist_matrix[p_dist_matrix > 0])
max_dist = np.max(p_dist_matrix)
print(f"Mean Pairwise Genetic Distance: {mean_dist:.4f} ({mean_dist*100:.2f}% divergence)")
print(f"Max Pairwise Genetic Distance: {max_dist:.4f} ({max_dist*100:.2f}% divergence)")
print("Figures 14, 15, and 16 generated successfully.")
