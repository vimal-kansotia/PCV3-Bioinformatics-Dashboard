import os
import pandas as pd
import re
from Bio import SeqIO
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

fasta_path = BASE_DIR
excel_path = BASE_DIR

df = pd.read_excel(excel_path)
df.columns = [c.strip() for c in df.columns]

records = list(SeqIO.parse(fasta_path, "fasta"))

parsed_records = []
for i, r in enumerate(records):
    header = r.id
    # Split from right side for year and country!
    # Format is <Accession>_<Country>_<Year>
    # Since accession can contain '_', r.id.rsplit('_', 2) will split into [Accession, Country, Year]!
    parts = header.rsplit('_', 2)
    if len(parts) == 3:
        acc, country, year = parts[0], parts[1], parts[2]
    else:
        acc, country, year = header, "Unknown", "Unknown"
        
    parsed_records.append({
        'fasta_index': i,
        'seq_id': header,
        'acc_in_fasta': acc,
        'country_in_fasta': country,
        'year_in_fasta': year,
        'length': len(r.seq)
    })

df_fasta = pd.DataFrame(parsed_records)

print(df_fasta.head(15))

# Let's clean accessions for matching
# e.g. remove version (.1, .2) or handle exact match
df['acc_clean'] = df['accession'].astype(str).str.strip()
df_fasta['acc_clean'] = df_fasta['acc_in_fasta'].astype(str).str.strip()

# Check how many exact matches on acc_clean
matched_exact = pd.merge(df_fasta, df, on='acc_clean', how='inner')
print(f"\nExact accession match count (with version): {len(matched_exact)}")

# Try stripping version suffix (.1, .2, etc.) for both
df['acc_no_version'] = df['acc_clean'].str.split('.').str[0]
df_fasta['acc_no_version'] = df_fasta['acc_clean'].str.split('.').str[0]

matched_no_ver = pd.merge(df_fasta, df, on='acc_no_version', how='inner')
print(f"Match count without version suffix: {len(matched_no_ver)}")

# Check duplicate accessions in Excel
dup_excel_acc = df[df['accession'].duplicated(keep=False)]
print(f"\nDuplicate accession rows in Excel: {len(dup_excel_acc)}")
print(dup_excel_acc)

# Check duplicate accessions in FASTA
dup_fasta_acc = df_fasta[df_fasta['acc_in_fasta'].duplicated(keep=False)]
print(f"\nDuplicate accession rows in FASTA: {len(dup_fasta_acc)}")
print(dup_fasta_acc)
