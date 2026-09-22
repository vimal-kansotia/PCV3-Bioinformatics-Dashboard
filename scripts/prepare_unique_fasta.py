import os
from Bio import SeqIO

in_fasta = '/Users/vimalkansotia/Downloads/Bioinformatics/data/processed/aligned_sequences.fasta'
out_fasta = '/Users/vimalkansotia/Downloads/Bioinformatics/data/processed/aligned_sequences_unique_ids.fasta'

records = list(SeqIO.parse(in_fasta, "fasta"))
unique_records = []
seen = {}

for idx, r in enumerate(records):
    base_id = r.id
    if base_id not in seen:
        seen[base_id] = 1
        new_id = base_id
    else:
        seen[base_id] += 1
        new_id = f"{base_id}_dup{seen[base_id]}"
        
    r.id = new_id
    r.description = new_id
    unique_records.append(r)

SeqIO.write(unique_records, out_fasta, "fasta")
print(f"Unique header FASTA written with {len(unique_records)} sequences to {out_fasta}")
