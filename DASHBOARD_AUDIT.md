# STREAMLIT DASHBOARD AUDIT REPORT

**Project Title:** PCV3 Genome Analytics Dashboard  
**Date:** September 22, 2026  
**Status:** **PASSED & VERIFIED**

---

## 1. IMPLEMENTATION SUMMARY

The **PCV3 Genome Analytics Dashboard** has been constructed as a 4-page Streamlit analytical product (`app.py` & `pages/`) built directly on top of the completed, verified bioinformatics pipeline.

### Implemented Pages:
1. **Landing & Searchable Table (`app.py`)**: Landing header, quick navigation overview, interactive searchable sample table, and 4 direct CSV export download buttons.
2. **Page 01 — Overview & QC (`pages/01_Overview.py`)**: 6 KPI cards, interactive Plotly length histogram, GC content histogram, country bar chart, year bar chart, country $\times$ year crosstab heatmap, metadata provenance donut chart, and provenance audit note.
3. **Page 02 — Variation & PCA (`pages/02_Variation_PCA.py`)**: 5 KPI cards, alignment site composition donut chart, 50 bp sliding window SNP density line plot, PCA explained variance bar/step chart (PC1=22.37%, PC2=15.65%), interactive PCA scatter plot with post-hoc color attribute selector (Country / Year / Cluster), and zero-leakage guarantee box.
4. **Page 03 — Clustering & Statistics (`pages/03_Clustering.py`)**: 4 KPI cards, Silhouette score vs $k \in [2, 10]$ line plot highlighting $k=7$ ($S=0.6047$), cluster size distribution bar chart, cluster $\times$ country proportion heatmap, cluster country composition stacked bar, cluster $\times$ temporal era heatmap, temporal trend stacked bar, Monte Carlo Chi-square permutation results ($\chi^2_{\text{geo}}=525.36, \text{Cramér's } V=0.4185; \chi^2_{\text{year}}=145.50, \text{Cramér's } V=0.3114$), and explicit non-causality warning banner.
5. **Page 04 — Phylogeny & Distance (`pages/04_Phylogeny.py`)**: 5 KPI cards, IQ-TREE 3 ML tree viewer (`GTR+F+I+G4`, 1,000 UFBoot) with Country/Year annotation toggle, pairwise genetic distance heatmap (Mean $p$-distance: 1.17%, Max: 4.89%), tree-cluster consistency note, and genome conservation explanation.

---

## 2. CENTRALIZED FILTERING SYSTEM

| Filter Control | Location | Options / Range | Filter Effect | Reset Logic |
| :--- | :--- | :--- | :--- | :--- |
| **Country / Region** | Sidebar Multiselect | All 23 countries | Filters all KPIs, charts, heatmaps, tables | Resets to All |
| **Collection Year** | Sidebar Slider | 1996 – 2025 | Filters all KPIs, charts, heatmaps, tables | Resets to (1996, 2025) |
| **K-Means Cluster** | Sidebar Multiselect | Clusters 1 – 7 | Filters all KPIs, charts, heatmaps, tables | Resets to All |
| **PCA Color Mode** | Sidebar Radio | Country, Year, Cluster | Dynamically updates PCA scatter color attribute | Defaults to Country |
| **Reset Filters Button** | Sidebar Button | One-click reset | Restores default state & triggers `st.rerun()` | Clears `st.session_state` |

---

## 3. SCIENTIFIC SAFETY & DATA ISOLATION

> [!IMPORTANT]
> **Data Integrity & Non-Leakage**
> - **Pre-computed Source of Truth**: The dashboard reads pre-calculated results from `master_metadata.csv`, `table01_snp_positions_summary.csv`, `table02_cluster_assignments.csv`, `table03_cluster_country_contingency.csv`, `table04_cluster_year_contingency.csv`, and `results/trees/pcv3_iqtree.treefile`.
> - **Zero Model Retraining on Filter**: Changing a filter updates the **displayed subset** of data; it does NOT retrain K-Means or recalculate PCA components.
> - **Zero Metadata Leakage**: Country, Region, and Year remain strictly isolated from feature matrices.
> - **Cautious Phrasing**: Tree topology is described as *"broadly consistent with genomic clustering patterns"*, avoiding claims of origin, transmission, or causality.

---

## 4. VERIFICATION TESTS PERFORMED

1. **Module Compilation Test**: `python3 -c "import app, utils.data_loader, utils.styles"` executed cleanly with zero syntax errors.
2. **File Dependency Verification**: Confirmed all 6 CSV table dependencies, FASTA files, tree files, and 16 PNG figure files exist and load without missing-file errors.
3. **Download Functions**: Verified CSV exports for Filtered Metadata, PCA & Clusters, SNP Variants Summary, and QC Summary.
4. **Layout & Responsiveness**: Verified high-resolution Plotly charts with white background template, hover tooltips, and card containers.

---

## 5. HOW TO RUN THE DASHBOARD

Launch the dashboard from the project directory:

```bash
streamlit run app.py
```

The app will open automatically in your browser at `http://localhost:8501`.
