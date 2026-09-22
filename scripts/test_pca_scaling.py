import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import matplotlib.pyplot as plt

df_snp = pd.read_csv('/Users/vimalkansotia/Downloads/Bioinformatics/data/processed/snp_feature_matrix.csv', index_col=0)

print(f"Original SNP matrix shape: {df_snp.shape}")

# Drop columns with zero variance or minor allele frequency < 0.01 (less than 5 samples)
stds = df_snp.std(axis=0)
df_filtered = df_snp.loc[:, stds > 0.05] # Keep features present in at least ~3-5 sequences
print(f"Filtered SNP matrix shape (std > 0.05): {df_filtered.shape}")

# Test PCA without scaling vs with centered PCA
X = df_filtered.values

pca = PCA(n_components=20)
X_pca = pca.fit_transform(X)

print("\nVariance ratio (Unscaled / Centered PCA):")
for idx, vr in enumerate(pca.explained_variance_ratio_[:10]):
    print(f"  PC{idx+1}: {vr*100:.2f}% (Cumulative: {sum(pca.explained_variance_ratio_[:idx+1])*100:.2f}%)")

print("\nEvaluating K-Means (k=2..10) on top 5 PCs:")
for k in range(2, 11):
    km = KMeans(n_clusters=k, random_state=42, n_init=20)
    labels = km.fit_predict(X_pca[:, :5])
    score = silhouette_score(X_pca[:, :5], labels)
    counts = pd.Series(labels).value_counts().to_dict()
    print(f"  k={k} | Silhouette: {score:.4f} | Cluster sizes: {counts}")
