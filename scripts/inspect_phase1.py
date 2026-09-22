import pandas as pd
import numpy as np
from Bio import SeqIO
from collections import Counter
import os

fasta_path = '/Users/vimalkansotia/Downloads/Bioinformatics/viral_genome.fasta'
excel_path = '/Users/vimalkansotia/Downloads/Bioinformatics/accessions.csv.xlsx'

print("="*60)
print("PHASE 1 — INSPECTION OF ACTUAL DATASET")
print("="*60)

# 1. FASTA Inspection
print("\n--- 1. VIRAL GENOME FASTA INSPECTION ---")
records = list(SeqIO.parse(fasta_path, "fasta"))
seq_count = len(records)
print(f"Total FASTA sequences: {seq_count}")

seq_ids = [r.id for r in records]
seq_descriptions = [r.description for r in records]
seq_lengths = [len(r.seq) for r in records]

min_len = int(np.min(seq_lengths))
max_len = int(np.max(seq_lengths))
mean_len = float(np.mean(seq_lengths))
median_len = float(np.median(seq_lengths))

print(f"Sequence Lengths -> Min: {min_len}, Max: {max_len}, Mean: {mean_len:.2f}, Median: {median_len:.1f}")

# Calculate GC content & Ambiguous bases
gc_contents = []
ambiguous_counts = []
invalid_char_counts = []
standard_bases = set("ATCGatcg")
ambiguous_bases_set = set("RYSWKMBDHVNryswkmbdhvn")

all_seq_strings = [str(r.seq) for r in records]
unique_seq_strings = set(all_seq_strings)
duplicate_seq_count = len(all_seq_strings) - len(unique_seq_strings)

for r in records:
    s = str(r.seq).upper()
    g = s.count('G')
    c = s.count('C')
    a = s.count('A')
    t = s.count('T')
    total = len(s)
    gc = (g + c) / total * 100 if total > 0 else 0
    gc_contents.append(gc)
    
    # ambiguous & invalid
    ambig = sum(s.count(b) for b in "RYSWKMBDHVN")
    invalid = sum(1 for char in s if char not in "ATCGRYSWKMBDHVN")
    ambiguous_counts.append(ambig)
    invalid_char_counts.append(invalid)

mean_gc = float(np.mean(gc_contents))
seqs_with_ambig = sum(1 for c in ambiguous_counts if c > 0)
total_ambig_bases = sum(ambiguous_counts)
total_invalid_chars = sum(invalid_char_counts)

print(f"Mean GC Content: {mean_gc:.2f}% (Range: {np.min(gc_contents):.2f}% - {np.max(gc_contents):.2f}%)")
print(f"Sequences with ambiguous bases: {seqs_with_ambig} / {seq_count} (Total ambiguous bases: {total_ambig_bases})")
print(f"Total invalid characters: {total_invalid_chars}")
print(f"Duplicate identical sequence strings in FASTA: {duplicate_seq_count}")

print("\nSample FASTA IDs (first 10):")
for sid in seq_ids[:10]:
    print("  -", sid)

# 2. Excel Inspection
print("\n--- 2. ACCESSIONS EXCEL METADATA INSPECTION ---")
df = pd.read_excel(excel_path)
print(f"Total metadata rows: {len(df)}")
print(f"Total metadata columns: {len(df.columns)}")
print("\nAll Column Names & Data Types & Non-Null Counts:")
for col in df.columns:
    non_nulls = df[col].notna().sum()
    nulls = df[col].isna().sum()
    dtype = df[col].dtype
    print(f"  Column: '{col}' | Type: {dtype} | Non-Null: {non_nulls} | Missing: {nulls}")

print("\nMissing Values Summary across all columns:")
print(df.isna().sum())

duplicate_rows = df.duplicated().sum()
print(f"\nDuplicate metadata rows: {duplicate_rows}")

print("\nFirst 5 rows of metadata:")
print(df.head())

print("\nValue distributions for potential Accession, Country, and Year columns:")
for col in df.columns:
    print(f"\n--- Top values in column '{col}' ---")
    print(df[col].value_counts(dropna=False).head(10))
