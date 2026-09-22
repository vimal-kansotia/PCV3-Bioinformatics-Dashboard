import os
import pandas as pd
import numpy as np
import streamlit as st

@st.cache_data
def load_master_data():
    base_dir = '/Users/vimalkansotia/Downloads/Bioinformatics'
    master_path = os.path.join(base_dir, 'data/processed/master_metadata.csv')
    pca_cluster_path = os.path.join(base_dir, 'results/tables/table02_cluster_assignments.csv')
    
    df_master = pd.read_csv(master_path)
    
    if os.path.exists(pca_cluster_path):
        df_pca = pd.read_csv(pca_cluster_path)
        # Merge PC1 and PC2 if not already aligned
        if 'PC1' in df_pca.columns and 'PC2' in df_pca.columns:
            df_master['PC1'] = df_pca['PC1']
            df_master['PC2'] = df_pca['PC2']
            if 'cluster' in df_pca.columns:
                df_master['cluster'] = df_pca['cluster']

    # Assign default temporal bins
    def bin_year(y):
        if y < 2015:
            return 'Early (<2015)'
        elif 2015 <= y <= 2017:
            return 'Mid-Early (2015-2017)'
        elif 2018 <= y <= 2020:
            return 'Mid-Late (2018-2020)'
        else:
            return 'Late (2021-2025)'
            
    df_master['year_bin'] = df_master['year'].apply(bin_year)
    return df_master

@st.cache_data
def load_snp_summary():
    path = '/Users/vimalkansotia/Downloads/Bioinformatics/results/tables/table01_snp_positions_summary.csv'
    if os.path.exists(path):
        return pd.read_csv(path)
    return pd.DataFrame()

@st.cache_data
def load_contingency_tables():
    base_dir = '/Users/vimalkansotia/Downloads/Bioinformatics/results/tables'
    path_geo = os.path.join(base_dir, 'table03_cluster_country_contingency.csv')
    path_year = os.path.join(base_dir, 'table04_cluster_year_contingency.csv')
    
    ct_geo = pd.read_csv(path_geo, index_col=0) if os.path.exists(path_geo) else None
    ct_year = pd.read_csv(path_year, index_col=0) if os.path.exists(path_year) else None
    
    return ct_geo, ct_year

def render_sidebar_filters(df):
    st.sidebar.markdown("### 🎛️ Dataset Filters")
    
    # Reset filters button
    if st.sidebar.button("🔄 Reset All Filters", use_container_width=True):
        st.session_state['selected_countries'] = []
        st.session_state['selected_clusters'] = []
        st.session_state['year_range'] = (int(df['year'].min()), int(df['year'].max()))
        st.rerun()

    # Country Filter
    all_countries = sorted(df['country'].unique().tolist())
    selected_countries = st.sidebar.multiselect(
        "Country / Region",
        options=all_countries,
        default=st.session_state.get('selected_countries', []),
        placeholder="All Countries"
    )
    
    # Year Range Filter
    min_year = int(df['year'].min())
    max_year = int(df['year'].max())
    
    default_year_range = st.session_state.get('year_range', (min_year, max_year))
    year_range = st.sidebar.slider(
        "Collection Year Range",
        min_value=min_year,
        max_value=max_year,
        value=default_year_range
    )
    
    # Cluster Filter
    all_clusters = sorted(df['cluster'].dropna().unique().tolist())
    selected_clusters = st.sidebar.multiselect(
        "K-Means Cluster",
        options=all_clusters,
        default=st.session_state.get('selected_clusters', []),
        placeholder="All Clusters"
    )
    
    # PCA Color Mode Selector
    color_mode = st.sidebar.radio(
        "PCA Scatter Color Attribute",
        options=["Country", "Year", "Cluster"],
        index=0
    )
    
    # Apply Filtering
    df_filtered = df.copy()
    
    if selected_countries:
        df_filtered = df_filtered[df_filtered['country'].isin(selected_countries)]
        
    df_filtered = df_filtered[(df_filtered['year'] >= year_range[0]) & (df_filtered['year'] <= year_range[1])]
    
    if selected_clusters:
        df_filtered = df_filtered[df_filtered['cluster'].isin(selected_clusters)]

    st.sidebar.markdown("---")
    st.sidebar.markdown(f"**Filtered Genomes:** `{len(df_filtered)} / {len(df)}` ({len(df_filtered)/len(df)*100:.1f}%)")
    
    return df_filtered, color_mode
