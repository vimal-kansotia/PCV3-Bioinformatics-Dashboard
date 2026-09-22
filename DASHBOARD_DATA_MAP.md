# DASHBOARD DATA SOURCE MAP

This document maps every metric, KPI, chart, table, and visualization in the Streamlit PCV3 Analytics Dashboard to its source file, columns, and data transformation logic.

---

## 1. Page 01 — Dataset Overview & Quality Control

| Dashboard Component | Metric / Chart Type | Primary Source File | Columns Used | Transformation / Aggregation |
| :--- | :--- | :--- | :--- | :--- |
| **KPI: Total Genomes** | Count | `data/processed/master_metadata.csv` | `seq_id` | `len(filtered_df)` |
| **KPI: Mean Genome Length** | Mean (bp) | `data/processed/master_metadata.csv` | `sequence_length` | `filtered_df['sequence_length'].mean()` |
| **KPI: Mean GC Content** | Percentage (%) | `data/processed/master_metadata.csv` | `gc_content` | `filtered_df['gc_content'].mean()` |
| **KPI: Variable Sites** | Count | `results/tables/table01_snp_positions_summary.csv` | `alignment_position` | Fixed 890 sites |
| **KPI: Unique Countries** | Count | `data/processed/master_metadata.csv` | `country` | `filtered_df['country'].nunique()` |
| **KPI: Year Range** | Min - Max Year | `data/processed/master_metadata.csv` | `year` | `min(year) - max(year)` |
| **Chart: Length Distribution** | Interactive Histogram | `data/processed/master_metadata.csv` | `sequence_length` | Plotly histogram with mean line |
| **Chart: GC Distribution** | Interactive Box/Hist | `data/processed/master_metadata.csv` | `gc_content` | Plotly histogram with mean line |
| **Chart: Country Distribution** | Bar Chart | `data/processed/master_metadata.csv` | `country` | Value counts of `country` |
| **Chart: Year Distribution** | Bar/Line Chart | `data/processed/master_metadata.csv` | `year` | Value counts of `year` sorted by year |
| **Chart: Country x Year Heatmap**| Heatmap | `data/processed/master_metadata.csv` | `country`, `year` | `pd.crosstab(country, year)` |
| **Chart: Data Provenance** | Donut Chart | `data/processed/master_metadata.csv` | `metadata_provenance` | Value counts (Excel_Verified: 474, Conflict: 16, Header: 10) |

---

## 2. Page 02 — Genome Variation & Dimensionality Reduction

| Dashboard Component | Metric / Chart Type | Primary Source File | Columns Used | Transformation / Aggregation |
| :--- | :--- | :--- | :--- | :--- |
| **KPI: Alignment Length** | bp | `data/processed/aligned_sequences.fasta` | Sequence string length | Fixed 2,156 bp |
| **KPI: Conserved Sites** | Count & % | `results/tables/table01_snp_positions_summary.csv` | Alignment length - 890 | Fixed 1,266 bp (58.72%) |
| **KPI: Variable Sites** | Count & % | `results/tables/table01_snp_positions_summary.csv` | `alignment_position` | Fixed 890 bp (41.28%) |
| **KPI: Parsimony-Informative**| Count & % | `results/tables/table01_snp_positions_summary.csv` | `is_parsimony_informative` | Fixed 466 bp (21.61%) |
| **KPI: One-Hot SNP Features**| Count | `data/processed/snp_feature_matrix.csv` | Feature columns | Fixed 2,067 binary features |
| **Chart: Site Proportions** | Donut Chart | Pre-calculated site metrics | Site categories | Conserved (1266), Variable (424), Informative (466) |
| **Chart: SNP Density** | Sliding Window Line Plot | `results/tables/table01_snp_positions_summary.csv` | `alignment_position` | 50 bp sliding window density |
| **Chart: PCA Variance Ratio** | Bar & Step Line | Pre-calculated PCA variances | PC components | PC1: 22.37%, PC2: 15.65%, Cum: 38.02% |
| **Chart: Interactive PCA Scatter**| Scatter Plot | `results/tables/table02_cluster_assignments.csv` | `PC1`, `PC2`, `country`, `year`, `cluster` | Plotly scatter colored dynamically by Country / Year / Cluster |

