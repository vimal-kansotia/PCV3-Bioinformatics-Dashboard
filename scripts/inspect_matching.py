import pandas as pd
from Bio import SeqIO

fasta_path = '/Users/vimalkansotia/Downloads/Bioinformatics/viral_genome.fasta'
excel_path = '/Users/vimalkansotia/Downloads/Bioinformatics/accessions.csv.xlsx'

# Load excel
df = pd.read_excel(excel_path)
# Strip column names
df.columns = [c.strip() for c in df.columns]

print("Excel columns stripped:", df.columns.tolist())

# Inspect FASTA records
records = list(SeqIO.parse(fasta_path, "fasta"))

fasta_info = []
for r in records:
    # Header format e.g. PD363191.1_China_2000
    parts = r.id.split('_')
    acc_raw = parts[0]
    # strip version for robust matching if needed, or keep full
    acc_base = acc_raw.split('.')[0]
    
    country = parts[1] if len(parts) > 1 else 'Unknown'
    year = parts[2] if len(parts) > 2 else 'Unknown'
    
    fasta_info.append({
        'seq_id': r.id,
        'acc_raw': acc_raw,
        'acc_base': acc_base,
        'fasta_country': country,
        'fasta_year': year,
        'length': len(r.seq)
    })

df_fasta = pd.DataFrame(fasta_info)

# Add base accession to excel df
df['acc_base'] = df['accession'].astype(str).str.strip().str.split('.').str[0]
df['acc_raw'] = df['accession'].astype(str).str.strip()

print("\nFASTA parsed head:")
print(df_fasta.head(10))

print("\nExcel head:")
print(df.head(10))

# Matching analysis
matched_raw = pd.merge(df_fasta, df, on='acc_raw', how='inner')
print(f"\nExact raw accession match count: {len(matched_raw)}")

matched_base = pd.merge(df_fasta, df, on='acc_base', how='inner')
print(f"Base accession match count: {len(matched_base)}")

# Let's inspect any unmatched records
unmatched_fasta = df_fasta[~df_fasta['acc_base'].isin(df['acc_base'])]
print(f"Unmatched FASTA records (by base accession): {len(unmatched_fasta)}")
if len(unmatched_fasta) > 0:
    print("Unmatched FASTA records:", unmatched_fasta[['seq_id', 'acc_raw']])

unmatched_excel = df[~df['acc_base'].isin(df_fasta['acc_base'])]
print(f"Unmatched Excel records (by base accession): {len(unmatched_excel)}")
if len(unmatched_excel) > 0:
    print("Unmatched Excel records:", unmatched_excel[['accession', 'Region']])

print("\nExcel Region distribution:")
print(df['Region'].value_counts())

print("\nFASTA Parsed Country distribution:")
print(df_fasta['fasta_country'].value_counts())

print("\nFASTA Parsed Year distribution:")
print(df_fasta['fasta_year'].value_counts())
