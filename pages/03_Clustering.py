import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os

from utils.styles import apply_custom_styles, render_header
from utils.data_loader import load_master_data, load_contingency_tables, render_sidebar_filters

st.set_page_config(page_title="PCV3 Analytics | Clustering & Statistics", page_icon="🧬", layout="wide")
apply_custom_styles()

render_header(
    "03 — Genomic Clustering & Epidemiological Patterns",
    "Unsupervised K-Means Clustering, Silhouette Evaluation, and Spatiotemporal Permutation Tests"
)

# Load data & filters
df_master = load_master_data()
ct_geo, ct_year = load_contingency_tables()
df_filtered, color_mode = render_sidebar_filters(df_master)

# KPI Cards
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric("Selected Cluster Count (k)", "7", help="Optimal configuration selected via Silhouette score")
with c2:
    st.metric("Silhouette Coefficient", "0.6047", help="Measures intra-cluster compactness vs inter-cluster separation")
with c3:
    st.metric("Geographic Cramér's V", "0.4185", delta="p = 0.0002 (Permutation)", delta_color="normal")
with c4:
    st.metric("Temporal Cramér's V", "0.3114", delta="p = 0.0002 (Permutation)", delta_color="normal")

st.markdown("---")

# Section A: Clustering Evaluation & Size Distribution
st.markdown("### 🧩 Section A — Unsupervised K-Means Clustering (k=7)")

col_a, col_b = st.columns(2)

with col_a:
    st.subheader("Silhouette Score vs Cluster Count (k=2..10)")
    ks = list(range(2, 11))
    scores = [0.4183, 0.4441, 0.4805, 0.5155, 0.5979, 0.6047, 0.5826, 0.5911, 0.5837]
    df_sil = pd.DataFrame({'k': ks, 'Silhouette_Score': scores})
    
    fig_sil = px.line(
        df_sil,
        x="k",
        y="Silhouette_Score",
        markers=True,
        title="Mean Silhouette Coefficient vs k",
        labels={"k": "Number of Clusters (k)", "Silhouette_Score": "Silhouette Score"}
    )
    fig_sil.add_vline(x=7, line_dash="dash", line_color="red", annotation_text="Selected k=7 (Score: 0.6047)")
    fig_sil.update_traces(line_color="#27ae60", marker=dict(size=8))
    fig_sil.update_layout(template="plotly_white", height=380)
    st.plotly_chart(fig_sil, use_container_width=True)

with col_b:
    st.subheader("Genome Cluster Size Distribution")
    cluster_counts = df_filtered['cluster'].value_counts().reset_index()
    cluster_counts.columns = ['Cluster', 'Count']
    cluster_counts = cluster_counts.sort_values('Cluster')
    
    fig_cls = px.bar(
        cluster_counts,
        x="Cluster",
        y="Count",
        title="Genomes per K-Means Cluster (Filtered Dataset)",
        color="Cluster",
        color_discrete_sequence=px.colors.qualitative.Set1
    )
    fig_cls.update_layout(template="plotly_white", height=380)
    st.plotly_chart(fig_cls, use_container_width=True)

# Row 2: Cluster x Country Heatmap & Stacked Composition Bar
col_c, col_d = st.columns(2)

with col_c:
    st.subheader("Cluster × Country Proportion Heatmap (%)")
    top_countries = df_filtered['country'].value_counts().head(8).index
    df_filtered_geo = df_filtered.copy()
    df_filtered_geo['country_grouped'] = df_filtered_geo['country'].apply(lambda c: c if c in top_countries else 'Other')
    
    ct_c = pd.crosstab(df_filtered_geo['cluster'], df_filtered_geo['country_grouped'])
    prop_c = ct_c.div(ct_c.sum(axis=0), axis=1) * 100
    
    fig_heatmap_c = px.imshow(
        prop_c,
        labels=dict(x="Country / Region", y="Cluster", color="Proportion (%)"),
        x=prop_c.columns,
        y=prop_c.index,
        color_continuous_scale="YlGnBu",
        title="Cluster Proportion within Country (%)"
    )
    fig_heatmap_c.update_layout(template="plotly_white", height=420)
    st.plotly_chart(fig_heatmap_c, use_container_width=True)

with col_d:
    st.subheader("Country Composition within Clusters")
    df_comp = df_filtered_geo.groupby(['cluster', 'country_grouped']).size().reset_index(name='Count')
    fig_comp = px.bar(
        df_comp,
        x="cluster",
        y="Count",
        color="country_grouped",
        title="Geographic Breakdown per K-Means Cluster",
        labels={"cluster": "PCV3 Cluster", "Count": "Number of Genomes", "country_grouped": "Country"}
    )
    fig_comp.update_layout(template="plotly_white", height=420, barmode="stack")
    st.plotly_chart(fig_comp, use_container_width=True)

