import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import os
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Publication plot settings
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.size'] = 11

snp_matrix_path = BASE_DIR
master_path = BASE_DIR
fig_dir = BASE_DIR
table_dir = BASE_DIR

print("="*60)
print("PHASE 7 & 8 — PCA & K-MEANS UNSUPERVISED CLUSTERING")
print("="*60)

# Load data
df_snp = pd.read_csv(snp_matrix_path, index_col=0)
df_master = pd.read_csv(master_path)

# Filter out constant/near-constant columns to focus on informative genome variants
stds = df_snp.std(axis=0)
informative_mask = stds > 0.05
df_snp_filtered = df_snp.loc[:, informative_mask]

print(f"Original SNP features: {df_snp.shape[1]}")
print(f"Informative SNP features retained (std > 0.05): {df_snp_filtered.shape[1]}")

# Mean-centering preprocessing (Preserves binary distance metric without zero-std scaling distortion)
X = df_snp_filtered.values - np.mean(df_snp_filtered.values, axis=0)

# 1. PCA Calculation
pca = PCA(n_components=20, random_state=42)
X_pca = pca.fit_transform(X)
var_ratio = pca.explained_variance_ratio_
cum_var = np.cumsum(var_ratio)

pc1_var = var_ratio[0] * 100
pc2_var = var_ratio[1] * 100
print(f"\nPCA Computed on {df_snp_filtered.shape[1]} informative SNP features across {df_snp_filtered.shape[0]} sequences.")
print(f"PC1 Variance: {pc1_var:.2f}%")
print(f"PC2 Variance: {pc2_var:.2f}%")
print(f"Cumulative Variance (PC1 + PC2): {pc1_var + pc2_var:.2f}%")

# Plot Figure 07: Explained Variance
plt.figure(figsize=(8, 5))
plt.plot(range(1, 21), var_ratio[:20] * 100, marker='o', color='#2980b9', linewidth=2, label='Individual PC Variance (%)')
plt.step(range(1, 21), cum_var[:20] * 100, where='mid', color='#e74c3c', linewidth=2, label='Cumulative Variance (%)')
plt.title('Figure 7: PCA Explained Variance Ratio (Informative SNP Features)', fontsize=14, fontweight='bold', pad=15)
plt.xlabel('Principal Component', fontsize=12)
plt.ylabel('Percentage of Variance Explained (%)', fontsize=12)
plt.xticks(range(1, 21))
plt.legend(frameon=True, facecolor='white')
plt.tight_layout()
plt.savefig(os.path.join(fig_dir, 'fig07_pca_explained_variance.png'), dpi=300)
plt.close()

# Prepare plotting dataframe with metadata post-hoc
df_plot = df_master.copy()
df_plot['PC1'] = X_pca[:, 0]
df_plot['PC2'] = X_pca[:, 1]

# Top 8 countries for clear coloring
top_countries = df_plot['country'].value_counts().head(8).index
df_plot['country_plot'] = df_plot['country'].apply(lambda c: c if c in top_countries else 'Other')

# Plot Figure 08: PCA Colored by Country
plt.figure(figsize=(9, 7))
sns.scatterplot(data=df_plot, x='PC1', y='PC2', hue='country_plot', style='country_plot', s=70, alpha=0.85, palette='tab10')
plt.title(f'Figure 8: PCA Scatter Plot Annotated by Country (PC1: {pc1_var:.1f}%, PC2: {pc2_var:.1f}%)', fontsize=14, fontweight='bold', pad=15)
plt.xlabel(f'PC1 ({pc1_var:.1f}% Variance)', fontsize=12)
plt.ylabel(f'PC2 ({pc2_var:.1f}% Variance)', fontsize=12)
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', frameon=True)
plt.tight_layout()
plt.savefig(os.path.join(fig_dir, 'fig08_pca_country.png'), dpi=300)
plt.close()

