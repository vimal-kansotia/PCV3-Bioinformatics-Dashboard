import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os

from utils.styles import apply_custom_styles, render_header
from utils.data_loader import load_master_data, render_sidebar_filters

st.set_page_config(page_title="PCV3 Analytics | Overview", page_icon="🧬", layout="wide")
apply_custom_styles()

render_header(
    "01 — Dataset Overview & Quality Control",
    "Comprehensive Sequence Quality Control, Provenance Audit, and Spatiotemporal Sampling Composition"
)

# Load data & filters
df_master = load_master_data()
df_filtered, color_mode = render_sidebar_filters(df_master)

# Top KPI Cards
c1, c2, c3, c4, c5, c6 = st.columns(6)

with c1:
    st.metric("Total Genomes", f"{len(df_filtered)}")
with c2:
    mean_len = df_filtered['sequence_length'].mean() if len(df_filtered) > 0 else 0
    st.metric("Mean Length", f"{mean_len:.2f} bp")
with c3:
    mean_gc = df_filtered['gc_content'].mean() if len(df_filtered) > 0 else 0
    st.metric("Mean GC Content", f"{mean_gc:.2f}%")
with c4:
    st.metric("Variable Sites", "890 bp", help="Polymorphic positions across alignment")
with c5:
    st.metric("Countries / Regions", f"{df_filtered['country'].nunique()}")
with c6:
    min_yr = int(df_filtered['year'].min()) if len(df_filtered) > 0 else 0
    max_yr = int(df_filtered['year'].max()) if len(df_filtered) > 0 else 0
    st.metric("Year Range", f"{min_yr} - {max_yr}")

st.markdown("---")

# Row 1: Quality Control Charts
col_a, col_b = st.columns(2)

with col_a:
    st.subheader("Genome Length Distribution (bp)")
    fig_len = px.histogram(
        df_filtered,
        x="sequence_length",
        nbins=15,
        title="PCV3 Sequence Length Histogram",
        labels={"sequence_length": "Sequence Length (bp)", "count": "Frequency"},
        color_discrete_sequence=["#2b5c8f"]
    )
    mean_len_val = df_filtered['sequence_length'].mean() if len(df_filtered) > 0 else 2000
    fig_len.add_vline(x=mean_len_val, line_dash="dash", line_color="red", annotation_text=f"Mean: {mean_len_val:.2f} bp")
    fig_len.update_layout(template="plotly_white", height=380)
    st.plotly_chart(fig_len, use_container_width=True)

with col_b:
    st.subheader("GC Content Distribution (%)")
    fig_gc = px.histogram(
        df_filtered,
        x="gc_content",
        nbins=20,
        title="PCV3 Genome GC Content (%)",
        labels={"gc_content": "GC Content (%)", "count": "Frequency"},
        color_discrete_sequence=["#27ae60"]
    )
    mean_gc_val = df_filtered['gc_content'].mean() if len(df_filtered) > 0 else 50.28
    fig_gc.add_vline(x=mean_gc_val, line_dash="dash", line_color="red", annotation_text=f"Mean: {mean_gc_val:.2f}%")
    fig_gc.update_layout(template="plotly_white", height=380)
    st.plotly_chart(fig_gc, use_container_width=True)

# Row 2: Metadata Distributions
col_c, col_d = st.columns(2)

with col_c:
    st.subheader("Sample Distribution by Country")
    cntry_counts = df_filtered['country'].value_counts().reset_index()
    cntry_counts.columns = ['Country', 'Count']
    fig_cntry = px.bar(
        cntry_counts,
        x="Count",
        y="Country",
        orientation="h",
        title="Sequences per Geographical Region",
        color="Count",
        color_continuous_scale="Viridis"
    )
    fig_cntry.update_layout(template="plotly_white", height=420, yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig_cntry, use_container_width=True)

with col_d:
    st.subheader("Sample Distribution by Collection Year")
    year_counts = df_filtered['year'].astype(int).value_counts().reset_index()
    year_counts.columns = ['Year', 'Count']
    year_counts = year_counts.sort_values('Year')
    fig_year = px.bar(
        year_counts,
        x="Year",
        y="Count",
        title="Sequences per Collection Year",
        color_discrete_sequence=["#3498db"]
    )
    fig_year.update_layout(template="plotly_white", height=420)
    st.plotly_chart(fig_year, use_container_width=True)

# Row 3: Heatmap & Data Provenance
col_e, col_f = st.columns([3, 2])

with col_e:
    st.subheader("Country × Collection Year Crosstabulation")
    ct_cy = pd.crosstab(df_filtered['country'], df_filtered['year'].astype(int))
    fig_heatmap = px.imshow(
        ct_cy,
        labels=dict(x="Collection Year", y="Country", color="Sequence Count"),
        x=ct_cy.columns.astype(str),
        y=ct_cy.index,
        color_continuous_scale="YlGnBu",
        title="Spatiotemporal Sample Sampling Heatmap"
    )
    fig_heatmap.update_layout(template="plotly_white", height=420)
    st.plotly_chart(fig_heatmap, use_container_width=True)

with col_f:
    st.subheader("Metadata Audit Provenance Summary")
    prov_counts = df_master['metadata_provenance'].value_counts().reset_index()
    prov_counts.columns = ['Provenance Category', 'Count']
    fig_prov = px.pie(
        prov_counts,
        names="Provenance Category",
        values="Count",
        hole=0.4,
        title="Metadata Verification Breakdown (N=500)",
        color_discrete_sequence=["#2ecc71", "#e74c3c", "#95a5a6"]
    )
    fig_prov.update_layout(template="plotly_white", height=420)
    st.plotly_chart(fig_prov, use_container_width=True)

st.markdown("""
    <div class="info-box">
        <strong>📌 Data Provenance Audit Note:</strong> 
        94.8% (474 records) of sample accessions were verified directly in the Excel metadata sheet without conflict. 
        16 records with conflicting geography between Excel and FASTA headers (e.g., Spain vs Poland) were explicitly tagged as 
        <code>Geography_Conflict_Excel</code>, and 10 records missing from Excel were recovered from FASTA headers (<code>FASTA_Header_Only</code>). 
        No metadata values were fabricated or silently altered.
    </div>
""", unsafe_allow_html=True)