st.markdown("---")

# Section B: Temporal Association Analysis
st.markdown("### ⏳ Section B — Temporal (Collection Year) Association")

col_e, col_f = st.columns(2)

with col_e:
    st.subheader("Cluster × Temporal Era Proportion Heatmap (%)")
    ct_y = pd.crosstab(df_filtered['cluster'], df_filtered['year_bin'])
    year_bin_order = ['Early (<2015)', 'Mid-Early (2015-2017)', 'Mid-Late (2018-2020)', 'Late (2021-2025)']
    existing_bins = [b for b in year_bin_order if b in ct_y.columns]
    ct_y = ct_y[existing_bins]
    prop_y = ct_y.div(ct_y.sum(axis=0), axis=1) * 100
    
    fig_heatmap_y = px.imshow(
        prop_y,
        labels=dict(x="Temporal Era", y="Cluster", color="Proportion (%)"),
        x=prop_y.columns,
        y=prop_y.index,
        color_continuous_scale="Purples",
        title="Cluster Proportion within Temporal Era (%)"
    )
    fig_heatmap_y.update_layout(template="plotly_white", height=420)
    st.plotly_chart(fig_heatmap_y, use_container_width=True)

with col_f:
    st.subheader("Temporal Distribution of Clusters Over Eras")
    df_temp = df_filtered.groupby(['year_bin', 'cluster']).size().reset_index(name='Count')
    fig_temp = px.bar(
        df_temp,
        x="year_bin",
        y="Count",
        color="cluster",
        title="Cluster Frequency Shift Over Collection Eras",
        labels={"year_bin": "Temporal Era", "Count": "Genome Count"},
        color_discrete_sequence=px.colors.qualitative.Set1
    )
    fig_temp.update_layout(template="plotly_white", height=420, barmode="stack")
    st.plotly_chart(fig_temp, use_container_width=True)

st.markdown("---")

# Section C: Statistical Interpretation & Non-Causality Warnings
st.markdown("### 📊 Section C — Rigorous Statistical Independence Tests")

col_stat1, col_stat2 = st.columns(2)

with col_stat1:
    st.markdown("""
        <div class="kpi-card">
            <h4 style="color:#1b365d; margin-top:0;">Geographical Statistical Association</h4>
            <ul>
                <li><strong>Chi-square Statistic (χ²):</strong> <code>525.36</code> (dof = 48)</li>
                <li><strong>Asymptotic p-value:</strong> <code>1.56e-81</code></li>
                <li><strong>Monte Carlo Permutation p-value (5,000 perms):</strong> <code>p = 0.0002</code></li>
                <li><strong>Cramér's V Association Index:</strong> <code>0.4185</code> (Strong association)</li>
                <li><strong>Diagnostics:</strong> 50.8% of contingency cells had expected counts &lt; 5. Label permutation test confirms robust statistical significance despite sparse cell counts.</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

with col_stat2:
    st.markdown("""
        <div class="kpi-card">
            <h4 style="color:#1b365d; margin-top:0;">Temporal Statistical Association</h4>
            <ul>
                <li><strong>Chi-square Statistic (χ²):</strong> <code>145.50</code> (dof = 18)</li>
                <li><strong>Asymptotic p-value:</strong> <code>5.54e-22</code></li>
                <li><strong>Monte Carlo Permutation p-value (5,000 perms):</strong> <code>p = 0.0002</code></li>
                <li><strong>Cramér's V Association Index:</strong> <code>0.3114</code> (Moderate-to-strong association)</li>
                <li><strong>Diagnostics:</strong> Temporal binning prevents single-year cell sparsity. Permutation testing confirms significant temporal cluster shifting.</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

st.markdown("""
    <div class="caution-box">
        <strong>⚠️ SCIENTIFIC INTERPRETATION & NON-CAUSALITY WARNING:</strong><br>
        Observed PCV3 genomic clusters exhibit statistically significant association with geographic origin (Cramér's V = 0.4185, p = 0.0002) 
        and temporal collection era (Cramér's V = 0.3114, p = 0.0002).<br>
        <strong>Crucial Caution:</strong> Statistical association does <strong>NOT</strong> prove geographical transmission routes, viral origin, or causal evolutionary divergence. 
        Observed patterns may reflect sampling biases (e.g. 117 samples from China vs 1 from Sweden) and regional sequencing efforts rather than viral transmission dynamics.
    </div>
""", unsafe_allow_html=True)
