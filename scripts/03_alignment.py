import subprocess
import os
import numpy as np
from Bio import SeqIO
from collections import Counter
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

raw_fasta = BASE_DIR
aligned_fasta = BASE_DIR

print("="*60)
print("PHASE 4 — MULTIPLE SEQUENCE ALIGNMENT (MAFFT)")
print("="*60)

# Run MAFFT alignment
cmd = f"mafft --auto --thread -1 {raw_fasta} > {aligned_fasta}"
print(f"Executing MAFFT command: {cmd}")

result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
if result.returncode != 0:
    print(f"MAFFT alignment failed with error:\n{result.stderr}")
    exit(1)

print("MAFFT alignment completed successfully!")

# Parse alignment and calculate statistics
aligned_records = list(SeqIO.parse(aligned_fasta, "fasta"))
seq_count = len(aligned_records)
alignment_len = len(aligned_records[0].seq)

print(f"Number of aligned sequences: {seq_count}")
print(f"Alignment length: {alignment_len} bp")

# Convert alignment to numpy matrix for character analysis
align_matrix = np.array([list(str(r.seq).upper()) for r in aligned_records])

conserved_sites = 0
variable_sites = 0
parsimony_sites = 0
total_gaps = 0

for j in range(alignment_len):
    col = align_matrix[:, j]
    total_gaps += np.sum(col == '-')
    
    # Filter gaps/N for state counting
    valid_states = [c for c in col if c in "ATCG"]
    counts = Counter(valid_states)
    
    if len(counts) <= 1:
        conserved_sites += 1
    else:
        variable_sites += 1
        # Parsimony informative: at least 2 distinct states occurring in at least 2 sequences
        states_gt1 = sum(1 for state, cnt in counts.items() if cnt >= 2)
        if states_gt1 >= 2:
            parsimony_sites += 1

gap_percentage = (total_gaps / (seq_count * alignment_len)) * 100

print(f"\nAlignment Statistics Summary:")
print(f"  - Total Alignment Length: {alignment_len} bp")
print(f"  - Conserved Positions: {conserved_sites} bp ({conserved_sites/alignment_len*100:.2f}%)")
print(f"  - Variable / Polymorphic Positions: {variable_sites} bp ({variable_sites/alignment_len*100:.2f}%)")
print(f"  - Parsimony-Informative Sites: {parsimony_sites} bp ({parsimony_sites/alignment_len*100:.2f}%)")
print(f"  - Overall Gap Percentage: {gap_percentage:.2f}%")
