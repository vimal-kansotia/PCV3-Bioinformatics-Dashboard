# VIVA VOCE EXAMINATION QUESTIONS & ANSWERS
## Project: Analysis of Genome Variation, Phylogenetic Relationships, and Geographic/Temporal Patterns in Porcine Circovirus 3 (PCV3)

---

### Q1: What is Porcine Circovirus 3 (PCV3) and why is its genomic investigation significant?
**Answer**:  
Porcine Circovirus 3 (PCV3) is a non-enveloped, single-stranded circular DNA (ssDNA) virus belonging to the family *Circoviridae*, genus *Circovirus*. Discovered via next-generation sequencing in 2015–2016, PCV3 is associated with Porcine Dermatitis and Nephropathy Syndrome (PDNS)-like disease, reproductive failure in sows, cardiac lesions, and multisystemic inflammation in swine worldwide. Investigating its genome variation across ~500 isolates helps identify circulating genotypes, baseline evolutionary dynamics, and potential associations between genomic features, temporal shifts, and geographical locations.

---

### Q2: What is a FASTA file format and how were the PCV3 sequence headers structured?
**Answer**:  
A FASTA file is a text-based format for representing nucleotide or peptide sequences, where each entry begins with a single-line description header prefixed by a `>` character, followed by sequence lines. In this project, the headers were formatted as `<Accession>_<Country/Region>_<Year>` (e.g., `PD363191.1_China_2000`). We used Python string splitting (`header.rsplit('_', 2)`) to extract the GenBank accession ID, geographical location, and sample collection year for all 500 sequence records.

---

### Q3: How do the phylogenetic tree topology and K-Means clusters relate to each other?
**Answer**:  
**The phylogenetic tree structure was broadly consistent with the K-Means genomic clustering patterns.** K-Means operates on Euclidean distance in principal component space derived from one-hot encoded SNP features, while IQ-TREE 3 estimates Maximum Likelihood branch lengths based on the `GTR+F+I+G4` substitution model. Comparing the tree tip colors with the K-Means cluster labels shows that sequence groups forming discrete K-Means clusters map to coherent clades on the ML tree. Avoid claiming that the tree "confirms" or "validates" the K-Means clusters, since no formal tree-vs-cluster concordance statistic (such as Robinson-Foulds distance or tanglegram alignment) was computed.

---

### Q4: How were accessions in the FASTA file matched against the Excel metadata sheet?
**Answer**:  
Rather than relying on row order (which matched only 22 out of 500 records), records were matched using unique accession IDs. In our empirical audit:
- 474 records were verified in Excel without geographic conflicts (`Excel_Verified`).
- 16 records matched accessions in Excel where Excel listed conflicting regions (e.g., Spain vs. Poland for `ON376256.1`–`ON376262.1`). These were flagged as `Geography_Conflict_Excel`.
- 10 records were present in the FASTA file with header metadata but absent from Excel. These were flagged as `FASTA_Header_Only`.
All 500 records were preserved without fabricating metadata.

---

### Q5: Why did we keep all 500 sequences including 27 identical sequences in the primary analysis?
**Answer**:  
Automatically removing identical sequences introduces sample selection bias, distorts epidemiological country/year frequencies, and violates dataset integrity. Preserving all 500 sequences ensures that geographical and temporal distributions reflect true sample proportions. The presence of 27 identical sequence strings (100% identity) was documented during Sequence Quality Control.

---

### Q6: What quality control metrics were calculated for the PCV3 sequences?
**Answer**:  
- **Sequence Length**: Min = 1,999 bp, Max = 2,006 bp, Mean = 2,000.01 bp, Median = 2,000.0 bp.
- **GC Content**: Mean = 50.28% (range 49.85% – 50.75%).
- **Ambiguous Bases**: 9 sequences contained degenerate IUPAC nucleotide codes (totaling 16 ambiguous bases).
- **Invalid Characters**: 0 non-IUPAC characters.

---

### Q7: What algorithm does MAFFT use and why was it preferred for Multiple Sequence Alignment (MSA)?
**Answer**:  
MAFFT (Multiple Alignment using Fast Fourier Transform) converts amino acid or nucleotide sequences into fast Fourier transform signals to rapidly identify homologous regions. It offers high speed and accuracy for full-length viral genomes (~2,000 bp). The alignment yielded a total alignment length of 2,156 bp.