# Plot Figure 09: PCA Colored by Year
plt.figure(figsize=(9, 7))
sns.scatterplot(data=df_plot, x='PC1', y='PC2', hue='year', palette='viridis', s=70, alpha=0.85)
plt.title(f'Figure 9: PCA Scatter Plot Annotated by Collection Year (PC1: {pc1_var:.1f}%, PC2: {pc2_var:.1f}%)', fontsize=14, fontweight='bold', pad=15)
plt.xlabel(f'PC1 ({pc1_var:.1f}% Variance)', fontsize=12)
plt.ylabel(f'PC2 ({pc2_var:.1f}% Variance)', fontsize=12)
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', title='Year', frameon=True)
plt.tight_layout()
plt.savefig(os.path.join(fig_dir, 'fig09_pca_year.png'), dpi=300)
plt.close()

# 2. K-Means Clustering & Silhouette Evaluation
k_range = range(2, 11)
silhouette_scores = []
X_cluster_input = X_pca[:, :5]

print("\n--- K-Means Silhouette Score Evaluation (k=2..10) ---")
for k in k_range:
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=20)
    labels = kmeans.fit_predict(X_cluster_input)
    score = silhouette_score(X_cluster_input, labels)
    silhouette_scores.append(score)
    print(f"  k = {k} | Silhouette Score: {score:.4f}")

# Select optimal k based on silhouette evaluation
optimal_k = k_range[np.argmax(silhouette_scores)]
best_score = max(silhouette_scores)
print(f"\nSelected Clustering Configuration based on Silhouette Criterion: k = {optimal_k} (Score: {best_score:.4f})")

# Plot Figure 10: Silhouette Scores vs k
plt.figure(figsize=(8, 5))
plt.plot(k_range, silhouette_scores, marker='s', color='#27ae60', linewidth=2, markersize=8)
plt.axvline(optimal_k, color='#e74c3c', linestyle='--', label=f"Selected k = {optimal_k} (Score: {best_score:.4f})")
plt.title('Figure 10: K-Means Silhouette Score vs Number of Clusters (k=2..10)', fontsize=14, fontweight='bold', pad=15)
plt.xlabel('Number of Clusters (k)', fontsize=12)
plt.ylabel('Mean Silhouette Coefficient', fontsize=12)
plt.xticks(k_range)
plt.legend(frameon=True, facecolor='white')
plt.tight_layout()
plt.savefig(os.path.join(fig_dir, 'fig10_silhouette_scores.png'), dpi=300)
plt.close()

# Fit optimal K-Means model
kmeans_opt = KMeans(n_clusters=optimal_k, random_state=42, n_init=20)
cluster_labels = kmeans_opt.fit_predict(X_cluster_input)
df_plot['cluster'] = [f"Cluster {l+1}" for l in cluster_labels]
df_master['cluster'] = df_plot['cluster']
df_master.to_csv(master_path, index=False)

# Plot Figure 11: PCA Colored by Cluster
plt.figure(figsize=(9, 7))
sns.scatterplot(data=df_plot, x='PC1', y='PC2', hue='cluster', style='cluster', s=80, alpha=0.9, palette='Set1')
plt.title(f'Figure 11: PCA Ordination Colored by K-Means Clusters (k={optimal_k})', fontsize=14, fontweight='bold', pad=15)
plt.xlabel(f'PC1 ({pc1_var:.1f}% Variance)', fontsize=12)
plt.ylabel(f'PC2 ({pc2_var:.1f}% Variance)', fontsize=12)
plt.legend(frameon=True, facecolor='white', loc='best')
plt.tight_layout()
plt.savefig(os.path.join(fig_dir, 'fig11_pca_clusters.png'), dpi=300)
plt.close()

# Save Cluster Assignments Table
df_cluster_table = df_plot[['seq_id', 'accession', 'country', 'year', 'cluster', 'PC1', 'PC2']]
df_cluster_table.to_csv(os.path.join(table_dir, 'table02_cluster_assignments.csv'), index=False)
print(f"Cluster assignments saved to {table_dir}/table02_cluster_assignments.csv")
print("\nCluster Size Breakdown:")
print(df_plot['cluster'].value_counts())
