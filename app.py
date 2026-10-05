"""
AI Dashboard Generator
-----------------------
A professional, production-grade Streamlit dashboard that transforms raw
business data (CSV/Excel) into meaningful KPIs, visualizations, AI-driven
insights, anomaly detection reports, and an interactive AI chat assistant.

Author: Senior Python / Streamlit Development Team
"""

import streamlit as st
import pandas as pd

from modules.data_loader import load_data
from modules.data_profiler import get_data_profile, get_column_info
from modules.data_cleaner import get_data_quality, clean_data
from modules.kpi_generator import generate_kpis
from modules.chart_generator import generate_charts
from modules.ai_insights import generate_insights
from modules.anomaly_detector import detect_anomalies
from modules.ai_assistant import create_dataset_context, ask_gemini
from modules.advanced_features import relationship_report, forecast, make_report_pdf, data_drilldown
from modules.chart_generator import smart_chart

# ==============================================================================
# PAGE CONFIGURATION
# ==============================================================================
st.set_page_config(
    page_title="AI Dashboard Generator",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ==============================================================================
# PREMIUM DARK THEME — CSS STYLING  (Linear / Stripe / Vercel inspired)
# ==============================================================================
def load_custom_css() -> None:
    """Inject premium dark SaaS-style CSS styling into the Streamlit app."""
    st.markdown(
        """
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
        <style>
            /* ==========================================================
               DESIGN TOKENS
               ========================================================== */
            :root {
                --bg-app: #08090C;
                --bg-app-2: #0C0D12;
                --bg-sidebar: #0A0B0F;
                --bg-card: #131417;
                --bg-card-hover: #16171C;
                --border-subtle: rgba(255, 255, 255, 0.08);
                --border-strong: rgba(255, 255, 255, 0.14);
                --accent: #6366F1;
                --accent-2: #8B5CF6;
                --accent-soft: rgba(99, 102, 241, 0.14);
                --success: #22C55E;
                --warning: #F59E0B;
                --danger: #F43F5E;
                --text-primary: #F5F5F7;
                --text-secondary: #9A9AA5;
                --text-tertiary: #6B6B76;
                --radius-lg: 20px;
                --radius-md: 14px;
                --radius-sm: 10px;
            }

            /* ==========================================================
               GLOBAL TYPOGRAPHY & BACKGROUND
               ========================================================== */
            html, body, [class*="css"] {
                font-family: 'Inter', 'Segoe UI', 'Helvetica Neue', Arial, sans-serif !important;
                -webkit-font-smoothing: antialiased;
            }

            .stApp {
                background:
                    radial-gradient(circle at 15% 0%, rgba(99, 102, 241, 0.10) 0%, transparent 45%),
                    radial-gradient(circle at 85% 15%, rgba(139, 92, 246, 0.08) 0%, transparent 40%),
                    var(--bg-app);
                color: var(--text-primary);
            }

            h1, h2, h3, h4, h5, h6 {
                color: var(--text-primary) !important;
                font-weight: 700;
                letter-spacing: -0.02em;
            }

            p, span, label, .stMarkdown {
                color: var(--text-secondary);
            }

            ::selection {
                background: var(--accent-soft);
                color: var(--text-primary);
            }

            /* Fade-in animation applied to freshly rendered sections */
            @keyframes fadeInUp {
                from { opacity: 0; transform: translateY(12px); }
                to { opacity: 1; transform: translateY(0); }
            }

            .block-container {
                padding-top: 2.2rem;
                padding-bottom: 4rem;
                max-width: 1280px;
                animation: fadeInUp 0.5s ease-out;
            }

            /* ==========================================================
               MAIN HEADER
               ========================================================== */
            .main-header {
                padding: 1.6rem 2.2rem;
                background: linear-gradient(135deg, rgba(19, 20, 23, 0.9) 0%, rgba(10, 11, 15, 0.9) 100%);
                border: 1px solid var(--border-subtle);
                border-radius: var(--radius-lg);
                margin-bottom: 2rem;
                box-shadow: 0 10px 40px rgba(0, 0, 0, 0.4);
                animation: fadeInUp 0.6s ease-out;
                position: relative;
                overflow: hidden;
                display: flex;
                align-items: center;
                justify-content: space-between;
                flex-wrap: wrap;
                gap: 1rem;
            }
            .main-header::before {
                content: "";
                position: absolute;
                top: -60%;
                right: -8%;
                width: 380px;
                height: 380px;
                background: radial-gradient(circle, var(--accent-soft) 0%, transparent 70%);
                pointer-events: none;
            }
            .main-header-brand {
                display: flex;
                align-items: center;
                gap: 0.9rem;
                position: relative;
                z-index: 1;
            }
            .main-header-logo {
                width: 44px;
                height: 44px;
                border-radius: 12px;
                background: linear-gradient(135deg, var(--accent) 0%, var(--accent-2) 100%);
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 1.3rem;
                box-shadow: 0 6px 18px rgba(99, 102, 241, 0.35);
                flex-shrink: 0;
            }
            .main-header h1 {
                color: #ffffff;
                font-size: 1.5rem;
                font-weight: 800;
                margin: 0;
                letter-spacing: -0.5px;
                line-height: 1.2;
            }
            .main-header p {
                color: var(--text-secondary);
                font-size: 0.88rem;
                font-weight: 400;
                margin: 0.15rem 0 0 0;
            }
            .main-header-badge {
                position: relative;
                z-index: 1;
                display: inline-flex;
                align-items: center;
                gap: 0.4rem;
                background: var(--accent-soft);
                border: 1px solid rgba(99, 102, 241, 0.3);
                color: #C7C9FF;
                font-size: 0.75rem;
                font-weight: 600;
                padding: 0.4rem 0.85rem;
                border-radius: 999px;
                white-space: nowrap;
            }

            /* ==========================================================
               HERO / LANDING SECTION (empty state)
               ========================================================== */
            .hero-wrap {
                text-align: center;
                padding: 3.2rem 1.5rem 2.4rem 1.5rem;
                animation: fadeInUp 0.6s ease-out;
            }
            .hero-badge {
                display: inline-flex;
                align-items: center;
                gap: 0.5rem;
                background: rgba(255, 255, 255, 0.04);
                border: 1px solid var(--border-subtle);
                color: var(--text-secondary);
                font-size: 0.8rem;
                font-weight: 600;
                padding: 0.45rem 1rem;
                border-radius: 999px;
                margin-bottom: 1.6rem;
            }
            .hero-badge .dot {
                width: 6px;
                height: 6px;
                border-radius: 50%;
                background: var(--success);
                box-shadow: 0 0 8px var(--success);
            }
            .hero-title {
                font-size: 3.1rem;
                font-weight: 900;
                line-height: 1.12;
                letter-spacing: -1.5px;
                color: var(--text-primary);
                max-width: 780px;
                margin: 0 auto 1.2rem auto;
            }
            .hero-title .gradient-text {
                background: linear-gradient(135deg, var(--accent) 0%, var(--accent-2) 60%, #EC4899 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
            }
            .hero-subtitle {
                font-size: 1.08rem;
                color: var(--text-secondary);
                max-width: 560px;
                margin: 0 auto 2.2rem auto;
                line-height: 1.6;
            }

            /* ==========================================================
               SECTION TITLES
               ========================================================== */
            .section-title {
                font-size: 1.15rem;
                font-weight: 700;
                color: var(--text-primary);
                margin-top: 2.4rem;
                margin-bottom: 1.1rem;
                padding-bottom: 0.7rem;
                border-bottom: 1px solid var(--border-subtle);
                display: flex;
                align-items: center;
                gap: 0.55rem;
                animation: fadeInUp 0.5s ease-out;
                letter-spacing: -0.3px;
            }

            /* ==========================================================
               KPI CARDS — GLASSMORPHISM + GRADIENT TOP BORDER
               ========================================================== */
            .kpi-card {
                position: relative;
                background: linear-gradient(180deg, var(--bg-card) 0%, var(--bg-app-2) 100%);
                backdrop-filter: blur(14px);
                -webkit-backdrop-filter: blur(14px);
                border-radius: var(--radius-md);
                padding: 1.4rem 1.3rem 1.2rem 1.3rem;
                border: 1px solid var(--border-subtle);
                box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
                text-align: left;
                overflow: hidden;
                transition: transform 0.22s ease, box-shadow 0.22s ease, border-color 0.22s ease;
                animation: fadeInUp 0.5s ease-out;
                height: 100%;
            }
            .kpi-card::before {
                content: "";
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                height: 3px;
                background: linear-gradient(90deg, var(--accent) 0%, var(--accent-2) 100%);
                opacity: 0.9;
            }
            .kpi-card:hover {
                transform: translateY(-4px);
                box-shadow: 0 14px 32px rgba(99, 102, 241, 0.16);
                border-color: var(--border-strong);
            }
            .kpi-icon {
                width: 34px;
                height: 34px;
                border-radius: 9px;
                background: var(--accent-soft);
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 1.05rem;
                margin-bottom: 0.9rem;
            }
            .kpi-label {
                font-size: 0.76rem;
                font-weight: 600;
                color: var(--text-secondary);
                text-transform: uppercase;
                letter-spacing: 0.6px;
                margin-bottom: 0.45rem;
            }
            .kpi-value {
                font-size: 1.85rem;
                font-weight: 800;
                color: var(--text-primary);
                letter-spacing: -0.6px;
            }
            .kpi-value.fraud {
                color: var(--danger);
            }
            .kpi-value.accent {
                color: #A5A6FF;
            }
            .kpi-value.success {
                color: var(--success);
            }

            /* ==========================================================
               AI INSIGHT CARDS
               ========================================================== */
            .insight-card {
                display: flex;
                align-items: flex-start;
                gap: 0.85rem;
                background: var(--bg-card);
                border: 1px solid var(--border-subtle);
                border-left: 3px solid var(--accent);
                border-radius: var(--radius-sm);
                padding: 1rem 1.2rem;
                margin-bottom: 0.75rem;
                box-shadow: 0 4px 14px rgba(0, 0, 0, 0.22);
                color: var(--text-primary);
                font-size: 0.95rem;
                line-height: 1.55;
                transition: transform 0.18s ease, box-shadow 0.18s ease, border-color 0.18s ease;
                animation: fadeInUp 0.5s ease-out;
            }
            .insight-card:hover {
                transform: translateX(4px);
                box-shadow: 0 6px 20px rgba(99, 102, 241, 0.14);
                border-color: var(--accent);
            }
            .insight-icon {
                font-size: 1.1rem;
                flex-shrink: 0;
                margin-top: 0.05rem;
            }
            .insight-text {
                flex: 1;
            }

            /* ==========================================================
               ANOMALY SUMMARY CARD
               ========================================================== */
            .anomaly-summary-card {
                position: relative;
                background: linear-gradient(135deg, rgba(244, 63, 94, 0.10) 0%, var(--bg-card) 65%);
                border: 1px solid rgba(244, 63, 94, 0.28);
                border-radius: var(--radius-md);
                padding: 1.5rem 1.6rem;
                box-shadow: 0 6px 22px rgba(244, 63, 94, 0.1);
                animation: fadeInUp 0.5s ease-out;
            }
            .anomaly-summary-label {
                font-size: 0.8rem;
                font-weight: 600;
                color: var(--text-secondary);
                text-transform: uppercase;
                letter-spacing: 0.6px;
                margin-bottom: 0.5rem;
            }
            .anomaly-summary-value {
                font-size: 2.4rem;
                font-weight: 900;
                color: var(--danger);
                letter-spacing: -1px;
                line-height: 1.1;
            }

            /* ==========================================================
               AI CHAT ASSISTANT
               ========================================================== */
            .ai-chat-card {
                background: var(--bg-card);
                border: 1px solid var(--border-subtle);
                border-radius: var(--radius-md);
                padding: 1.3rem 1.4rem;
                margin-bottom: 1.1rem;
                box-shadow: 0 6px 20px rgba(0, 0, 0, 0.22);
                animation: fadeInUp 0.5s ease-out;
            }
            .ai-response-card {
                display: flex;
                align-items: flex-start;
                gap: 0.9rem;
                background: var(--bg-card-hover);
                border: 1px solid var(--border-subtle);
                border-left: 3px solid var(--accent);
                border-radius: var(--radius-md);
                padding: 1.15rem 1.35rem;
                margin-top: 1rem;
                box-shadow: 0 6px 20px rgba(99, 102, 241, 0.1);
                color: var(--text-primary);
                font-size: 0.95rem;
                line-height: 1.6;
                animation: fadeInUp 0.4s ease-out;
            }
            .ai-response-icon {
                width: 32px;
                height: 32px;
                border-radius: 9px;
                background: linear-gradient(135deg, var(--accent) 0%, var(--accent-2) 100%);
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 1rem;
                flex-shrink: 0;
            }
            .ai-response-body {
                flex: 1;
            }
            .ai-response-label {
                font-size: 0.72rem;
                font-weight: 700;
                text-transform: uppercase;
                letter-spacing: 0.6px;
                color: #A5A6FF;
                margin-bottom: 0.4rem;
            }
            div[data-testid="stTextInput"] input {
                background: rgba(255, 255, 255, 0.03) !important;
                border: 1px solid var(--border-subtle) !important;
                border-radius: var(--radius-sm) !important;
                color: var(--text-primary) !important;
                padding: 0.6rem 0.9rem !important;
            }
            div[data-testid="stTextInput"] input:focus {
                border-color: var(--accent) !important;
                box-shadow: 0 0 0 3px var(--accent-soft) !important;
            }
            div[data-testid="stTextInput"] input::placeholder {
                color: var(--text-tertiary) !important;
            }

            /* ==========================================================
               PLACEHOLDER / FEATURE CARDS (Landing state)
               ========================================================== */
            .placeholder-card {
                background: var(--bg-card);
                border: 1px solid var(--border-subtle);
                border-radius: var(--radius-md);
                padding: 1.6rem 1.4rem;
                text-align: left;
                color: var(--text-secondary);
                transition: border-color 0.2s ease, transform 0.2s ease, background 0.2s ease;
                animation: fadeInUp 0.5s ease-out;
                height: 100%;
            }
            .placeholder-card:hover {
                border-color: var(--border-strong);
                transform: translateY(-4px);
                background: var(--bg-card-hover);
            }
            .placeholder-card .feature-icon {
                width: 38px;
                height: 38px;
                border-radius: 10px;
                background: var(--accent-soft);
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 1.1rem;
                margin-bottom: 0.9rem;
            }
            .placeholder-card h4 {
                color: var(--text-primary) !important;
                margin-bottom: 0.4rem;
                font-size: 1rem;
                font-weight: 700;
            }
            .placeholder-card p {
                font-size: 0.86rem;
                line-height: 1.5;
                margin: 0;
            }

            /* ==========================================================
               UPLOAD CTA CARD (landing state)
               ========================================================== */
            .upload-cta-card {
                max-width: 620px;
                margin: 0 auto 3rem auto;
                background: var(--bg-card);
                border: 1px solid var(--border-subtle);
                border-radius: var(--radius-lg);
                padding: 1.4rem 1.6rem;
                box-shadow: 0 10px 34px rgba(0, 0, 0, 0.3);
                animation: fadeInUp 0.6s ease-out;
            }
            .upload-cta-label {
                display: flex;
                align-items: center;
                gap: 0.5rem;
                font-size: 0.85rem;
                font-weight: 600;
                color: var(--text-secondary);
                margin-bottom: 0.7rem;
            }

            /* ==========================================================
               CHART CARD CONTAINER
               ========================================================== */
            .chart-card-title {
                font-size: 0.95rem;
                font-weight: 700;
                color: var(--text-primary);
                margin-bottom: 0.7rem;
                display: flex;
                align-items: center;
                gap: 0.5rem;
            }
            div[data-testid="stVerticalBlockBorderWrapper"] {
                border-radius: var(--radius-md) !important;
                border: 1px solid var(--border-subtle) !important;
                background: var(--bg-card) !important;
                box-shadow: 0 6px 20px rgba(0, 0, 0, 0.22) !important;
                padding: 0.5rem 0.3rem !important;
                margin-bottom: 1.3rem !important;
                transition: box-shadow 0.2s ease, border-color 0.2s ease;
                animation: fadeInUp 0.5s ease-out;
            }
            div[data-testid="stVerticalBlockBorderWrapper"]:hover {
                border-color: var(--border-strong) !important;
                box-shadow: 0 10px 26px rgba(99, 102, 241, 0.12) !important;
            }

            /* ==========================================================
               SIDEBAR
               ========================================================== */
            section[data-testid="stSidebar"] {
                background: var(--bg-sidebar);
                border-right: 1px solid var(--border-subtle);
            }
            section[data-testid="stSidebar"] * {
                color: var(--text-primary) !important;
            }
            section[data-testid="stSidebar"] .stCaption,
            section[data-testid="stSidebar"] small {
                color: var(--text-secondary) !important;
            }

            .sidebar-logo {
                display: flex;
                align-items: center;
                gap: 0.7rem;
                padding: 0.4rem 0.2rem 1.3rem 0.2rem;
                margin-bottom: 0.7rem;
                border-bottom: 1px solid var(--border-subtle);
            }
            .sidebar-logo-icon {
                width: 36px;
                height: 36px;
                border-radius: 10px;
                background: linear-gradient(135deg, var(--accent) 0%, var(--accent-2) 100%);
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 1.1rem;
                flex-shrink: 0;
                box-shadow: 0 4px 14px rgba(99, 102, 241, 0.3);
            }
            .sidebar-logo-text h3 {
                margin: 0;
                font-size: 1rem;
                font-weight: 800;
                color: var(--text-primary) !important;
                line-height: 1.2;
            }
            .sidebar-logo-text span {
                font-size: 0.7rem;
                color: var(--text-secondary) !important;
                letter-spacing: 0.4px;
                text-transform: uppercase;
            }

            .sidebar-section-label {
                font-size: 0.72rem;
                font-weight: 700;
                text-transform: uppercase;
                letter-spacing: 0.7px;
                color: var(--text-tertiary) !important;
                margin: 1.2rem 0 0.6rem 0;
            }

            section[data-testid="stSidebar"] .stRadio > label {
                font-weight: 600;
            }
            section[data-testid="stSidebar"] [role="radiogroup"] {
                gap: 0.25rem;
            }
            section[data-testid="stSidebar"] [role="radiogroup"] label {
                background: transparent;
                border: 1px solid transparent;
                border-radius: var(--radius-sm);
                padding: 0.55rem 0.7rem;
                margin-bottom: 0.15rem;
                transition: background 0.15s ease, border-color 0.15s ease;
            }
            section[data-testid="stSidebar"] [role="radiogroup"] label:hover {
                background: rgba(255, 255, 255, 0.04);
                border-color: var(--border-subtle);
            }
            section[data-testid="stSidebar"] [role="radiogroup"] label[data-checked="true"] {
                background: var(--accent-soft);
                border-color: rgba(99, 102, 241, 0.35);
            }

            section[data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] {
                background: rgba(99, 102, 241, 0.05);
                border: 1.5px dashed rgba(99, 102, 241, 0.4);
                border-radius: var(--radius-md);
                transition: border-color 0.2s ease, background 0.2s ease;
            }
            section[data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"]:hover {
                border-color: var(--accent);
                background: rgba(99, 102, 241, 0.09);
            }

            .sidebar-footer {
                margin-top: 2.6rem;
                padding-top: 1rem;
                border-top: 1px solid var(--border-subtle);
                font-size: 0.72rem;
                color: var(--text-tertiary) !important;
                text-align: center;
                line-height: 1.5;
            }

            /* ==========================================================
               DATAFRAME STYLING
               ========================================================== */
            .stDataFrame {
                border-radius: var(--radius-md);
                overflow: hidden;
                border: 1px solid var(--border-subtle);
                box-shadow: 0 4px 16px rgba(0, 0, 0, 0.22);
            }

            /* ==========================================================
               BUTTONS
               ========================================================== */
            .stButton > button {
                border-radius: var(--radius-sm);
                font-weight: 600;
                border: 1px solid var(--border-subtle);
                transition: transform 0.15s ease, box-shadow 0.15s ease, border-color 0.15s ease;
            }
            .stButton > button:hover {
                transform: translateY(-2px);
                box-shadow: 0 8px 20px rgba(99, 102, 241, 0.22);
                border-color: var(--border-strong);
            }
            .stButton > button[kind="primary"] {
                background: linear-gradient(135deg, var(--accent) 0%, var(--accent-2) 100%) !important;
                border: none !important;
                color: #ffffff !important;
                box-shadow: 0 6px 18px rgba(99, 102, 241, 0.3);
            }
            .stButton > button[kind="primary"]:hover {
                box-shadow: 0 10px 26px rgba(99, 102, 241, 0.42);
            }

            /* ==========================================================
               ALERTS (info / success / warning / error)
               ========================================================== */
            div[data-testid="stAlert"] {
                border-radius: var(--radius-sm);
                border: 1px solid var(--border-subtle);
            }

            /* ==========================================================
               EXPANDER
               ========================================================== */
            details {
                background: var(--bg-card);
                border: 1px solid var(--border-subtle) !important;
                border-radius: var(--radius-md) !important;
                overflow: hidden;
            }

            /* ==========================================================
               DIVIDER SPACING
               ========================================================== */
            hr {
                margin: 1.8rem 0;
                border-color: var(--border-subtle);
            }

            /* ==========================================================
               HIDE DEFAULT STREAMLIT CHROME
               (hamburger menu, Deploy button, footer, header bar, the
               red "running" status pill) — this is what makes a Streamlit
               app instantly look like a template instead of a product.
               ========================================================== */
            #MainMenu { visibility: hidden; }
            footer { visibility: hidden; }
            header[data-testid="stHeader"] {
                background: transparent;
                height: 0;
            }
            div[data-testid="stToolbar"] { visibility: hidden; height: 0; }
            div[data-testid="stDecoration"] { visibility: hidden; height: 0; }
            div[data-testid="stStatusWidget"] { visibility: hidden; }
            .stAppDeployButton { display: none !important; }
            div[data-testid="stAppViewBlockContainer"] { padding-top: 1.2rem; }

            /* ==========================================================
               CUSTOM SCROLLBAR
               ========================================================== */
            ::-webkit-scrollbar { width: 10px; height: 10px; }
            ::-webkit-scrollbar-track { background: transparent; }
            ::-webkit-scrollbar-thumb {
                background: rgba(255, 255, 255, 0.12);
                border-radius: 999px;
                border: 2px solid transparent;
                background-clip: padding-box;
            }
            ::-webkit-scrollbar-thumb:hover {
                background: rgba(99, 102, 241, 0.45);
                background-clip: padding-box;
            }

            /* ==========================================================
               TOGGLE SWITCH (Dark Mode)
               ========================================================== */
            div[data-testid="stCheckbox"] label[data-baseweb="checkbox"] div:first-child,
            label[data-baseweb="switch"] span,
            div[data-testid="stWidgetLabel"] p {
                color: var(--text-primary) !important;
            }
            div[role="switch"][aria-checked="true"] {
                background-color: var(--accent) !important;
            }

            /* ==========================================================
               MULTISELECT / SELECTBOX (Data Explorer column picker)
               ========================================================== */
            div[data-baseweb="select"] > div {
                background: var(--bg-card) !important;
                border: 1px solid var(--border-subtle) !important;
                border-radius: var(--radius-sm) !important;
                box-shadow: none !important;
            }
            div[data-baseweb="select"] > div:hover {
                border-color: var(--border-strong) !important;
            }
            div[data-baseweb="tag"] {
                background: var(--accent-soft) !important;
                border: 1px solid rgba(99, 102, 241, 0.35) !important;
                border-radius: 7px !important;
            }
            div[data-baseweb="tag"] span { color: #C7C9FF !important; }
            ul[data-testid="stSelectboxVirtualDropdown"],
            div[data-baseweb="popover"] ul {
                background: var(--bg-card-hover) !important;
                border: 1px solid var(--border-subtle) !important;
                border-radius: var(--radius-sm) !important;
            }

            /* ==========================================================
               DOWNLOAD BUTTON
               ========================================================== */
            div[data-testid="stDownloadButton"] > button {
                background: var(--bg-card) !important;
                border: 1px solid var(--border-subtle) !important;
                color: var(--text-primary) !important;
                font-weight: 600;
                border-radius: var(--radius-sm) !important;
                transition: border-color 0.2s ease, transform 0.15s ease;
            }
            div[data-testid="stDownloadButton"] > button:hover {
                border-color: var(--accent) !important;
                transform: translateY(-2px);
            }

            /* ==========================================================
               DATAFRAME HEADER ROW
               ========================================================== */
            div[data-testid="stDataFrame"] [role="columnheader"] {
                background: var(--bg-card-hover) !important;
                color: var(--text-secondary) !important;
                font-weight: 700 !important;
                font-size: 0.78rem !important;
                text-transform: uppercase;
                letter-spacing: 0.4px;
            }

            /* ==========================================================
               CAPTION TEXT
               ========================================================== */
            [data-testid="stCaptionContainer"] {
                color: var(--text-tertiary) !important;
                font-size: 0.85rem !important;
                margin-top: -0.6rem;
                margin-bottom: 0.6rem;
            }

            /* ==========================================================
               SUBTLE APP-WIDE VIGNETTE FOR DEPTH
               ========================================================== */
            .stApp::after {
                content: "";
                position: fixed;
                inset: 0;
                pointer-events: none;
                background: radial-gradient(ellipse at 50% 0%, transparent 55%, rgba(0,0,0,0.35) 100%);
                z-index: 0;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


# ==============================================================================
# REUSABLE UI COMPONENTS
# ==============================================================================
def render_kpi_card(label: str, value: str, style: str = "", icon: str = "📊") -> str:
    """Return HTML markup for a single premium glassmorphism KPI card."""
    value_class = f"kpi-value {style}".strip()
    return f"""
        <div class="kpi-card">
            <div class="kpi-icon">{icon}</div>
            <div class="kpi-label">{label}</div>
            <div class="{value_class}">{value}</div>
        </div>
    """


def render_trend_kpi_card(card: dict, good_direction: str = "up") -> str:
    """Return HTML markup for a premium KPI card with a real trend indicator.

    Built from a rich card dict (title/value/icon/trend/status/color) as
    produced by kpi_generator.generate_kpis()'s "cards" list. good_direction
    controls whether an "up" trend is shown as good (green) or bad (red) —
    e.g. "up" is good for Total Value, but bad for Fraud Rate.
    """
    title = card.get("title", "")
    value = card.get("value")
    icon = card.get("icon", "📊")
    color = card.get("color", "#6366F1")
    status = card.get("status", "neutral")
    trend = card.get("trend") or {}

    display_value = format_number(value) if value is not None else "N/A"
    if card.get("key") == "fraud_rate" and value is not None:
        display_value = f"{display_value}%"

    direction = trend.get("direction")
    delta = trend.get("delta")
    label = trend.get("label", "No previous period to compare")

    if direction in ("up", "down") and delta is not None:
        is_good = (direction == good_direction)
        trend_color = "#22C55E" if is_good else "#F43F5E"
        arrow = "↑" if direction == "up" else "↓"
        trend_html = (
            f'<span style="color:{trend_color};font-weight:700;">{arrow} {abs(delta):.1f}%</span> '
            f'<span style="color:var(--text-tertiary);">vs previous period</span>'
        )
    else:
        trend_html = f'<span style="color:var(--text-tertiary);font-size:0.72rem;">{label}</span>'

    value_color = color if status in ("critical", "warning") else "var(--text-primary)"

    return f"""
        <div class="kpi-card">
            <div class="kpi-icon" style="background:{color}22;color:{color};">{icon}</div>
            <div class="kpi-label">{title}</div>
            <div class="kpi-value" style="color:{value_color};">{display_value}</div>
            <div style="margin-top:0.55rem;font-size:0.78rem;">{trend_html}</div>
        </div>
    """


def render_placeholder_card(title: str, description: str) -> str:
    """Return HTML markup for a placeholder / feature card shown before data upload."""
    icon = title.split(" ", 1)[0] if title and title[0] not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ" else "✨"
    label = title.split(" ", 1)[1] if title and title[0] not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ" and " " in title else title
    return f"""
        <div class="placeholder-card">
            <div class="feature-icon">{icon}</div>
            <h4>{label}</h4>
            <p>{description}</p>
        </div>
    """


def render_insight_card(insight: str) -> str:
    """Return HTML markup for a single AI insight card with an icon."""
    return f"""
        <div class="insight-card">
            <div class="insight-icon">🤖</div>
            <div class="insight-text">{insight}</div>
        </div>
    """


def render_anomaly_summary_card(value: str) -> str:
    """Return HTML markup for the premium anomaly count summary card."""
    return f"""
        <div class="anomaly-summary-card">
            <div class="anomaly-summary-label">🚨 Total Anomalies Detected</div>
            <div class="anomaly-summary-value">{value}</div>
        </div>
    """


def render_ai_response_card(answer: str) -> str:
    """Return HTML markup for the AI Chat Assistant's response card."""
    return f"""
        <div class="ai-response-card">
            <div class="ai-response-icon">🤖</div>
            <div class="ai-response-body">
                <div class="ai-response-label">AI Response</div>
                {answer}
            </div>
        </div>
    """


def format_number(value) -> str:
    """Format numeric values with thousands separators for display."""
    try:
        return f"{float(value):,.2f}"
    except (ValueError, TypeError):
        return str(value)


def normalize_chart_items(charts) -> list:
    """Normalize the output of generate_charts() into a list of (title, fig) pairs.

    generate_charts(df) returns a list of tuples in the form:
        [("Histogram", fig1), ("Bar Chart", fig2), ...]

    This helper also tolerates a dict return value ({"title": fig, ...})
    for backward compatibility, without ever using enumerate() on a list
    of tuples (which would incorrectly pair an index with a whole tuple).
    """
    if not charts:
        return []

    if isinstance(charts, dict):
        return list(charts.items())

    # Assume it is already an iterable of (title, fig) tuples.
    return list(charts)


def render_chart_card(title: str, fig) -> None:
    """Render a single Plotly chart inside a modern rounded, shadowed card."""
    with st.container(border=True):
        st.markdown(f'<div class="chart-card-title">📈 {title}</div>', unsafe_allow_html=True)
        st.plotly_chart(fig, width="stretch")


# ==============================================================================
# MAIN HEADER
# ==============================================================================
def render_main_header() -> None:
    """Render the compact top app bar with brand and a live status badge."""
    st.markdown(
        """
        <div class="main-header">
            <div class="main-header-brand">
                <div class="main-header-logo">📊</div>
                <div>
                    <h1>AI Dashboard Generator</h1>
                    <p>Transform raw business data into meaningful insights and visualizations.</p>
                </div>
            </div>
            <div class="main-header-badge">
                <span style="color:#22C55E;">●</span> AI Engine Online
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ==============================================================================
# SIDEBAR NAVIGATION
# ==============================================================================
def render_sidebar():
    """Render the sidebar with logo, navigation, file uploader, and footer.

    Returns:
        tuple: (selected_page, uploaded_file)
    """
    with st.sidebar:
        # ------------------------------------------------------------
        # Logo / Brand Area
        # ------------------------------------------------------------
        st.markdown(
            """
            <div class="sidebar-logo">
                <div class="sidebar-logo-icon">◆</div>
                <div class="sidebar-logo-text">
                    <h3>AI Dashboard</h3>
                    <span>Generator</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # ------------------------------------------------------------
        # Navigation — matches the 8-page reference layout
        # ------------------------------------------------------------
        st.markdown('<div class="sidebar-section-label">Navigation</div>', unsafe_allow_html=True)
        nav_options = [
            "🏠 Overview",
            "🤖 AI Assistant",
            "📋 Dashboard",
            "📈 Visualizations",
            "💡 AI Insights",
            "🚨 Anomalies",
            "🗂️ Data Explorer",
            "🧠 AI Dashboard Studio",
            "⚙️ Settings",
        ]
        selected = st.radio(
            label="Select a page",
            options=nav_options,
            label_visibility="collapsed",
        )
        # Strip the emoji prefix so routing logic in main() stays plain text.
        page = selected.split(" ", 1)[1]

        # ------------------------------------------------------------
        # Upload Dataset
        # ------------------------------------------------------------
        st.markdown('<div class="sidebar-section-label">Upload Dataset</div>', unsafe_allow_html=True)
        uploaded_file = st.file_uploader(
            label="Upload a CSV or Excel file",
            type=["csv", "xlsx", "xls"],
            help="Supported formats: CSV, XLSX, XLS",
        )

        # ------------------------------------------------------------
        # Dark Mode Toggle
        # ------------------------------------------------------------
        st.markdown('<div class="sidebar-section-label">Appearance</div>', unsafe_allow_html=True)
        st.toggle("🌙 Dark Mode", value=True, key="dark_mode_toggle", disabled=True)

        # ------------------------------------------------------------
        # Footer
        # ------------------------------------------------------------
        st.markdown(
            """
            <div class="sidebar-footer">
                © 2026 AI Dashboard Generator<br>Internal Analytics Tool
            </div>
            """,
            unsafe_allow_html=True,
        )

    return page, uploaded_file


# ==============================================================================
# EMPTY STATE (NO DATA UPLOADED) — PREMIUM LANDING / HERO EXPERIENCE
# ==============================================================================
def render_empty_state() -> None:
    """Render a premium SaaS-style hero landing section and feature grid."""

    st.markdown(
        """
        <div class="hero-wrap">
            <div class="hero-badge"><span class="dot"></span> AI-Powered Analytics Platform</div>
            <div class="hero-title">
                Transform Raw Data into<br><span class="gradient-text">AI-Powered</span> Business Insights
            </div>
            <div class="hero-subtitle">
                Upload any CSV or Excel file and instantly generate KPIs, visualizations,
                anomaly detection, and an AI assistant that understands your data.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="upload-cta-card">
            <div class="upload-cta-label">⬆️ Upload your dataset to get started</div>
        """,
        unsafe_allow_html=True,
    )
    st.info("👆 Use the file uploader in the sidebar to select a CSV or Excel file.")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="section-title">✨ What You\'ll Get</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(
            render_placeholder_card("📈 Data Analysis", "Automatic profiling and quality checks of your dataset."),
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            render_placeholder_card("🎯 KPI Generation", "Key business metrics generated instantly from your data."),
            unsafe_allow_html=True,
        )
    with col3:
        st.markdown(
            render_placeholder_card("📊 Visualizations", "Rich, interactive charts to explore trends and patterns."),
            unsafe_allow_html=True,
        )

    col4, col5, col6 = st.columns(3)
    with col4:
        st.markdown(
            render_placeholder_card("🚨 Anomaly Detection", "Automatically surface outliers and suspicious patterns."),
            unsafe_allow_html=True,
        )
    with col5:
        st.markdown(
            render_placeholder_card("🤖 AI Assistant", "Chat with your data and get instant, context-aware answers."),
            unsafe_allow_html=True,
        )
    with col6:
        st.markdown(
            render_placeholder_card("🧹 Data Cleaning", "One-click cleanup for missing values and duplicate rows."),
            unsafe_allow_html=True,
        )


# ==============================================================================
# OVERVIEW PAGE — KPI row + curated charts (matches "Dashboard Overview")
# ==============================================================================
def render_overview_page(df: pd.DataFrame, kpis: dict) -> None:
    """Domain-independent overview. Never assumes fraud, transactions, or a specific industry."""
    st.markdown('<div class="section-title">📌 Dashboard Overview</div>', unsafe_allow_html=True)
    cards = kpis.get("cards", [])
    cols = st.columns(min(5, max(1, len(cards))))
    for i, card in enumerate(cards[:5]):
        with cols[i]:
            st.markdown(render_trend_kpi_card(card, "up"), unsafe_allow_html=True)

    st.markdown('<div class="section-title">🗃️ Dataset Preview</div>', unsafe_allow_html=True)
    with st.container(border=True):
        st.markdown(f'<div class="chart-card-title">Showing first 10 of {format_number(len(df))} rows</div>', unsafe_allow_html=True)
        st.dataframe(df.head(10), width="stretch")

    st.markdown('<div class="section-title">📊 AI-Generated Visualizations</div>', unsafe_allow_html=True)
    try:
        chart_items = normalize_chart_items(generate_charts(df))
        for i in range(0, len(chart_items), 2):
            c1, c2 = st.columns(2)
            if i < len(chart_items):
                with c1: render_chart_card(chart_items[i][0], chart_items[i][1])
            if i+1 < len(chart_items):
                with c2: render_chart_card(chart_items[i+1][0], chart_items[i+1][1])
        if not chart_items: st.info("No suitable charts were found for this dataset.")
    except Exception as error:
        st.error(f"Unable to generate charts: {error}")

    st.markdown('<div class="section-title">✨ Ask the Dashboard to Create a Chart</div>', unsafe_allow_html=True)
    q = st.text_input("Natural language chart request", placeholder="e.g. Show average CGPA by department", key="nl_chart_request")
    if st.button("✨ Create Visualization", type="primary", key="create_nl_chart") and q:
        try:
            # Deterministic execution from validated columns; Gemini is optional for the assistant.
            nums=df.select_dtypes(include="number").columns.tolist(); cats=df.select_dtypes(include=["object","category","bool"]).columns.tolist()
            ql=q.lower()
            metric=next((c for c in nums if str(c).lower() in ql), nums[0] if nums else None)
            dim=next((c for c in cats if str(c).lower() in ql), None)
            if dim is None and cats and any(x in ql for x in ["by","department","region","product","category","country"]): dim=cats[0]
            time_col=kpis.get("time_column")
            chart_type="line" if time_col and any(x in ql for x in ["trend","over time","monthly","daily"]) else "bar" if dim else "histogram"
            aggregation="average" if any(x in ql for x in ["average","avg","mean"]) else "sum"
            fig=smart_chart(df,metric=metric,dimension=dim,time_col=time_col,aggregation=aggregation,chart_type=chart_type)
            if fig is None: st.warning("I could not map that request to the available columns. Try naming a metric or dimension from the dataset.")
            else: render_chart_card("AI Requested Visualization", fig)
        except Exception as error:
            st.error(f"Unable to create the visualization: {error}")


# ==============================================================================
# DASHBOARD PAGE — data quality snapshot + column info + cleaning
# ==============================================================================
def render_dashboard_page(df: pd.DataFrame) -> None:
    """Render the Dashboard page: quality metrics, column info, and cleaning."""

    st.markdown('<div class="section-title">🧪 Data Quality Metrics</div>', unsafe_allow_html=True)
    try:
        quality = get_data_quality(df)
        rows = quality.get("rows", len(df))
        columns = quality.get("columns", len(df.columns))
        missing_values = quality.get("missing_values", int(df.isnull().sum().sum()))
        duplicate_rows = quality.get("duplicate_rows", int(df.duplicated().sum()))

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(render_kpi_card("Rows", format_number(rows), icon="📄"), unsafe_allow_html=True)
        with col2:
            st.markdown(render_kpi_card("Columns", format_number(columns), icon="🧱"), unsafe_allow_html=True)
        with col3:
            st.markdown(render_kpi_card("Missing Values", format_number(missing_values), "fraud", icon="❗"), unsafe_allow_html=True)
        with col4:
            st.markdown(render_kpi_card("Duplicate Rows", format_number(duplicate_rows), "fraud", icon="🧬"), unsafe_allow_html=True)
    except Exception as error:
        st.error(f"Unable to compute data quality metrics: {error}")

    st.markdown('<div class="section-title">🧭 Column Information</div>', unsafe_allow_html=True)
    try:
        column_info = get_column_info(df)
        with st.container(border=True):
            st.dataframe(column_info, width="stretch")
    except Exception as error:
        st.error(f"Unable to retrieve column information: {error}")

    st.markdown('<div class="section-title">🧹 Data Cleaning</div>', unsafe_allow_html=True)
    if st.button("🧹 Clean Dataset", type="primary"):
        try:
            cleaned_df = clean_data(df)
            st.session_state["cleaned_df"] = cleaned_df
            st.success("Dataset cleaned successfully.")
        except Exception as error:
            st.error(f"Unable to clean dataset: {error}")

    if "cleaned_df" in st.session_state:
        st.markdown("**Cleaned Dataset Preview**")
        with st.container(border=True):
            st.dataframe(st.session_state["cleaned_df"].head(10), width="stretch")


# ==============================================================================
# AI ASSISTANT PAGE — dedicated chat screen with quick-prompt chips
# ==============================================================================
def render_ai_assistant_page(df: pd.DataFrame) -> None:
    """Render a dedicated AI Chat Assistant page, styled like the reference chat panel."""

    st.markdown('<div class="section-title">🤖 AI Chat Assistant</div>', unsafe_allow_html=True)
    st.caption("Ask anything about your data")

    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []

    st.markdown('<div class="ai-chat-card">', unsafe_allow_html=True)

    clear_col, _ = st.columns([1, 5])
    with clear_col:
        if st.button("🗑️ Clear Chat", key="clear_ai_chat", width="stretch"):
            st.session_state["chat_history"] = []
            st.rerun()

    quick_prompts = [
        "Summarize this dataset",
        "Show transaction trends",
        "Detect anomalies",
        "Explain columns",
    ]
    chip_cols = st.columns(len(quick_prompts))
    picked_prompt = None
    for col, prompt in zip(chip_cols, quick_prompts):
        with col:
            if st.button(prompt, key=f"chip_{prompt}", width="stretch"):
                picked_prompt = prompt

    chat_col1, chat_col2 = st.columns([4, 1])
    with chat_col1:
        question = st.text_input(
            label="Ask a question about your dataset",
            placeholder="Type your question...",
            label_visibility="collapsed",
            key="ai_chat_question",
        )
    with chat_col2:
        ask_clicked = st.button("Ask AI ➔", type="primary", width="stretch")

    final_question = picked_prompt or (question if ask_clicked else None)

    if picked_prompt or ask_clicked:
        if not final_question or not final_question.strip():
            st.warning("⚠️ Please type a question before clicking 'Ask AI'.")
        else:
            try:
                answer = ask_gemini(
                    final_question,
                    st.session_state.get("dataset_context", {}),
                    st.session_state.get("chat_history", [])[-6:],
                )
                st.session_state["chat_history"].append((final_question, answer))
            except Exception as error:
                st.error(f"Unable to get a response from the AI Chat Assistant: {error}")

    for asked, answer in reversed(st.session_state["chat_history"]):
        st.markdown(f'<div class="chart-card-title">🧑 {asked}</div>', unsafe_allow_html=True)
        st.markdown(render_ai_response_card(answer), unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)


# ==============================================================================
# AI INSIGHTS PAGE
# ==============================================================================
def render_ai_insights_page(df: pd.DataFrame) -> None:
    """Render the AI Insights page: AI-generated insight cards."""

    st.markdown('<div class="section-title">💡 AI Generated Insights</div>', unsafe_allow_html=True)
    st.caption("Insights generated by AI based on your data")

    try:
        insights = generate_insights(df)
        if insights:
            for insight in insights:
                st.markdown(render_insight_card(insight), unsafe_allow_html=True)
        else:
            st.info("No insights could be generated for this dataset.")
    except Exception as error:
        st.error(f"Unable to generate AI insights: {error}")


# ==============================================================================
# ANOMALIES PAGE — unified, sortable anomaly table (Index/Amount/Score/Reason/Severity)
# ==============================================================================
def render_anomalies_page(df: pd.DataFrame) -> None:
    """Render the Anomalies page: a unified anomaly table across all numeric columns."""

    st.markdown('<div class="section-title">🚨 Anomaly Detection</div>', unsafe_allow_html=True)
    st.caption("Detected anomalies and suspicious patterns")

    try:
        anomalies = detect_anomalies(df)

        total_anomalies = 0
        combined_rows = []
        if isinstance(anomalies, dict):
            for column, outliers in anomalies.items():
                if outliers is None or outliers.empty:
                    continue
                total_anomalies += len(outliers)
                for idx, row in outliers.iterrows():
                    combined_rows.append({
                        "Index": idx,
                        "Column": column,
                        "Value": row.get(column),
                        "Anomaly Score": row.get("anomaly_score"),
                        "Reason": row.get("reason"),
                        "Severity": row.get("severity"),
                    })

        st.markdown(render_anomaly_summary_card(format_number(total_anomalies)), unsafe_allow_html=True)
        st.markdown("<div style='height: 0.6rem;'></div>", unsafe_allow_html=True)

        if combined_rows:
            anomaly_df = pd.DataFrame(combined_rows).sort_values(
                "Anomaly Score", ascending=False
            ).reset_index(drop=True)
            with st.container(border=True):
                st.dataframe(anomaly_df.head(50), width="stretch")

            with st.expander("🔍 View by column"):
                numeric_columns = df.select_dtypes(include="number").columns.tolist()
                for column in numeric_columns:
                    if column in anomalies and anomalies[column] is not None and len(anomalies[column]) > 0:
                        outliers = anomalies[column]
                        st.markdown(f"**{column}** ({len(outliers)} found)")
                        st.dataframe(outliers.head(20), width="stretch")
        else:
            st.info("No anomalies were detected in the numerical columns.")
    except Exception as error:
        st.error(f"Unable to run anomaly detection: {error}")


# ==============================================================================
# VISUALIZATIONS PAGE — every generated chart, displayed vertically
# ==============================================================================
def render_visualizations_page(df: pd.DataFrame) -> None:
    """Render the Visualizations page: every generated chart displayed vertically."""

    st.markdown('<div class="section-title">📊 Visualizations</div>', unsafe_allow_html=True)

    try:
        charts = generate_charts(df)
        chart_items = normalize_chart_items(charts)

        if chart_items:
            for title, fig in chart_items:
                render_chart_card(title, fig)
        else:
            st.info("No charts are available for this dataset.")
    except Exception as error:
        st.error(f"Unable to generate analytics charts: {error}")


# ==============================================================================
# DATA EXPLORER PAGE — searchable / filterable raw data table + export
# ==============================================================================
def render_data_explorer_page(df: pd.DataFrame) -> None:
    """Render the Data Explorer page: search, column selection, filter, and export."""

    st.markdown('<div class="section-title">🗂️ Data Explorer</div>', unsafe_allow_html=True)
    st.caption("Explore your dataset")

    top_col1, top_col2 = st.columns([3, 1])
    with top_col1:
        search_term = st.text_input(
            "Search",
            placeholder="🔍 Search...",
            label_visibility="collapsed",
        )
    with top_col2:
        columns_to_show = st.multiselect(
            "Columns",
            options=list(df.columns),
            default=list(df.columns),
            label_visibility="collapsed",
            placeholder="Columns",
        )

    filtered_df = df.copy()
    if columns_to_show:
        filtered_df = filtered_df[columns_to_show]

    if search_term:
        mask = filtered_df.astype(str).apply(
            lambda col: col.str.contains(search_term, case=False, na=False)
        ).any(axis=1)
        filtered_df = filtered_df[mask]

    with st.container(border=True):
        st.markdown(
            f'<div class="chart-card-title">Showing {format_number(len(filtered_df))} of {format_number(len(df))} rows</div>',
            unsafe_allow_html=True,
        )
        st.dataframe(filtered_df, width="stretch")

    st.download_button(
        "⬇️ Export CSV",
        data=filtered_df.to_csv(index=False).encode("utf-8"),
        file_name="data_explorer_export.csv",
        mime="text/csv",
    )


def render_ai_dashboard_studio_page(df: pd.DataFrame) -> None:
    st.markdown('<div class="section-title">🧠 AI Dashboard Studio</div>', unsafe_allow_html=True)
    st.caption("Advanced analytics: relationships, forecasting, drill-down and report export.")

    t1,t2,t3,t4=st.tabs(["🔗 Relationships","🔮 Forecast","🔎 Drill-down","📄 Report"])
    with t1:
        rel=relationship_report(df)
        if rel.empty: st.info("At least two numeric columns are needed for relationship analysis.")
        else:
            st.dataframe(rel,use_container_width=True)
            top=rel.iloc[0]
            st.success(f"Strongest detected relationship: {top['Column A']} ↔ {top['Column B']} (correlation {top['Correlation']:.3f}).")
    with t2:
        result,err=forecast(df)
        if err: st.info(err)
        else:
            hist=result["history"]; pred=result["forecast"]; metric=result["metric"]; time_col=hist.columns[0]
            import plotly.graph_objects as go
            fig=go.Figure()
            fig.add_trace(go.Scatter(x=hist[time_col],y=hist[metric],mode="lines+markers",name="Historical",line=dict(color="#6366F1",width=2.5)))
            fig.add_trace(go.Scatter(x=pred[time_col],y=pred[metric],mode="lines+markers",name="Forecast",line=dict(color="#8B5CF6",width=2.5,dash="dash")))
            fig.update_layout(title=f"{metric} Forecast",template="plotly_dark",paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",height=450)
            st.plotly_chart(fig,use_container_width=True); st.dataframe(pred,use_container_width=True)
    with t3:
        cats=df.select_dtypes(include=["object","category","bool"]).columns.tolist()
        if not cats: st.info("No categorical dimensions are available for drill-down.")
        else:
            dim=st.selectbox("Choose a dimension",cats,key="drill_dim"); values=df[dim].dropna().astype(str).value_counts().head(25).index.tolist()
            value=st.selectbox("Choose a value",values,key="drill_value") if values else None
            if value is not None:
                subset=data_drilldown(df,dim,value); st.metric("Filtered Records",f"{len(subset):,}"); st.dataframe(subset,use_container_width=True)
                if len(subset)>0: st.download_button("Download filtered data",subset.to_csv(index=False).encode("utf-8"),"drilldown.csv","text/csv")
    with t4:
        profile=get_data_profile(df) or {}; insight_text=[x for x in generate_insights(df)]
        if st.button("Generate PDF Report",type="primary",key="generate_pdf"):
            pdf=make_report_pdf(df,insight_text,profile); st.download_button("Download PDF",pdf,"ai_dashboard_report.pdf","application/pdf",key="download_pdf")
        st.info("Scheduling/email can be configured externally with Windows Task Scheduler or cron using this report generator. No credentials are hard-coded.")


# ==============================================================================
# SETTINGS PAGE
# ==============================================================================
def render_settings_page() -> None:
    """Render the Settings page: appearance and app info."""

    st.markdown('<div class="section-title">⚙️ Settings</div>', unsafe_allow_html=True)

    with st.container(border=True):
        st.markdown("**Appearance**")
        st.toggle("🌙 Dark Mode", value=True, key="settings_dark_mode", disabled=True)
        st.caption("This build ships dark theme only — light theme is planned for a future release.")

    with st.container(border=True):
        st.markdown("**About**")
        st.caption("AI Dashboard Generator — an AI-powered analytics platform for CSV/Excel data.")
        st.caption("© 2026 AI Dashboard Generator · Internal Analytics Tool")


# ==============================================================================
# MAIN APPLICATION LOGIC
# ==============================================================================
def main() -> None:
    """Entry point for the Streamlit application."""

    load_custom_css()
    render_main_header()

    page, uploaded_file = render_sidebar()

    # No file uploaded yet: show empty state and stop further rendering.
    if uploaded_file is None:
        render_empty_state()
        return

    # --------------------------------------------------------------------
    # Load Dataset
    # --------------------------------------------------------------------
    try:
        df = load_data(uploaded_file)
    except Exception as error:
        st.error(f"Failed to load the uploaded file: {error}")
        return

    if df is None or df.empty:
        st.warning("The uploaded dataset appears to be empty. Please upload a valid file.")
        return
    try:
        st.session_state["dataset_context"] = create_dataset_context(df)

        # Reset chat when the loaded dataset changes. This prevents old
        # questions/answers from one dataset appearing under another dataset.
        try:
            sample_hash = pd.util.hash_pandas_object(
                pd.concat([df.head(25), df.tail(25)]),
                index=True,
            ).sum()
            dataset_signature = (
                tuple(map(str, df.columns)),
                tuple(map(str, df.dtypes)),
                int(len(df)),
                int(sample_hash),
            )
        except Exception:
            dataset_signature = (
                tuple(map(str, df.columns)),
                tuple(map(str, df.dtypes)),
                int(len(df)),
            )

        if st.session_state.get("dataset_signature") != dataset_signature:
            st.session_state["dataset_signature"] = dataset_signature
            st.session_state["chat_history"] = []
    except Exception as error:
        st.error(f"Failed to create AI dataset context: {error}")
        st.session_state["dataset_context"] = {}

    # --------------------------------------------------------------------
    # Generate Core Analysis Objects
    # --------------------------------------------------------------------
    try:
        profile = get_data_profile(df)
    except Exception as error:
        st.error(f"Failed to profile the dataset: {error}")
        profile = None

    try:
        quality = get_data_quality(df)
    except Exception as error:
        st.error(f"Failed to assess data quality: {error}")
        quality = None

    try:
        kpis = generate_kpis(df)
    except Exception as error:
        st.error(f"Failed to generate KPIs: {error}")
        kpis = {}

    # --------------------------------------------------------------------
    # Page Routing — 8 pages matching the reference sidebar
    # --------------------------------------------------------------------
    if page == "Overview":
        render_overview_page(df, kpis)
    elif page == "AI Assistant":
        render_ai_assistant_page(df)
    elif page == "Dashboard":
        render_dashboard_page(df)
    elif page == "Visualizations":
        render_visualizations_page(df)
    elif page == "AI Insights":
        render_ai_insights_page(df)
    elif page == "Anomalies":
        render_anomalies_page(df)
    elif page == "Data Explorer":
        render_data_explorer_page(df)
    elif page == "AI Dashboard Studio":
        render_ai_dashboard_studio_page(df)
    elif page == "Settings":
        render_settings_page()


if __name__ == "__main__":
    main()
