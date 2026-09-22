import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os

from utils.styles import apply_custom_styles, render_header
from utils.data_loader import load_master_data, load_snp_summary, render_sidebar_filters

st.set_page_config(page_title="PCV3 Analytics | Variation & PCA", page_icon="🧬", layout="wide")
apply_custom_styles()

render_header(
    "02 — Genome Variation & Dimensionality Reduction",
    "Aligned Site Composition, Genomic Variant Density, and Unsupervised Principal Component Analysis (PCA)"
)

# Load data & filters
df_master = load_master_data()
df_snp_summary = load_snp_summary()
df_filtered, color_mode = render_sidebar_filters(df_master)

# KPI Cards
c1, c2, c3, c4, c5 = st.columns(5)

with c1:
    st.metric("Alignment Length", "2,156 bp")
with c2:
    st.metric("Conserved Sites", "1,266 bp", delta="58.72% of genome", delta_color="normal")
with c3:
    st.metric("Variable Sites", "890 bp", delta="41.28% of genome", delta_color="normal")
with c4:
    st.metric("Parsimony-Informative", "466 bp", delta="21.61% of genome", delta_color="normal")
with c5:
    st.metric("One-Hot SNP Features", "2,067", help="Binary encoded non-constant nucleotide states")

st.markdown("---")

# Row 1: MSA Site Composition & SNP Density Plot
col_a, col_b = st.columns(2)

with col_a:
    st.subheader("Alignment Site Composition")
    site_df = pd.DataFrame({
        'Category': ['Conserved Sites', 'Variable (Singleton)', 'Parsimony-Informative'],
        'Count': [1266, 424, 466]
    })
    fig_sites = px.pie(
        site_df,
        names="Category",
        values="Count",
        hole=0.4,
        title="Genomic Alignment Site Classification (2,156 bp Total)",
        color_discrete_sequence=["#2ecc71", "#f39c12", "#e74c3c"]
    )
    fig_sites.update_layout(template="plotly_white", height=380)
    st.plotly_chart(fig_sites, use_container_width=True)

with col_b:
    st.subheader("Genome-Wide Variant Density (50 bp Sliding Window)")
    if not df_snp_summary.empty:
        align_len = 2156
        window_size = 50
        bins = range(0, align_len, window_size)
        snp_counts = [0] * len(bins)
        
        for pos in df_snp_summary['alignment_position']:
            idx = int((pos - 1) // window_size)
            if idx < len(snp_counts):
                snp_counts[idx] += 1
                
        df_density = pd.DataFrame({'Position_bp': list(bins), 'SNP_Count': snp_counts})
        
        fig_density = px.line(
            df_density,
            x="Position_bp",
            y="SNP_Count",
            title="Polymorphic Site Density across PCV3 Coordinates",
            labels={"Position_bp": "Genomic Position (bp)", "SNP_Count": "SNPs / 50 bp"},
            markers=True,
            color_discrete_sequence=["#8e44ad"]
        )
        fig_density.update_layout(template="plotly_white", height=380)
        st.plotly_chart(fig_density, use_container_width=True)

# Row 2: PCA Explained Variance & Interactive PCA Scatter
col_c, col_d = st.columns([2, 3])

with col_c:
    st.subheader("PCA Explained Variance Ratio")
    pca_vars = [22.37, 15.65, 8.42, 6.12, 4.85, 3.91, 3.25, 2.74, 2.31, 1.98]
    cum_vars = np.cumsum(pca_vars)
    df_var = pd.DataFrame({
        'PC': [f"PC{i+1}" for i in range(10)],
        'Individual_Variance': pca_vars,
        'Cumulative_Variance': cum_vars
    })
    
    fig_pca_var = go.Figure()
    fig_pca_var.add_trace(go.Bar(x=df_var['PC'], y=df_var['Individual_Variance'], name="Individual %", marker_color="#2980b9"))
    fig_pca_var.add_trace(go.Scatter(x=df_var['PC'], y=df_var['Cumulative_Variance'], name="Cumulative %", mode="lines+markers", line=dict(color="#e74c3c", width=2)))
    fig_pca_var.update_layout(
        title="PCA Variance Ratio (PC1 = 22.37%, PC2 = 15.65%)",
        xaxis_title="Principal Component",
        yaxis_title="Percentage of Variance Explained (%)",
        template="plotly_white",
        height=450,
        legend=dict(x=0.05, y=0.95)
    )
    st.plotly_chart(fig_pca_var, use_container_width=True)

with col_d:
    st.subheader(f"Interactive PCA Scatter Plot (Colored by {color_mode})")
    color_col = 'country' if color_mode == 'Country' else ('year' if color_mode == 'Year' else 'cluster')
    
    palette_seq = px.colors.qualitative.Set1 if color_mode == "Cluster" else px.colors.qualitative.D3
    
    fig_pca_scatter = px.scatter(
        df_filtered,
        x="PC1",
        y="PC2",
        color=color_col,
        symbol="cluster" if color_mode != "Cluster" else None,
        hover_data=["seq_id", "accession", "country", "year", "cluster", "PC1", "PC2"],
        title=f"PC1 (22.37%) vs PC2 (15.65%) — Color Attribute: {color_mode}",
        labels={"PC1": "PC1 (22.37% Variance)", "PC2": "PC2 (15.65% Variance)"},
        color_discrete_sequence=palette_seq
    )
    fig_pca_scatter.update_traces(marker=dict(size=8, opacity=0.85))
    fig_pca_scatter.update_layout(template="plotly_white", height=450)
    st.plotly_chart(fig_pca_scatter, use_container_width=True)

st.markdown("""
    <div class="info-box">
        <strong>🔒 Zero Metadata Leakage Guarantee:</strong> 
        The input feature matrix was derived exclusively from one-hot binary encoded nucleotide sequence variations at the 890 variable positions (2,067 binary SNP features). 
        Geographical location (Country), Region, and Collection Year were strictly <strong>excluded</strong> from PCA matrix calculations. 
        Metadata variables are projected onto PCA space post-hoc for visual and statistical interpretation only.
    </div>
""", unsafe_allow_html=True)
