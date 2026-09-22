import streamlit as st

def apply_custom_styles():
    st.markdown("""
        <style>
        /* Modern Dark Navy & Clean Scientific Styling */
        .main .block-container {
            padding-top: 1.5rem;
            padding-bottom: 2rem;
            padding-left: 2rem;
            padding-right: 2rem;
            max-width: 1400px;
        }
        
        /* Metric Card Styles */
        div[data-testid="stMetricValue"] {
            font-size: 24px !important;
            font-weight: 700 !important;
            color: #1b365d !important;
        }
        
        div[data-testid="stMetricLabel"] {
            font-size: 13px !important;
            font-weight: 600 !important;
            color: #4a5568 !important;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        /* Custom Card Container */
        .kpi-card {
            background-color: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            padding: 16px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
            margin-bottom: 15px;
        }
        
        /* Header Banner */
        .dashboard-header {
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
            color: white;
            padding: 24px;
            border-radius: 10px;
            margin-bottom: 25px;
            box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
        }
        
        .dashboard-header h1 {
            color: #ffffff !important;
            font-size: 28px !important;
            font-weight: 800 !important;
            margin: 0 !important;
        }
        
        .dashboard-header p {
            color: #94a3b8 !important;
            font-size: 14px !important;
            margin-top: 6px !important;
            margin-bottom: 0 !important;
        }
        
        .status-badge {
            display: inline-block;
            background-color: #0284c7;
            color: white;
            font-size: 11px;
            font-weight: 600;
            padding: 4px 10px;
            border-radius: 20px;
            margin-top: 10px;
            letter-spacing: 0.5px;
        }
        
        /* Scientific Caution Banner */
        .caution-box {
            background-color: #fffbebf5;
            border-left: 4px solid #d97706;
            padding: 14px 18px;
            border-radius: 6px;
            color: #92400e;
            font-size: 13px;
            margin-top: 15px;
            margin-bottom: 20px;
            line-height: 1.5;
        }
        
        /* Explanation Box */
        .info-box {
            background-color: #f0f9ff;
            border-left: 4px solid #0284c7;
            padding: 14px 18px;
            border-radius: 6px;
            color: #0369a1;
            font-size: 13px;
            margin-top: 15px;
            margin-bottom: 20px;
            line-height: 1.5;
        }
        
        /* Streamlit Sidebar Customization */
        section[data-testid="stSidebar"] {
            background-color: #f8fafc;
            border-right: 1px solid #e2e8f0;
        }
        </style>
    """, unsafe_allow_html=True)

def render_header(title, subtitle, badge_text="500 PCV3 genomes | MAFFT | PCA | K-Means | IQ-TREE"):
    st.markdown(f"""
        <div class="dashboard-header">
            <h1>{title}</h1>
            <p>{subtitle}</p>
            <div class="status-badge">{badge_text}</div>
        </div>
    """, unsafe_allow_html=True)
