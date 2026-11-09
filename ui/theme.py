import streamlit as st

def apply_theme():
    """Applies comprehensive Premium SaaS dark theme CSS overrides with smooth animations, larger sidebar, and fluid transitions."""
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

        /* Global App Background & Font */
        .stApp {
            background-color: #090D0C !important;
            color: #F9FAFB !important;
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
            animation: fadeIn 0.4s ease-out;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(6px); }
            to { opacity: 1; transform: translateY(0); }
        }

        /* Main Content Area */
        .main .block-container {
            background-color: #090D0C !important;
            padding-top: 2rem;
            padding-bottom: 2rem;
            animation: fadeIn 0.4s ease-out;
        }

        /* Expanded Sidebar & Navigation Styling */
        section[data-testid="stSidebar"] {
            background-color: #090D0C !important;
            border-right: 1px solid rgba(16, 185, 129, 0.25) !important;
            min-width: 300px !important;
            width: 300px !important;
        }
        section[data-testid="stSidebar"] > div {
            height: 100% !important;
        }
        section[data-testid="stSidebar"] .block-container {
            background-color: #090D0C !important;
            padding-left: 1.5rem !important;
            padding-right: 1.5rem !important;
            padding-top: 1.5rem !important;
            padding-bottom: 1.5rem !important;
            display: flex !important;
            flex-direction: column !important;
            height: 100% !important;
            box-sizing: border-box !important;
        }
        section[data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
            display: flex !important;
            flex-direction: column !important;
            flex: 1 !important;
        }
        section[data-testid="stSidebar"] [data-testid="stVerticalBlock"] > div:last-child {
            margin-top: auto !important;
        }
        section[data-testid="stSidebar"] [data-testid="stDivider"],
        section[data-testid="stSidebar"] hr {
            margin: 0.6rem 0 !important;
        }
        section[data-testid="stSidebar"] h3 {
            font-size: 1.15rem !important;
            margin-top: 0.2rem !important;
            margin-bottom: 0.4rem !important;
            color: #F9FAFB !important;
            letter-spacing: 0.3px !important;
        }
        section[data-testid="stSidebar"] [data-testid="stRadio"] div[role="radiogroup"] {
            gap: 0.35rem !important;
        }
        section[data-testid="stSidebar"] [data-testid="stRadio"] label {
            background-color: transparent !important;
            border-radius: 8px !important;
            padding: 0.6rem 0.8rem !important;
            transition: all 0.2s ease !important;
            cursor: pointer !important;
            border: 1px solid transparent !important;
        }
        section[data-testid="stSidebar"] [data-testid="stRadio"] label:hover {
            background-color: rgba(34, 197, 94, 0.08) !important;
            border-color: rgba(34, 197, 94, 0.15) !important;
        }
        section[data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked) {
            background-color: rgba(34, 197, 94, 0.15) !important;
            border-color: rgba(34, 197, 94, 0.35) !important;
        }
        section[data-testid="stSidebar"] [data-testid="stRadio"] label p,
        section[data-testid="stSidebar"] [data-testid="stRadio"] label span {
            font-size: 1.08rem !important;
            font-weight: 500 !important;
        }

        /* Cards, Containers & Expanders with smooth hover lift */
        [data-testid="stVerticalBlockBorderWrapper"],
        [data-testid="stExpander"],
        div.stContainer {
            border: 1px solid rgba(16, 185, 129, 0.25) !important;
            border-radius: 10px !important;
            background-color: #111816 !important;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3) !important;
            transition: transform 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease !important;
        }
        [data-testid="stVerticalBlockBorderWrapper"]:hover,
        [data-testid="stExpander"]:hover {
            border-color: rgba(16, 185, 129, 0.5) !important;
            transform: translateY(-2px);
            box-shadow: 0 6px 16px rgba(16, 185, 129, 0.15) !important;
        }

        /* Form Inputs */
        input, select, textarea, [data-baseweb="select"] div, [data-baseweb="input"] div {
            background-color: #202B26 !important;
            color: #F9FAFB !important;
            border-color: rgba(16, 185, 129, 0.3) !important;
            border-radius: 6px !important;
            transition: all 0.2s ease !important;
        }
        input:focus, select:focus, textarea:focus {
            border-color: #10B981 !important;
            box-shadow: 0 0 0 2px rgba(16, 185, 129, 0.25) !important;
        }

        /* Buttons with fluid transitions */
        .stButton > button {
            background-color: #111816 !important;
            color: #F9FAFB !important;
            border: 1px solid rgba(16, 185, 129, 0.4) !important;
            border-radius: 8px !important;
            font-weight: 600 !important;
            transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
        }
        .stButton > button:hover {
            background-color: #202B26 !important;
            border-color: #10B981 !important;
            color: #10B981 !important;
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(16, 185, 129, 0.25) !important;
        }
        button[kind="primary"] {
            background-color: #10B981 !important;
            color: #090D0C !important;
            border: none !important;
            font-weight: 700 !important;
        }
        button[kind="primary"]:hover {
            background-color: #059669 !important;
            color: #FFFFFF !important;
            transform: translateY(-1px);
            box-shadow: 0 4px 14px rgba(16, 185, 129, 0.4) !important;
        }

        /* Metric Widgets */
        [data-testid="stMetric"] {
            background-color: #111816 !important;
            border: 1px solid rgba(16, 185, 129, 0.25) !important;
            padding: 12px 16px !important;
            border-radius: 8px !important;
            transition: transform 0.2s ease;
        }
        [data-testid="stMetric"]:hover {
            transform: translateY(-2px);
            border-color: rgba(16, 185, 129, 0.5) !important;
        }
        [data-testid="stMetricLabel"] {
            color: #9CA3AF !important;
            font-size: 0.85rem !important;
            text-transform: uppercase !important;
            letter-spacing: 0.5px !important;
        }
        [data-testid="stMetricValue"] {
            color: #10B981 !important;
            font-size: 1.75rem !important;
            font-weight: 700 !important;
        }

        /* Custom Plate Box */
        .plate-box {
            font-family: 'Courier New', monospace;
            background-color: #202B26;
            color: #10B981;
            padding: 6px 12px;
            border: 1px solid #10B981;
            border-radius: 6px;
            font-weight: bold;
            display: inline-block;
            letter-spacing: 1.5px;
            transition: transform 0.2s ease;
        }
        .plate-box:hover {
            transform: scale(1.03);
        }

        /* Metric Card Component */
        .metric-card {
            background: linear-gradient(135deg, #111816, #202B26);
            border: 1px solid rgba(16, 185, 129, 0.3);
            border-radius: 12px;
            padding: 20px;
            text-align: center;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2);
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }
        .metric-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 20px rgba(16, 185, 129, 0.2);
        }
        .metric-value {
            font-size: 2rem;
            font-weight: 700;
            color: #10B981;
            margin-top: 6px;
        }
        .metric-label {
            font-size: 0.85rem;
            color: #9CA3AF;
            text-transform: uppercase;
            letter-spacing: 0.8px;
            font-weight: 600;
        }

        /* Empty State */
        .empty-state {
            text-align: center;
            padding: 50px 20px;
            color: #9CA3AF;
            background: #111816;
            border: 1px dashed rgba(16, 185, 129, 0.3);
            border-radius: 10px;
            margin: 20px 0;
            animation: fadeIn 0.5s ease-out;
        }

        /* Pulsing indicator */
        @keyframes pulse-glow {
            0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7); }
            70% { transform: scale(1); box-shadow: 0 0 0 8px rgba(16, 185, 129, 0); }
            100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
        }
        .pulse-badge {
            display: inline-block;
            width: 10px;
            height: 10px;
            border-radius: 50%;
            background: #10B981;
            box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7);
            animation: pulse-glow 2s infinite;
            margin-right: 6px;
        }

        /* Headers and Titles */
        h1, h2, h3, h4, h5, h6 {
            color: #F9FAFB !important;
            font-weight: 700 !important;
        }
        p, span, label {
            color: #D1D5DB !important;
        }
    </style>
    """, unsafe_allow_html=True)

def render_status_badge(status):
    """Renders a styled HTML status badge with premium SaaS palette and pulse effect for active."""
    status_str = str(status or "ativa").strip().lower()
    color_map = {
        "ativa": "#10B981",
        "cancelada": "#EF4444",
        "concluída": "#6B7280",
        "concluida": "#6B7280",
        "livre": "#10B981",
        "ocupada": "#F59E0B"
    }
    color = color_map.get(status_str, "#6B7280")
    pulse = '<span class="pulse-badge"></span>' if status_str == "ativa" else ""
    return f"<span style='background-color:{color}; color:#090D0C; padding:4px 12px; border-radius:14px; font-size:0.75rem; font-weight:700; text-transform:uppercase; letter-spacing:0.5px; display:inline-flex; align-items:center;'>{pulse}{status_str}</span>"

def render_metric_card(label, value, icon="📊"):
    """Renders a compact metric card with icon and hover animation."""
    st.markdown(f"""
    <div class="metric-card">
        <div style="font-size: 1.6rem; margin-bottom: 4px;">{icon}</div>
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
    </div>
    """, unsafe_allow_html=True)

def render_plate(plate):
    """Renders a formatted vehicle license plate badge with hover effect."""
    clean_plate = str(plate or "---").upper()
    return f'<span class="plate-box">🚗 {clean_plate}</span>'

def render_empty_state(message, icon="📭"):
    """Renders a styled empty state container with fade-in animation."""
    st.markdown(f"""
    <div class="empty-state">
        <div style="font-size: 3rem; margin-bottom: 12px; animation: fadeIn 0.6s ease;">{icon}</div>
        <div style="font-size: 1.05rem; color: #F9FAFB; font-weight: 500;">{message}</div>
    </div>
    """, unsafe_allow_html=True)
