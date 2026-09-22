import numpy as np
import pandas as pd
from Bio import SeqIO
from collections import Counter
import itertools
import os

aligned_fasta = '/Users/vimalkansotia/Downloads/Bioinformatics/data/processed/aligned_sequences.fasta'
raw_fasta = '/Users/vimalkansotia/Downloads/Bioinformatics/data/raw/viral_genome.fasta'
out_dir = '/Users/vimalkansotia/Downloads/Bioinformatics/data/processed'

print("="*60)
print("PHASE 6 — FEATURE EXTRACTION")
print("="*60)

records_aligned = list(SeqIO.parse(aligned_fasta, "fasta"))
seq_ids = [r.id for r in records_aligned]
align_matrix = np.array([list(str(r.seq).upper()) for r in records_aligned])

seq_count, align_len = align_matrix.shape

# 1. Primary Feature Matrix: One-Hot Encoded Variable Sites (SNPs)
variable_indices = []
for j in range(align_len):
    col = align_matrix[:, j]
    valid = [c for c in col if c in "ATCG"]
    if len(Counter(valid)) > 1:
        variable_indices.append(j)

print(f"Total variable positions identified: {len(variable_indices)}")

# Filter matrix to variable sites only
snp_submatrix = align_matrix[:, variable_indices]

# One-hot encoding of nucleotide states at variable sites (A, C, G, T, -)
nucleotides = ['A', 'C', 'G', 'T', '-']
encoded_blocks = []
feature_names = []

for idx, col_idx in enumerate(variable_indices):
    col_vals = snp_submatrix[:, idx]
    for nt in ['A', 'C', 'G', 'T']: # Excluding gaps to avoid redundancy or including if informative
        binary_col = (col_vals == nt).astype(int)
        # Only keep feature column if it has variation across sample
        if binary_col.std() > 0:
            encoded_blocks.append(binary_col)
            feature_names.append(f"Pos_{col_idx+1}_{nt}")

snp_feature_matrix = np.column_stack(encoded_blocks)
df_snp_features = pd.DataFrame(snp_feature_matrix, index=seq_ids, columns=feature_names)
snp_csv_path = os.path.join(out_dir, 'snp_feature_matrix.csv')
df_snp_features.to_csv(snp_csv_path)

print(f"Primary SNP Feature Matrix created: {df_snp_features.shape[0]} sequences x {df_snp_features.shape[1]} binary SNP features")
print(f"Saved to: {snp_csv_path}")

# 2. Supplementary Feature Matrix: k=4 K-mer Frequencies
k = 4
bases = ['A', 'C', 'G', 'T']
kmers = ["".join(p) for p in itertools.product(bases, repeat=k)]
kmer_to_idx = {km: i for i, km in enumerate(kmers)}

records_raw = list(SeqIO.parse(raw_fasta, "fasta"))
kmer_matrix = np.zeros((len(records_raw), len(kmers)), dtype=float)

for i, r in enumerate(records_raw):
    s = str(r.seq).upper()
    total_kmers = len(s) - k + 1
    counts = Counter()
    for j in range(total_kmers):
        km = s[j:j+k]
        if km in kmer_to_idx:
            counts[km] += 1
            
    for km, count in counts.items():
        kmer_matrix[i, kmer_to_idx[km]] = count / total_kmers

df_kmer_features = pd.DataFrame(kmer_matrix, index=[r.id for r in records_raw], columns=kmers)
kmer_csv_path = os.path.join(out_dir, 'kmer_feature_matrix.csv')
df_kmer_features.to_csv(kmer_csv_path)

print(f"Supplementary k=4 K-mer Feature Matrix created: {df_kmer_features.shape[0]} sequences x {df_kmer_features.shape[1]} k-mer features")
print(f"Saved to: {kmer_csv_path}")
