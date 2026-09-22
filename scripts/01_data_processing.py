import pandas as pd
import numpy as np
from Bio import SeqIO
import os
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

fasta_path = BASE_DIR
excel_path = BASE_DIR
out_path = BASE_DIR

# Load Excel metadata
df_excel = pd.read_excel(excel_path)
df_excel.columns = [c.strip() for c in df_excel.columns]
df_excel['excel_acc'] = df_excel['accession'].astype(str).str.strip()
df_excel['excel_region'] = df_excel['Region'].astype(str).str.strip()

# Build Excel lookup dictionary (acc -> list of regions)
excel_lookup = {}
for idx, row in df_excel.iterrows():
    acc = row['excel_acc']
    reg = row['excel_region']
    if acc not in excel_lookup:
        excel_lookup[acc] = []
    excel_lookup[acc].append(reg)

# Standardize Country/Region names mapping for consistency
country_norm_map = {
    'SouthKorea': 'South Korea',
    'NorthAmerica': 'N America',
    'N America': 'N America'
}

# Process FASTA records
records = list(SeqIO.parse(fasta_path, "fasta"))
master_rows = []

for idx, r in enumerate(records):
    header = r.id
    parts = header.rsplit('_', 2)
    acc = parts[0] if len(parts) == 3 else header
    country = parts[1] if len(parts) == 3 else "Unknown"
    year_str = parts[2] if len(parts) == 3 else "Unknown"
    try:
        year = int(year_str)
    except ValueError:
        year = np.nan
        
    seq_str = str(r.seq).upper()
    seq_len = len(seq_str)
    gc_content = (seq_str.count('G') + seq_str.count('C')) / seq_len * 100
    ambig_count = sum(seq_str.count(b) for b in "RYSWKMBDHVN")
    
    country_norm = country_norm_map.get(country, country)
    
    # Metadata provenance check against Excel
    excel_regions = excel_lookup.get(acc, [])
    if len(excel_regions) == 0:
        provenance = "FASTA_Header_Only"
        excel_region_str = "Absent_in_Excel"
    else:
        excel_region_str = "/".join(sorted(list(set(excel_regions))))
        norm_excel_regs = [country_norm_map.get(r, r) for r in excel_regions]
        if len(set(norm_excel_regs)) > 1:
            provenance = "Geography_Conflict_Excel"
        elif norm_excel_regs[0] == country_norm:
            provenance = "Excel_Verified"
        else:
            provenance = "Geography_Conflict_Excel"
            
    master_rows.append({
        'fasta_index': idx,
        'seq_id': header,
        'accession': acc,
        'country': country_norm,
        'year': year,
        'sequence_length': seq_len,
        'gc_content': round(gc_content, 2),
        'ambiguous_bases': ambig_count,
        'excel_regions': excel_region_str,
        'metadata_provenance': provenance
    })

df_master = pd.DataFrame(master_rows)
df_master.to_csv(out_path, index=False)
print(f"Master metadata saved to {out_path}")
print(f"Total Master Records: {len(df_master)}")
print("\nMetadata Provenance Breakdown:")
print(df_master['metadata_provenance'].value_counts())
print("\nCountry Distribution:")
print(df_master['country'].value_counts())
print("\nYear Summary:")
print(df_master['year'].describe())