---

### Q8: What is the difference between conserved, variable, and parsimony-informative sites?
**Answer**:  
- **Conserved Sites**: Alignment positions where all sequences share the exact same nucleotide state (1,266 bp / 58.72% in PCV3).
- **Variable Sites**: Alignment positions containing at least two different nucleotide states across samples (890 bp / 41.28%).
- **Parsimony-Informative Sites**: Variable sites containing at least two distinct nucleotide states that each appear in at least two different sequences (466 bp / 21.61%).

---

### Q9: Why did 890 variable alignment positions result in 2,067 binary SNP features?
**Answer**:  
At each of the 890 variable positions, up to 4 nucleotide states (A, C, G, T) occur across the 500 samples. One-hot encoding creates a binary indicator column $I(\text{site}_j == \text{allele})$ for every non-constant allele present at that site. Retaining all non-constant binary indicators across the 890 variable positions yields exactly **2,067 binary features**. This allows PCA and K-Means to operate on exact nucleotide substitution states without imposing artificial numerical distances between different nucleotides.

---

### Q10: Why were Country, Region, and Year strictly excluded from input ML feature matrices?
**Answer**:  
Including metadata variables (Country/Year) in PCA or K-Means clustering causes **data leakage** and circular reasoning. The goal of unsupervised learning is to discover intrinsic genome-derived structures first, and then post-hoc evaluate whether those genomic clusters correlate with geographic origin or collection year.

---

### Q11: How was Principal Component Analysis (PCA) applied to the SNP feature matrix?
**Answer**:  
PCA was performed on mean-centered informative SNP features (variants with std $> 0.05$). PCA projects the high-dimensional SNP space (2,067 features) onto orthogonal axes (Principal Components) that maximize variance capture.

---

### Q12: How much variance was explained by PC1 and PC2?
**Answer**:  
PC1 explained **22.37%** of the variance, and PC2 explained **15.65%** of the variance, giving a cumulative PC1+PC2 variance of **38.02%**.

---

### Q13: What is K-Means clustering and how does it partition genomic feature space?
**Answer**:  
K-Means is an unsupervised iterative partitioning algorithm that divides $N$ samples into $k$ clusters by minimizing the Within-Cluster Sum of Squares (WCSS / inertia):
$$\text{WCSS} = \sum_{i=1}^{k} \sum_{\mathbf{x} \in S_i} \|\mathbf{x} - \boldsymbol{\mu}_i\|^2$$
where $\boldsymbol{\mu}_i$ is the centroid of cluster $S_i$.

---

### Q14: What is the Silhouette Coefficient and how was $k$ selected?
**Answer**:  
The Silhouette Coefficient $s(i)$ measures how similar an object is to its own cluster compared to other clusters:
$$s(i) = \frac{b(i) - a(i)}{\max(a(i), b(i))}$$
where $a(i)$ is the mean intra-cluster distance and $b(i)$ is the mean nearest-cluster distance. Evaluating $k \in [2, 10]$ identified $k=7$ as the selected statistical clustering configuration (Silhouette Score = 0.6047).

---

### Q15: Why must we avoid claiming that the silhouette-selected $k$ is a biological "truth"?
**Answer**:  
The silhouette score selects the cluster count that maximizes mathematical separation in feature space. In biology, viral populations exist along evolutionary gradients with continuous mutation rates. Describing $k$ as a statistical configuration rather than an absolute biological boundary respects evolutionary complexity.

---

### Q16: How did we test the statistical association between PCV3 clusters and Geographical Location?
**Answer**:  
We constructed a $7 \times 9$ Cluster $\times$ Country contingency table and performed a Pearson's Chi-square test of independence. To address sparse cells (where expected count $<5$), we implemented a 5,000-permutation label Monte Carlo test, yielding $p = 0.0002$ and Cramér's V = 0.4185.

---

