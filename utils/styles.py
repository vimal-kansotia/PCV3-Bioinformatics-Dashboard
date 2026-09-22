import streamlit as st

def apply_custom_styles():
    st.markdown("""
        <style>
        /* Modern Clean Scientific Styling */
        .main .block-container {
            padding-top: 1.5rem;
            padding-bottom: 2rem;
            padding-left: 2rem;
            padding-right: 2rem;
            max-width: 1400px;
        }

        /* Global Metric Card Overrides */
        div[data-testid="stMetric"] {
            background-color: #ffffff !important;
            padding: 12px 16px !important;
            border-radius: 8px !important;
            border: 1px solid #e2e8f0 !important;
            box-shadow: 0 1px 3px rgba(0,0,0,0.04) !important;
        }

        div[data-testid="stMetricValue"] {
            font-size: 24px !important;
            font-weight: 700 !important;
            color: #0f172a !important;
        }

        div[data-testid="stMetricLabel"] {
            font-size: 12px !important;
            font-weight: 600 !important;
            color: #475569 !important;
            text-transform: uppercase !important;
            letter-spacing: 0.5px !important;
        }

        /* Custom White Card Container */
        .kpi-card {
            background-color: #ffffff !important;
            border: 1px solid #cbd5e1 !important;
            border-radius: 10px !important;
            padding: 20px 24px !important;
            box-shadow: 0 2px 4px rgba(0,0,0,0.04) !important;
            margin-bottom: 20px !important;
            color: #1e293b !important;
        }

        .kpi-card h1, .kpi-card h2, .kpi-card h3, .kpi-card h4, .kpi-card h5, .kpi-card h6 {
            color: #0f172a !important;
            font-weight: 700 !important;
        }

        .kpi-card p, .kpi-card li, .kpi-card span, .kpi-card ul, .kpi-card div, .kpi-card td, .kpi-card th {
            color: #334155 !important;
            font-size: 14px !important;
            line-height: 1.6 !important;
        }

        .kpi-card strong {
            color: #0f172a !important;
            font-weight: 600 !important;
        }

        .kpi-card code {
            background-color: #f1f5f9 !important;
            color: #0f172a !important;
            padding: 2px 6px !important;
            border-radius: 4px !important;
        }

        /* Header Banner */
        .dashboard-header {
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%) !important;
            color: #ffffff !important;
            padding: 24px 28px !important;
            border-radius: 10px !important;
            margin-bottom: 25px !important;
            box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1) !important;
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
            background-color: #0284c7 !important;
            color: #ffffff !important;
            font-size: 11px !important;
            font-weight: 600 !important;
            padding: 4px 12px !important;
            border-radius: 20px !important;
            margin-top: 10px !important;
            letter-spacing: 0.5px !important;
        }

        /* Scientific Caution Banner */
        .caution-box {
            background-color: #fffbe6 !important;
            border-left: 4px solid #d97706 !important;
            padding: 16px 20px !important;
            border-radius: 6px !important;
            color: #78350f !important;
            font-size: 13px !important;
            margin-top: 15px !important;
            margin-bottom: 20px !important;
            line-height: 1.6 !important;
        }

        .caution-box p, .caution-box li, .caution-box span, .caution-box div, .caution-box strong, .caution-box em {
            color: #78350f !important;
        }

        /* Explanation Box */
        .info-box {
            background-color: #f0f9ff !important;
            border-left: 4px solid #0284c7 !important;
            padding: 16px 20px !important;
            border-radius: 6px !important;
            color: #0369a1 !important;
            font-size: 13px !important;
            margin-top: 15px !important;
            margin-bottom: 20px !important;
            line-height: 1.6 !important;
        }

        .info-box p, .info-box li, .info-box span, .info-box div, .info-box strong, .info-box em, .info-box code {
            color: #0369a1 !important;
        }

        .info-box code {
            background-color: #e0f2fe !important;
            padding: 2px 5px !important;
            border-radius: 4px !important;
        }

        /* Streamlit Sidebar Customization */
        section[data-testid="stSidebar"] {
            background-color: #f8fafc !important;
            border-right: 1px solid #e2e8f0 !important;
        }

        section[data-testid="stSidebar"] h1, 
        section[data-testid="stSidebar"] h2, 
        section[data-testid="stSidebar"] h3, 
        section[data-testid="stSidebar"] label,
        section[data-testid="stSidebar"] p,
        section[data-testid="stSidebar"] span {
            color: #1e293b !important;
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
