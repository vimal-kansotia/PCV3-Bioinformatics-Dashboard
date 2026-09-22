import os
import re
from pptx import Presentation
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

pptx_path = BASE_DIR
prs = Presentation(pptx_path)

# Extract all unique words
words = set()
for slide in prs.slides:
    for shape in slide.shapes:
        if shape.has_text_frame:
            for p in shape.text_frame.paragraphs:
                for word in re.findall(r'\b[A-Za-z]{3,}\b', p.text):
                    words.add(word)

# Known domain terms
valid_bio_terms = {
    'PCV', 'MAFFT', 'SNPs', 'SNP', 'PCA', 'Means', 'UFBoot', 'BIC', 'GTR', 'IUPAC', 
    'Phan', 'Stadejek', 'Franzo', 'Minh', 'Virology', 'PLOS', 'ONE', 'Evol', 'Biol',
    'Dermatitis', 'Nephropathy', 'Circovirus', 'Circoviridae', 'ssDNA', 'Porcine',
    'alignment', 'conserved', 'polymorphic', 'parsimony', 'heatmap', 'dof', 'perms',
    'divergence', 'contingency', 'delineate', 'provenance', 'sublineages', 'multisystemic',
    'replicase', 'capsid', 'tetranucleotide', 'ordination', 'subsample', 'subsampled'
}

suspicious = []
for w in words:
    # Check simple spelling rules or non-standard capitalization
    if not w[0].isupper() and not w.islower():
        suspicious.append(w)

print("Audited words count:", len(words))
print("Suspicious words:", suspicious)
