import pandas as pd
from Bio import SeqIO

fasta_path = '/Users/vimalkansotia/Downloads/Bioinformatics/viral_genome.fasta'
excel_path = '/Users/vimalkansotia/Downloads/Bioinformatics/accessions.csv.xlsx'

# Load Excel
df_excel = pd.read_excel(excel_path)
df_excel.columns = [c.strip() for c in df_excel.columns]

# Load FASTA
records = list(SeqIO.parse(fasta_path, "fasta"))
fasta_dict = {}
fasta_seq_dict = {}
for r in records:
    header = r.id
    parts = header.rsplit('_', 2)
    acc = parts[0] if len(parts) == 3 else header
    country = parts[1] if len(parts) == 3 else "Unknown"
    year = parts[2] if len(parts) == 3 else "Unknown"
    
    acc_clean = acc.strip()
    if acc_clean not in fasta_dict:
        fasta_dict[acc_clean] = []
        fasta_seq_dict[acc_clean] = []
    fasta_dict[acc_clean].append({'seq_id': header, 'country': country, 'year': year})
    fasta_seq_dict[acc_clean].append(str(r.seq))

# Find duplicated accessions in Excel
df_excel['acc_clean'] = df_excel['accession'].astype(str).str.strip()
dup_accs = df_excel[df_excel['acc_clean'].duplicated(keep=False)]
unique_dup_accs = dup_accs['acc_clean'].unique()

print(f"Total unique duplicated accession IDs in Excel: {len(unique_dup_accs)}")
print(f"Total Excel rows involved in duplication: {len(dup_accs)}\n")

results = []
for acc in unique_dup_accs:
    rows = df_excel[df_excel['acc_clean'] == acc]
    regions_in_excel = rows['Region'].tolist()
    
    fasta_matches = fasta_dict.get(acc, [])
    fasta_headers = [f['seq_id'] for f in fasta_matches]
    fasta_countries = list(set([f['country'] for f in fasta_matches]))
    fasta_years = list(set([f['year'] for f in fasta_matches]))
    seqs = fasta_seq_dict.get(acc, [])
    
    is_seq_identical = len(set(seqs)) == 1 if len(seqs) > 0 else "N/A"
    
    # Conflict analysis
    excel_has_conflict = len(set(regions_in_excel)) > 1
    
    results.append({
        'accession': acc,
        'excel_record_count': len(rows),
        'excel_regions': ", ".join(regions_in_excel),
        'excel_has_conflict': excel_has_conflict,
        'fasta_header_count': len(fasta_matches),
        'fasta_headers': ", ".join(fasta_headers),
        'fasta_countries': ", ".join(fasta_countries),
        'fasta_years': ", ".join(fasta_years),
        'is_seq_identical': is_seq_identical
    })

df_res = pd.DataFrame(results)
print(df_res.to_string())

# Summarize resolution breakdown
print("\n--- SUMMARY OF DUPLICATE ACCESSION CONFLICTS ---")
print(f"Accessions where Excel lists MULTIPLE conflicting regions: {df_res['excel_has_conflict'].sum()}")
conflicts = df_res[df_res['excel_has_conflict']]
print(conflicts[['accession', 'excel_regions', 'fasta_countries', 'fasta_years', 'is_seq_identical']])