### Q17: What is Cramér's V and how is it interpreted?
**Answer**:  
Cramér's V measures the strength of association between two categorical variables on a scale from 0 (no association) to 1 (perfect association):
$$V = \sqrt{\frac{\chi^2}{N \cdot \min(r-1, c-1)}}$$
A Cramér's V of 0.4185 indicates a strong statistical association between PCV3 genome clusters and geographic origin.

---

### Q18: Why does statistical association between cluster and country NOT imply geographical causation or origin?
**Answer**:  
Association indicates that certain genetic clusters are sampled more frequently in specific regions. However, this may result from sampling bias (e.g. 117 samples from China vs 1 from Sweden), regional sequencing efforts, or unobserved trade patterns. It does not prove that a specific country originated or mutated the virus.

---

### Q19: How was the temporal (year of collection) association evaluated?
**Answer**:  
We grouped collection years into 4 temporal bins (`Early <2015`, `Mid-Early 2015–2017`, `Mid-Late 2018–2020`, `Late 2021–2025`) to prevent sparse cell counts per individual year. Chi-square permutation testing yielded $p = 0.0002$ and Cramér's V = 0.3114, confirming moderate-to-strong temporal structure.

---

### Q20: What is IQ-TREE 3 and what advantage does ModelFinder provide?
**Answer**:  
IQ-TREE 3 is a state-of-the-art Maximum Likelihood (ML) phylogenetic software. ModelFinder (`-m MFP`) tests hundreds of nucleotide substitution models (such as GTR, HKY, TIM, TVM with gamma rate heterogeneity $+G$ and invariant sites $+I$) and selects the optimal model using the Bayesian Information Criterion (BIC). For our dataset, `GTR+F+I+G4` was selected.

---

### Q21: What is Ultra-fast Bootstrap (UFBoot) support in phylogenetics?
**Answer**:  
Bootstrap support assesses clade reliability by resampling alignment columns with replacement. Ultra-fast Bootstrap (`-B 1000`) uses candidate tree space approximations to compute unbiased branch support values across 1,000 replicates. Values $\ge 95\%$ indicate strong clade support.

---

### Q22: What is nucleotide $p$-distance and how was the genetic distance matrix computed?
**Answer**:  
Pairwise $p$-distance is the proportion of nucleotide sites at which two aligned sequences differ:
$$p = \frac{n_{\text{differences}}}{n_{\text{compared valid sites}}}$$
Across representative PCV3 genomes, mean pairwise genetic distance was 0.0117 (1.17% mean divergence, maximum 4.89%), confirming high sequence conservation across global isolates.

---

### Q23: How do the phylogenetic tree topology, PCA, and K-Means clusters integrate?
**Answer**:  
The three approaches provide complementary perspectives:
- PCA shows continuous genetic ordination in two dimensions.
- K-Means partitions the principal components into 7 statistical clusters.
- IQ-TREE Maximum Likelihood tree shows evolutionary branching structure, which was **broadly consistent with the K-Means genomic clustering patterns**.

---

### Q24: What are the primary limitations of this study?
**Answer**:  
1. **Sampling Imbalance**: Heavy sampling in China (117), USA (69), Spain (57), and South Korea (51) compared to single isolates from Sweden or Mexico.
2. **Temporal Gaps**: Earlier years (<2015) have sparse representation compared to 2017 (151 isolates).
3. **Metadata Inconsistencies**: 16 records in Excel had conflicting regions (e.g. Spain vs Poland) and 10 were absent from Excel.
4. **Non-Inference of Function**: Sequence variations cannot be linked to viral virulence or clinical severity without animal challenge data.

---

### Q25: What are the key conclusions of the project?
**Answer**:  
1. PCV3 exhibits a conserved 2,000 bp genome (1.17% mean nucleotide divergence) with 890 variable sites (466 parsimony-informative).
2. Unsupervised PCA and K-Means clustering on pure SNP features reveal 7 distinct genomic subgroups.
3. Genome clusters exhibit strong statistical association with geography ($V=0.4185, p=0.0002$) and temporal periods ($V=0.3114, p=0.0002$).
4. Maximum Likelihood phylogenetics reveals evolutionary branching that is broadly consistent with genomic clustering without supporting unsupported causal transmission claims.
