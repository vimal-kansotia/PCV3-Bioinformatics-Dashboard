import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import chi2_contingency
import os

# Publication plot settings
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.size'] = 11

master_path = '/Users/vimalkansotia/Downloads/Bioinformatics/data/processed/master_metadata.csv'
fig_dir = '/Users/vimalkansotia/Downloads/Bioinformatics/results/figures'
table_dir = '/Users/vimalkansotia/Downloads/Bioinformatics/results/tables'

print("="*60)
print("PHASE 9 & 10 — GEOGRAPHICAL & TEMPORAL STATISTICAL ASSOCIATION")
print("="*60)

df = pd.read_csv(master_path)

# Helper function for Cramér's V
def cramers_v(contingency_table):
    chi2 = chi2_contingency(contingency_table)[0]
    n = contingency_table.values.sum()
    r, k = contingency_table.shape
    return np.sqrt(chi2 / (n * (min(r, k) - 1)))

# Label Permutation Monte Carlo Chi-square test
def label_permutation_chi2(labels_x, labels_y, permutations=5000):
    ct_obs = pd.crosstab(labels_x, labels_y)
    obs_chi2, _, _, _ = chi2_contingency(ct_obs)
    
    sim_chi2 = []
    np.random.seed(42)
    labels_y_perm = labels_y.copy()
    
    for _ in range(permutations):
        np.random.shuffle(labels_y_perm)
        ct_sim = pd.crosstab(labels_x, labels_y_perm)
        chi2_val, _, _, _ = chi2_contingency(ct_sim)
        sim_chi2.append(chi2_val)
        
    p_val_mc = (np.sum(np.array(sim_chi2) >= obs_chi2) + 1) / (permutations + 1)
    return obs_chi2, p_val_mc

# 1. Geographical Association Analysis
print("\n--- 1. GEOGRAPHICAL ASSOCIATION ANALYSIS ---")
top_countries = df['country'].value_counts().head(8).index
df['country_grouped'] = df['country'].apply(lambda c: c if c in top_countries else 'Other')

ct_country = pd.crosstab(df['cluster'], df['country_grouped'])
ct_country.to_csv(os.path.join(table_dir, 'table03_cluster_country_contingency.csv'))

chi2_c, p_c, dof_c, exp_c = chi2_contingency(ct_country)
sparse_cells_c = np.sum(exp_c < 5)
total_cells_c = exp_c.size
pct_sparse_c = (sparse_cells_c / total_cells_c) * 100

_, p_mc_c = label_permutation_chi2(df['cluster'].values, df['country_grouped'].values, permutations=5000)
v_c = cramers_v(ct_country)

print(f"Cluster x Country Contingency Table Shape: {ct_country.shape}")
print(f"Chi-square Statistic: {chi2_c:.2f} (dof = {dof_c})")
print(f"Asymptotic p-value: {p_c:.4e}")
print(f"Permutation Simulated p-value (5,000 perms): {p_mc_c:.4f}")
print(f"Cramér's V: {v_c:.4f}")
print(f"Expected Cell Count Diagnostics: {sparse_cells_c} / {total_cells_c} cells ({pct_sparse_c:.1f}%) have expected count < 5.")

# Plot Figure 12: Cluster x Country Proportion Heatmap
plt.figure(figsize=(10, 6))
prop_country = ct_country.div(ct_country.sum(axis=0), axis=1) * 100
sns.heatmap(prop_country, annot=True, fmt=".1f", cmap="YlGnBu", cbar_kws={'label': 'Proportion within Country (%)'})
plt.title(f'Figure 12: Cluster Proportion Heatmap by Country (Cramér\'s V = {v_c:.3f}, p = {p_mc_c:.3f})', fontsize=14, fontweight='bold', pad=15)
plt.xlabel('Country / Region', fontsize=12)
plt.ylabel('PCV3 Cluster', fontsize=12)
plt.tight_layout()
plt.savefig(os.path.join(fig_dir, 'fig12_cluster_country_heatmap.png'), dpi=300)
plt.close()

# 2. Temporal (Year) Association Analysis
print("\n--- 2. TEMPORAL (YEAR) ASSOCIATION ANALYSIS ---")
def bin_year(y):
    if y < 2015:
        return 'Early (<2015)'
    elif 2015 <= y <= 2017:
        return 'Mid-Early (2015-2017)'
    elif 2018 <= y <= 2020:
        return 'Mid-Late (2018-2020)'
    else:
        return 'Late (2021-2025)'

df['year_bin'] = df['year'].apply(bin_year)
year_bin_order = ['Early (<2015)', 'Mid-Early (2015-2017)', 'Mid-Late (2018-2020)', 'Late (2021-2025)']

ct_year = pd.crosstab(df['cluster'], df['year_bin'])[year_bin_order]
ct_year.to_csv(os.path.join(table_dir, 'table04_cluster_year_contingency.csv'))

chi2_y, p_y, dof_y, exp_y = chi2_contingency(ct_year)
sparse_cells_y = np.sum(exp_y < 5)
total_cells_y = exp_y.size
pct_sparse_y = (sparse_cells_y / total_cells_y) * 100

_, p_mc_y = label_permutation_chi2(df['cluster'].values, df['year_bin'].values, permutations=5000)
v_y = cramers_v(ct_year)

print(f"Cluster x Year Bin Contingency Table Shape: {ct_year.shape}")
print(f"Chi-square Statistic: {chi2_y:.2f} (dof = {dof_y})")
print(f"Asymptotic p-value: {p_y:.4e}")
print(f"Permutation Simulated p-value (5,000 perms): {p_mc_y:.4f}")
print(f"Cramér's V: {v_y:.4f}")
print(f"Expected Cell Count Diagnostics: {sparse_cells_y} / {total_cells_y} cells ({pct_sparse_y:.1f}%) have expected count < 5.")

# Plot Figure 13: Cluster x Year Proportion Heatmap
plt.figure(figsize=(9, 6))
prop_year = ct_year.div(ct_year.sum(axis=0), axis=1) * 100
sns.heatmap(prop_year, annot=True, fmt=".1f", cmap="Purples", cbar_kws={'label': 'Proportion within Temporal Period (%)'})
plt.title(f'Figure 13: Cluster Proportion Heatmap by Temporal Period (Cramér\'s V = {v_y:.3f}, p = {p_mc_y:.3f})', fontsize=14, fontweight='bold', pad=15)
plt.xlabel('Temporal Period', fontsize=12)
plt.ylabel('PCV3 Cluster', fontsize=12)
plt.tight_layout()
plt.savefig(os.path.join(fig_dir, 'fig13_cluster_year_heatmap.png'), dpi=300)
plt.close()

print("Figures 12 & 13 and statistical tables 03 & 04 generated successfully.")
