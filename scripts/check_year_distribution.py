import pandas as pd
from Bio import SeqIO
from collections import Counter

fasta_path = '/Users/vimalkansotia/Downloads/Bioinformatics/data/raw/viral_genome.fasta'

records = list(SeqIO.parse(fasta_path, "fasta"))
years = []
year_to_ids = {}

for r in records:
    header = r.id
    parts = header.rsplit('_', 2)
    year_str = parts[2] if len(parts) == 3 else "Unknown"
    try:
        yr = int(year_str)
        years.append(yr)
        if yr not in year_to_ids:
            year_to_ids[yr] = []
        year_to_ids[yr].append(header)
    except ValueError:
        pass

df_years = pd.DataFrame(years, columns=['Year'])
print("="*60)
print("EMPIRICAL YEAR DISTRIBUTION IN TEACHER'S viral_genome.fasta")
print("="*60)
print(f"Total parsed years: {len(years)} / {len(records)} sequences")
print(f"Minimum Year: {df_years['Year'].min()}")
print(f"Maximum Year: {df_years['Year'].max()}")
print("\nYear breakdown (sorted by year):")
print(df_years['Year'].value_counts().sort_index())

print("\nExamples of 1996 isolates in FASTA:")
if 1996 in year_to_ids:
    for sid in year_to_ids[1996]:
        print("  -", sid)

print("\nExamples of 2025 isolates in FASTA:")
if 2025 in year_to_ids:
    for sid in year_to_ids[2025]:
        print("  -", sid)
