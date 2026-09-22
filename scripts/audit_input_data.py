import os
import pandas as pd
import numpy as np
from Bio import SeqIO
from collections import Counter
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

fasta_path = BASE_DIR
excel_path = BASE_DIR

print("==================================================")
print("COMPREHENSIVE INPUT DATA AUDIT")
print("==================================================")

# 1. FASTA Audit
records = list(SeqIO.parse(fasta_path, "fasta"))
seq_count = len(records)
print(f"Total FASTA Sequences: {seq_count}")

seq_lengths = [len(r.seq) for r in records]
min_len = int(np.min(seq_lengths))
max_len = int(np.max(seq_lengths))
mean_len = float(np.mean(seq_lengths))
median_len = float(np.median(seq_lengths))

print(f"Sequence Lengths: Min={min_len}, Max={max_len}, Mean={mean_len:.2f}, Median={median_len:.1f}")

# Check GC, Ambiguous, Invalid
gc_list = []
ambig_seqs = 0
total_ambig_bases = 0
invalid_chars = 0
all_seqs_str = []

for r in records:
    s = str(r.seq).upper()
    all_seqs_str.append(s)
    g = s.count('G')
    c = s.count('C')
    a = s.count('A')
    t = s.count('T')
    gc = (g + c) / len(s) * 100
    gc_list.append(gc)
    
    ambig = sum(s.count(b) for b in "RYSWKMBDHVN")
    if ambig > 0:
        ambig_seqs += 1
        total_ambig_bases += ambig
        
    invalid = sum(1 for char in s if char not in "ATCGRYSWKMBDHVN")
    invalid_chars += invalid

duplicate_sequence_strings = len(all_seqs_str) - len(set(all_seqs_str))

print(f"GC Content: Mean={np.mean(gc_list):.2f}%, Min={np.min(gc_list):.2f}%, Max={np.max(gc_list):.2f}%")
print(f"Sequences with Ambiguous Bases: {ambig_seqs} / {seq_count} (Total ambiguous bases: {total_ambig_bases})")
print(f"Total Invalid Characters: {invalid_chars}")
print(f"Duplicate Sequence Strings (100% identity): {duplicate_sequence_strings}")

# Header parsing
fasta_parsed = []
for i, r in enumerate(records):
    header = r.id
    parts = header.rsplit('_', 2)
    acc = parts[0] if len(parts) == 3 else header
    country = parts[1] if len(parts) == 3 else "Unknown"
    year = parts[2] if len(parts) == 3 else "Unknown"
    
    acc_clean = acc.strip()
    acc_base = acc_clean.split('.')[0]
    
    fasta_parsed.append({
        'fasta_index': i,
        'seq_id': header,
        'fasta_acc_raw': acc,
        'fasta_acc_clean': acc_clean,
        'fasta_acc_base': acc_base,
        'fasta_country': country,
        'fasta_year': year,
        'length': len(r.seq)
    })

df_fasta = pd.DataFrame(fasta_parsed)
print(f"Unique accessions in FASTA (raw): {df_fasta['fasta_acc_clean'].nunique()}")
print(f"Unique base accessions in FASTA: {df_fasta['fasta_acc_base'].nunique()}")
dup_fasta_acc = df_fasta[df_fasta['fasta_acc_clean'].duplicated(keep=False)]
print(f"FASTA records with duplicated accession IDs: {len(dup_fasta_acc)}")

# 2. Excel Audit
df_excel = pd.read_excel(excel_path)
excel_rows = len(df_excel)
print(f"\nTotal Excel Rows: {excel_rows}")
print(f"Raw Excel Columns: {df_excel.columns.tolist()}")

df_excel.columns = [c.strip() for c in df_excel.columns]
print(f"Cleaned Excel Columns: {df_excel.columns.tolist()}")

df_excel['excel_acc_clean'] = df_excel['accession'].astype(str).str.strip()
df_excel['excel_acc_base'] = df_excel['excel_acc_clean'].str.split('.').str[0]
df_excel['excel_region_clean'] = df_excel['Region'].astype(str).str.strip()

print(f"Missing values in Excel:\n{df_excel[['accession', 'Region']].isna().sum()}")
print(f"Unique accessions in Excel (raw): {df_excel['excel_acc_clean'].nunique()}")
print(f"Unique base accessions in Excel: {df_excel['excel_acc_base'].nunique()}")
dup_excel_rows = df_excel.duplicated(subset=['accession', 'Region']).sum()
print(f"Exact Duplicate rows in Excel: {dup_excel_rows}")
dup_excel_acc = df_excel[df_excel['excel_acc_clean'].duplicated(keep=False)]
print(f"Excel rows with duplicated accession IDs: {len(dup_excel_acc)}")

# 3. Matching Validation
print("\n--- FASTA vs EXCEL MATCHING ANALYSIS ---")

# Method A: Index-by-index order comparison
order_matches = (df_fasta['fasta_acc_clean'] == df_excel['excel_acc_clean']).sum()
print(f"Index-by-index order match (FASTA row == Excel row): {order_matches} / 500")

# Method B: Key-based matching on exact accession string
merged_exact = pd.merge(df_fasta, df_excel, left_on='fasta_acc_clean', right_on='excel_acc_clean', how='inner')
print(f"Key-based exact accession matches: {len(merged_exact)}")

# Method C: Key-based matching on base accession (without version)
merged_base = pd.merge(df_fasta, df_excel, left_on='fasta_acc_base', right_on='excel_acc_base', how='inner')
print(f"Key-based base accession matches: {len(merged_base)}")

# Unmatched analysis
unmatched_fasta_base = df_fasta[~df_fasta['fasta_acc_base'].isin(df_excel['excel_acc_base'])]
print(f"Unmatched FASTA base accessions in Excel: {len(unmatched_fasta_base)}")
if len(unmatched_fasta_base) > 0:
    print("Unmatched FASTA sequences:")
    print(unmatched_fasta_base[['seq_id', 'fasta_acc_clean']])

unmatched_excel_base = df_excel[~df_excel['excel_acc_base'].isin(df_fasta['fasta_acc_base'])]
print(f"Unmatched Excel base accessions in FASTA: {len(unmatched_excel_base)}")
if len(unmatched_excel_base) > 0:
    print("Unmatched Excel rows:")
    print(unmatched_excel_base[['accession', 'Region']])

# Country consistency check between FASTA header and Excel Region
print("\nCountry Consistency Check (FASTA Header Country vs Excel Region):")
# Normalize names for comparison
country_map = {'SouthKorea': 'South Korea', 'NorthAmerica': 'N America', 'N America': 'N America'}
df_fasta['norm_country'] = df_fasta['fasta_country'].replace(country_map)
df_excel['norm_region'] = df_excel['excel_region_clean'].replace(country_map)

# Let's compare row-by-row mapping
df_joined = df_fasta.merge(df_excel, left_on='fasta_acc_clean', right_on='excel_acc_clean', how='left')
mismatch_geo = df_joined[df_joined['norm_country'] != df_joined['norm_region']]
print(f"Accession-matched records where FASTA header Country differs from Excel Region: {len(mismatch_geo)}")
if len(mismatch_geo) > 0:
    print(mismatch_geo[['seq_id', 'fasta_country', 'excel_region_clean']].head(10))

print("\nMatched examples (First 10):")
print(df_joined[['seq_id', 'fasta_acc_clean', 'fasta_country', 'excel_region_clean', 'fasta_year']].head(10))
