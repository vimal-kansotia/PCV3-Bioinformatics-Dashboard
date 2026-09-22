import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import os
from PIL import Image

from utils.styles import apply_custom_styles, render_header
from utils.data_loader import load_master_data, render_sidebar_filters

st.set_page_config(page_title="PCV3 Analytics | Phylogeny & Distance", page_icon="🧬", layout="wide")
apply_custom_styles()

render_header(
    "04 — Phylogenetic Structure & Genetic Diversity",
    "IQ-TREE 3 Maximum Likelihood Tree Reconstruction, ModelFinder Selection, and Pairwise Genetic Distance Analysis"
)

# Load data & filters
df_master = load_master_data()
df_filtered, color_mode = render_sidebar_filters(df_master)

# KPI Cards
c1, c2, c3, c4, c5 = st.columns(5)

with c1:
    st.metric("Phylogenetic Method", "Maximum Likelihood")
with c2:
    st.metric("Substitution Model", "GTR+F+I+G4", help="Selected by ModelFinder via BIC criterion")
with c3:
    st.metric("UFBoot Support", "1,000 Replicates", help="Ultra-fast Bootstrap support assessment")
with c4:
    st.metric("Mean p-Distance", "1.17%", delta="0.0117 subs / site", delta_color="normal")
with c5:
    st.metric("Max p-Distance", "4.89%", delta="0.0489 subs / site", delta_color="normal")

st.markdown("---")

# Section A: Phylogenetic Tree Visualizations
st.markdown("### 🌳 Section A — IQ-TREE 3 Maximum Likelihood Tree Topology")

tree_annotation = st.radio(
    "Select Tree Branch Color Annotation:",
    options=["Annotated by Country / Region", "Annotated by Collection Year"],
    horizontal=True
)

col_tree, col_tree_info = st.columns([3, 2])

fig_dir = '/Users/vimalkansotia/Downloads/Bioinformatics/results/figures'

with col_tree:
    if tree_annotation == "Annotated by Country / Region":
        img_path = os.path.join(fig_dir, 'fig14_phylo_tree_country.png')
        title_text = "Figure 14: ML Tree Colored by Country / Region"
    else:
        img_path = os.path.join(fig_dir, 'fig15_phylo_tree_year.png')
        title_text = "Figure 15: ML Tree Colored by Collection Year"
        
    if os.path.exists(img_path):
        image = Image.open(img_path)
        st.image(image, caption=title_text, use_container_width=True)
    else:
        st.warning("Phylogenetic tree image file not found.")

with col_tree_info:
    st.markdown("""
        <div class="kpi-card">
            <h4 style="color:#1b365d; margin-top:0;">Phylogenetic Model & Parameters</h4>
            <ul>
                <li><strong>Tree Building Tool:</strong> <code>IQ-TREE 3</code> (v3.1.4)</li>
                <li><strong>Model Selection:</strong> ModelFinder (evaluated 968 substitution models)</li>
                <li><strong>Selected Model:</strong> <code>GTR+F+I+G4</code> (General Time Reversible with empirical base frequencies + Invariable sites + 4 Gamma rate categories)</li>
                <li><strong>Selection Criterion:</strong> Bayesian Information Criterion (BIC)</li>
                <li><strong>Bootstrap Support:</strong> 1,000 Ultra-fast Bootstrap (UFBoot) replicates</li>
                <li><strong>Total Alignment Length:</strong> 2,156 bp across 500 complete genomes</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div class="info-box">
            <strong>🔬 Tree-Cluster Relationship Note:</strong><br>
            The phylogenetic tree structure was <strong>broadly consistent with the K-Means genomic clustering patterns</strong>. 
            Sequence isolates forming distinct K-Means clusters map to coherent clades on the ML tree topology.<br><br>
            <em>Scientific Caution: We do not state that the tree 'validates' or 'proves' the clusters, as no formal tree-vs-cluster concordance statistic (e.g. Robinson-Foulds distance or tanglegram alignment) was computed.</em>
        </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Section B: Pairwise Genetic Distance Analysis
st.markdown("### 🧬 Section B — Pairwise Genetic Distance & Genome Conservation")

col_dist_img, col_dist_text = st.columns([3, 2])

with col_dist_img:
    dist_img_path = os.path.join(fig_dir, 'fig16_genetic_distance_heatmap.png')
    if os.path.exists(dist_img_path):
        image_dist = Image.open(dist_img_path)
        st.image(image_dist, caption="Figure 16: Pairwise Genetic Distance Heatmap (N=100 Subsampled Genomes)", use_container_width=True)
    else:
        st.warning("Genetic distance heatmap image file not found.")

with col_dist_text:
    st.markdown("""
        <div class="kpi-card">
            <h4 style="color:#1b365d; margin-top:0;">Pairwise Distance Summary Metrics</h4>
            <ul>
                <li><strong>Mean Pairwise Distance:</strong> <code>0.0117</code> (1.17% mean nucleotide divergence)</li>
                <li><strong>Maximum Pairwise Distance:</strong> <code>0.0489</code> (4.89% maximum divergence)</li>
                <li><strong>Minimum Pairwise Distance:</strong> <code>0.0000</code> (100% identical sequence strings present in 27 isolates)</li>
                <li><strong>Alignment Base:</strong> 2,156 bp MAFFT alignment matrix</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div class="info-box">
            <strong>💡 Conservation Interpretation:</strong><br>
            A mean nucleotide divergence of 1.17% (max 4.89%) confirms high sequence conservation across global PCV3 isolates. 
            This low overall divergence is consistent with the alignment site composition (58.72% conserved positions) 
            and reflects typical single-stranded circular circovirus genomic stability.
        </div>
    """, unsafe_allow_html=True)
