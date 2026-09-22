import os
from Bio import SeqIO, Phylo
from Bio.Phylo.TreeConstruction import DistanceCalculator, DistanceTreeConstructor

in_fasta = '/Users/vimalkansotia/Downloads/Bioinformatics/data/processed/aligned_sequences_unique_ids.fasta'
tree_out = '/Users/vimalkansotia/Downloads/Bioinformatics/results/trees/pcv3_iqtree.treefile'

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
