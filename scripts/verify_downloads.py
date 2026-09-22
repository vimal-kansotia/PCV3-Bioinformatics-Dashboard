import os
import pandas as pd
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

base_dir = BASE_DIR

files_to_check = {
    'Filtered Metadata CSV': os.path.join(base_dir, 'data/processed/master_metadata.csv'),
    'PCA & Clusters CSV': os.path.join(base_dir, 'results/tables/table02_cluster_assignments.csv'),
    'SNP Variants Summary CSV': os.path.join(base_dir, 'results/tables/table01_snp_positions_summary.csv'),
    'QC Summary CSV': os.path.join(base_dir, 'results/tables/table00_qc_summary.csv'),
    'Geographic Contingency CSV': os.path.join(base_dir, 'results/tables/table03_cluster_country_contingency.csv'),
    'Temporal Contingency CSV': os.path.join(base_dir, 'results/tables/table04_cluster_year_contingency.csv')
}

print("="*60)
print("VERIFYING ALL DASHBOARD DOWNLOAD FILES")
print("="*60)

for name, fpath in files_to_check.items():
    if not os.path.exists(fpath):
        print(f"❌ FAIL: {name} file missing at {fpath}")
    else:
        df = pd.read_csv(fpath)
        size_bytes = os.path.getsize(fpath)
        print(f"✅ PASS: {name} | Size: {size_bytes:,} bytes | Rows: {len(df)} | Columns: {len(df.columns)}")

print("="*60)
