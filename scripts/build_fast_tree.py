import os
from Bio import SeqIO, Phylo
from Bio.Phylo.TreeConstruction import DistanceCalculator, DistanceTreeConstructor
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

in_fasta = os.path.join(BASE_DIR, 'fasta')
tree_out = BASE_DIR

if not os.path.exists(tree_out):
    print("Generating rapid Neighbor-Joining tree fallback while IQ-TREE completes...")
    records = list(SeqIO.parse(in_fasta, "fasta"))
    
    # Subsample 150 sequences for fast initial NJ tree construction
    sub_records = records[:150]
    
    calculator = DistanceCalculator('identity')
    dm = calculator.get_distance(sub_records)
    constructor = DistanceTreeConstructor()
    tree = constructor.nj(dm)
    
    Phylo.write(tree, tree_out, "newick")
    print(f"Fallback tree saved to {tree_out}")
else:
    print(f"Tree file already exists at {tree_out}")
