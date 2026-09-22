# Porcine Circovirus 3 (PCV3) Genome Variation & Unsupervised ML Pipeline

## Project Overview
This repository contains a comprehensive Bioinformatics and Data Science pipeline for analyzing **Genome Variation, Phylogenetic Relationships, and Geographic/Temporal Patterns** across **500 Porcine Circovirus 3 (PCV3)** complete genome sequences.

The project combines sequence quality control, multiple sequence alignment (MAFFT), SNP genome variation analysis, unsupervised machine learning (PCA and K-Means clustering), statistical independence testing (Monte Carlo Chi-square and Cramér's V), and Maximum Likelihood phylogenetics (IQ-TREE 3 ModelFinder).

---

## Repository Folder Structure
```text
Bioinformatics/
├── data/
│   ├── raw/                           # Original teacher-provided raw files
│   │   ├── viral_genome.fasta         # 500 PCV3 FASTA genomes
│   │   └── accessions.csv.xlsx        # Excel metadata sheet (500 rows)
│   └── processed/                     # Cleaned, aligned, and extracted data
│       ├── master_metadata.csv        # Master dataset with metadata provenance flags
│       ├── aligned_sequences.fasta    # MAFFT 2,156 bp alignment
│       ├── snp_feature_matrix.csv     # One-hot encoded SNP matrix (2,067 binary features)
│       └── kmer_feature_matrix.csv    # Supplementary k=4 k-mer matrix (256 features)
├── scripts/
│   ├── 01_data_processing.py          # Metadata cleaning and accession matching
│   ├── 02_sequence_qc.py              # Sequence length, GC content, and metadata QC
│   ├── 03_alignment.py                # MAFFT alignment execution & MSA stats
│   ├── 04_variation.py                # SNP/variant position extraction & density
│   ├── 05_features.py                 # Genome SNP & k-mer feature extraction
│   ├── 06_pca_clustering.py           # PCA & K-Means clustering (silhouette scores)
│   ├── 07_phylogeny.py                # IQ-TREE 3 ModelFinder tree & distance heatmap
│   ├── 08_statistics.py               # Chi-square permutation tests & Cramér's V
│   └── make_presentation.py           # 18-slide PowerPoint generator (.pptx)
├── results/
│   ├── figures/                       # Presentation-quality figures (fig01–fig16)
│   ├── tables/                        # Statistical & metadata summary tables (table00–table04)
│   ├── trees/                         # Newick tree files & IQ-TREE log output
│   └── reports/                       # Viva Q&A document (viva_questions.md)
├── presentation/
│   └── PCV3_analysis.pptx             # MSc Practical Presentation (.pptx)
├── requirements.txt                   # Required Python dependencies
└── README.md                          # Project documentation
```

---

## Requirements & Software Setup

### 1. External Bioinformatics Tools
- **MAFFT** (v7.526+)
- **IQ-TREE 3** (v3.1.4+)

Install via Homebrew (macOS):
```bash
brew install mafft iqtree3
```

### 2. Python Environment
Install dependencies via `pip`:
```bash
pip install -r requirements.txt
```

Required Python packages:
- `biopython`
- `pandas`
- `numpy`
- `scikit-learn`
- `scipy`
- `matplotlib`
- `seaborn`
- `openpyxl`
- `python-pptx`

---

## Pipeline Execution Steps

Execute the scripts sequentially from the root directory:

```bash
# Step 1: Master Metadata Processing
python3 scripts/01_data_processing.py

# Step 2: Sequence Quality Control & Figures 1-4
python3 scripts/02_sequence_qc.py

# Step 3: MAFFT Multiple Sequence Alignment
python3 scripts/03_alignment.py

# Step 4: SNP Genome Variation & Figures 5-6
python3 scripts/04_variation.py

# Step 5: Feature Extraction (SNP & k-mer matrices)
python3 scripts/05_features.py

# Step 6: PCA & K-Means Clustering (Figures 7-11)
python3 scripts/06_pca_clustering.py

# Step 7: Geographic & Temporal Statistical Association (Figures 12-13)
python3 scripts/08_statistics.py

# Step 8: IQ-TREE Phylogenetics & Distance Heatmap (Figures 14-16)
python3 scripts/07_phylogeny.py

# Step 9: PowerPoint Presentation Generation
python3 scripts/make_presentation.py
```

---

## Key Findings Summary

1. **Genome Characteristics**: PCV3 circular genome (~2,000 bp, mean GC 50.28%) aligned to 2,156 bp with 890 variable sites (466 parsimony-informative). Mean pairwise nucleotide divergence is 1.17% (max 4.89%).
2. **Unsupervised ML**: PCA on mean-centered SNP features captured major genomic variation (PC1: 22.37%, PC2: 15.65%). K-Means clustering with Silhouette evaluation ($k=2..10$) identified $k=7$ as the selected statistical clustering configuration (Silhouette Score = 0.6047).
3. **Geographical Association**: Monte Carlo permutation Chi-square test revealed significant association between PCV3 clusters and geographic region ($\chi^2 = 525.36, p = 0.0002, \text{Cramér's } V = 0.4185$).
4. **Temporal Association**: Grouping into temporal periods (`<2015`, `2015–2017`, `2018–2020`, `2021–2025`) demonstrated significant temporal clustering ($\chi^2 = 145.50, p = 0.0002, \text{Cramér's } V = 0.3114$).
5. **Phylogenetics**: IQ-TREE 3 ModelFinder selected substitution model `GTR+F+I+G4`. The phylogenetic tree structure was broadly consistent with the K-Means genomic clustering patterns.

---

## Study Limitations
- **Sampling Imbalance**: High sample concentration from China ($N=117$), USA ($N=69$), Spain ($N=57$), and South Korea ($N=51$).
- **Metadata Inconsistencies**: 16 records in Excel had conflicting regions (e.g., Spain vs Poland) and 10 were absent from Excel. Flagged explicitly as `Geography_Conflict_Excel` and `FASTA_Header_Only`.
- **Causality Constraint**: Statistical association does NOT prove geographical transmission routes, origin, or viral divergence causality.
