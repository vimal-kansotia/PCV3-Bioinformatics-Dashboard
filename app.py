import streamlit as st
import pandas as pd
import numpy as np
import os

from utils.styles import apply_custom_styles, render_header
from utils.data_loader import load_master_data, render_sidebar_filters
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

st.set_page_config(page_title="PCV3 Genome Analytics Dashboard", page_icon="🧬", layout="wide")
apply_custom_styles()

# Render Landing Header
render_header(
    "PCV3 Genome Analytics Dashboard",
    "Analysis of Genome Variation, Unsupervised Learning, Phylogenetics, and Geographic/Temporal Patterns in Porcine Circovirus 3"
)

# Load data & filters
df_master = load_master_data()
df_filtered, color_mode = render_sidebar_filters(df_master)

# Page Introduction Card
st.markdown("""
    <div class="kpi-card">
        <h3 style="color:#1b365d; margin-top:0;">👋 Welcome to the PCV3 Genome Analytics Dashboard</h3>
        <p>This portfolio-quality research dashboard provides interactive visual exploration of the completed <strong>Porcine Circovirus 3 (PCV3)</strong> 
        bioinformatics and unsupervised machine learning project (N=500 complete genomes).</p>
        <p>Use the <strong>Sidebar Navigation</strong> to explore the 4 analytical pages:</p>
        <ul>
            <li><strong>01 — Overview & QC:</strong> Genome length/GC distributions, country/year counts, and metadata provenance audit.</li>
            <li><strong>02 — Variation & PCA:</strong> Aligned site composition, SNP density, and interactive PCA scatter plot.</li>
            <li><strong>03 — Clustering & Statistics:</strong> K-Means silhouette evaluation (k=7), cluster heatmaps, and Chi-square permutation tests.</li>
            <li><strong>04 — Phylogeny & Distance:</strong> IQ-TREE 3 ML phylogenetic tree (GTR+F+I+G4) and pairwise genetic distance heatmap.</li>
        </ul>
    </div>
""", unsafe_allow_html=True)

st.markdown("---")

# Interactive Sample Table Section
st.subheader("🔍 Searchable & Filterable Sample Metadata Table")
st.markdown("This table reflects the active sidebar filter selection (Country, Year Range, Cluster). You can search, sort, and download the data below.")

search_query = st.text_input("🔍 Search by Accession, Country, or Cluster ID:", placeholder="e.g. PD363191.1, China, Cluster 6")

df_table = df_filtered[['seq_id', 'accession', 'country', 'year', 'cluster', 'PC1', 'PC2', 'sequence_length', 'gc_content', 'metadata_provenance']].copy()
df_table.columns = ['Sequence ID', 'Accession', 'Country', 'Year', 'Cluster', 'PC1', 'PC2', 'Length (bp)', 'GC Content (%)', 'Provenance']

if search_query:
    q = search_query.lower()
    df_table = df_table[
        df_table['Sequence ID'].astype(str).str.lower().str.contains(q) |
        df_table['Accession'].astype(str).str.lower().str.contains(q) |
        df_table['Country'].astype(str).str.lower().str.contains(q) |
        df_table['Cluster'].astype(str).str.lower().str.contains(q)
    ]

st.dataframe(
    df_table,
    use_container_width=True,
    height=350,
    column_config={
        "PC1": st.column_config.NumberColumn("PC1 (22.37%)", format="%.3f"),
        "PC2": st.column_config.NumberColumn("PC2 (15.65%)", format="%.3f"),
        "GC Content (%)": st.column_config.NumberColumn("GC Content (%)", format="%.2f")
    }
)

st.markdown("---")

# Downloads Section
st.subheader("📥 Export & Download Project Deliverables")

d_col1, d_col2, d_col3, d_col4 = st.columns(4)

with d_col1:
    csv_filtered = df_filtered.to_csv(index=False).encode('utf-8')
    st.download_button(
        "📄 Download Filtered Metadata CSV",
        data=csv_filtered,
        file_name="pcv3_filtered_metadata.csv",
        mime="text/csv",
        use_container_width=True
    )

with d_col2:
    pca_cluster_path = os.path.join(BASE_DIR, 'results/tables/table02_cluster_assignments.csv')
    if os.path.exists(pca_cluster_path):
        with open(pca_cluster_path, 'rb') as f:
            st.download_button(
                "📊 Download PCA & Clusters CSV",
                data=f.read(),
                file_name="pcv3_table02_cluster_assignments.csv",
                mime="text/csv",
                use_container_width=True
            )

with d_col3:
    snp_summary_path = os.path.join(BASE_DIR, 'results/tables/table01_snp_positions_summary.csv')
    if os.path.exists(snp_summary_path):
        with open(snp_summary_path, 'rb') as f:
            st.download_button(
                "🧬 Download SNP Variants Summary CSV",
                data=f.read(),
                file_name="pcv3_table01_snp_positions_summary.csv",
                mime="text/csv",
                use_container_width=True
            )

with d_col4:
    qc_summary_path = os.path.join(BASE_DIR, 'results/tables/table00_qc_summary.csv')
    if os.path.exists(qc_summary_path):
        with open(qc_summary_path, 'rb') as f:
            st.download_button(
                "📈 Download QC Summary CSV",
                data=f.read(),
                file_name="pcv3_table00_qc_summary.csv",
                mime="text/csv",
                use_container_width=True
            )

st.markdown("---")
st.markdown("""
    <div style="text-align: center; color: #64748b; font-size: 12px; margin-top: 20px;">
        PCV3 Genome Analytics Dashboard | MSc Big Data Analytics Practical Examination Project | Reproducible Streamlit & Biopython Pipeline
    </div>
""", unsafe_allow_html=True)