---

## 3. Page 03 — Genomic Clustering & Epidemiological Patterns

| Dashboard Component | Metric / Chart Type | Primary Source File | Columns Used | Transformation / Aggregation |
| :--- | :--- | :--- | :--- | :--- |
| **KPI: Selected k** | Count | K-Means model evaluation | Cluster count | Fixed k = 7 |
| **KPI: Silhouette Score** | Score | K-Means model evaluation | Silhouette coefficient | Fixed 0.6047 |
| **KPI: Geographic Cramér's V**| Statistic | `results/tables/table03_cluster_country_contingency.csv` | Contingency matrix | Fixed 0.4185 (p = 0.0002) |
| **KPI: Temporal Cramér's V** | Statistic | `results/tables/table04_cluster_year_contingency.csv` | Contingency matrix | Fixed 0.3114 (p = 0.0002) |
| **Chart: Silhouette vs k** | Line Chart | Model evaluation values | k = 2..10, scores | Plotly line chart highlighting k=7 |
| **Chart: Cluster Sizes** | Bar Chart | `results/tables/table02_cluster_assignments.csv` | `cluster` | Cluster size distribution |
| **Chart: Cluster x Country Heatmap**| Heatmap | `results/tables/table03_cluster_country_contingency.csv` | `cluster`, `country` | Crosstab proportion heatmap |
| **Chart: Country Composition** | Stacked Bar Chart | `results/tables/table02_cluster_assignments.csv` | `cluster`, `country` | Proportion within cluster |
| **Chart: Cluster x Era Heatmap** | Heatmap | `results/tables/table04_cluster_year_contingency.csv` | `cluster`, `year_bin` | Crosstab proportion heatmap |
| **Chart: Temporal Cluster Trend**| Stacked Bar Chart | `results/tables/table02_cluster_assignments.csv` | `cluster`, `year_bin` | Proportion within temporal era |

---

## 4. Page 04 — Phylogenetic Structure & Genetic Diversity

| Dashboard Component | Metric / Chart Type | Primary Source File | Columns Used | Transformation / Aggregation |
| :--- | :--- | :--- | :--- | :--- |
| **KPI: ML Tree Method** | Text | IQ-TREE 3 ModelFinder | Model string | Fixed `GTR+F+I+G4` |
| **KPI: UFBoot Replicates** | Count | IQ-TREE 3 execution log | Replicate count | Fixed 1,000 UFBoot |
| **KPI: Mean p-Distance** | Divergence (%) | Alignment matrix calculation | Pairwise differences | Fixed 0.0117 (1.17%) |
| **KPI: Max p-Distance** | Divergence (%) | Alignment matrix calculation | Pairwise differences | Fixed 0.0489 (4.89%) |
| **Chart: ML Phylogenetic Tree** | Interactive/Image Tree | `results/trees/pcv3_iqtree.treefile` | Newick tree topology | Parsed via Biopython Phylo / Rendered tree |
| **Chart: Distance Heatmap** | Interactive Heatmap | Representative 100x100 matrix | Pairwise p-distances | Subsampled 100 representative genomes heatmap |

---

## 5. Sample Table & File Export Data Sources

| Feature | Primary Source File | Export File Format |
| :--- | :--- | :--- |
| **Interactive Sample Table** | `data/processed/master_metadata.csv` & `table02_cluster_assignments.csv` | Filtered dataframe display with search & sort |
| **Filtered Metadata CSV** | Filtered master metadata | CSV download button |
| **PCA Coordinates CSV** | `results/tables/table02_cluster_assignments.csv` | CSV download button |
| **Cluster Assignments CSV** | `results/tables/table02_cluster_assignments.csv` | CSV download button |
| **Summary Statistics CSV** | `results/tables/table00_qc_summary.csv` | CSV download button |
