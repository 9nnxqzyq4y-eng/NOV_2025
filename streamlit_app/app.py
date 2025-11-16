"""
ABACO Financial Intelligence Platform
Enterprise-grade financial analytics with 4K visualizations
Production-ready Google Drive → Supabase ingestion pipeline

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
import re
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from supabase import create_client
import io

# Import custom modules
from config.theme import ABACO_THEME, PLOTLY_LAYOUT_4K, CUSTOM_CSS, PLOTLY_CONFIG_4K
from utils.ingestion import DataIngestionEngine
from utils.feature_engineering import FeatureEngineer
from utils.kpi_engine import KPIEngine

# ================== PAGE CONFIGURATION ==================
st.set_page_config(
    page_title="ABACO Financial Intelligence Platform",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom CSS
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ================== HEADER ==================
st.markdown("""
<h1 style='text-align: center; margin-bottom: 0;'>ABACO Financial Intelligence Platform</h1>
<p style='text-align: center; color: #9b87f5; font-size: 18px; margin-top: 0;'>
    Superior predictive intelligence for strategic financial decisions
</p>
""", unsafe_allow_html=True)

st.divider()

# ================== CONFIGURATION & SECRETS ==================
@st.cache_resource
def get_configs():
    """Load configuration from Streamlit secrets"""
    try:
        return {
            "SUPABASE_URL": st.secrets.get("SUPABASE_URL", ""),
            "SUPABASE_KEY": st.secrets.get("SUPABASE_SERVICE_KEY", ""),
            "GDRIVE_SERVICE_ACCOUNT": st.secrets.get("GDRIVE_SERVICE_ACCOUNT", "{}"),
            "GDRIVE_FOLDER_ID": st.secrets.get("GDRIVE_FOLDER_ID", ""),
            "GEMINI_API_KEY": st.secrets.get("GEMINI_API_KEY", ""),
        }
    except Exception as e:
        st.error(f"Configuration error: {str(e)}")
        st.info("Please configure secrets in `.streamlit/secrets.toml`")
        return {}

configs = get_configs()

# ================== INITIALIZE CLIENTS ==================
def init_supabase():
    """Initialize Supabase client"""
    if not configs.get("SUPABASE_URL") or not configs.get("SUPABASE_KEY"):
        st.warning("Supabase credentials not configured")
        return None
    return create_client(configs["SUPABASE_URL"], configs["SUPABASE_KEY"])

def init_drive():
    """Initialize Google Drive client"""
    if not configs.get("GDRIVE_SERVICE_ACCOUNT"):
        st.warning("Google Drive credentials not configured")
    
        credentials_dict = json.loads(configs["GDRIVE_SERVICE_ACCOUNT"])
        credentials = service_account.Credentials.from_service_account_info(
            credentials_dict,
            scopes=['https://www.googleapis.com/auth/drive.readonly']
        )
        return build('drive', 'v3', credentials=credentials)
        st.error(f"Failed to initialize Google Drive: {str(e)}")

supabase = init_supabase()
drive = init_drive()

# ================== SIDEBAR NAVIGATION ==================
st.sidebar.title("🎯 Navigation")

page = st.sidebar.radio(
    "Select Module",
    [
        "📊 Dashboard Overview",
        "📥 Data Ingestion",
        "🎯 Risk Assessment",
        "📈 Growth Analysis",
        "💰 Revenue & Profitability",
        "🔄 Roll Rate Analysis",
        "🎨 Data Quality Audit",
        "🤖 AI Insights",
        "📤 Exports & Reports"
    ]

st.sidebar.divider()

# ================== INGESTION MODULE ==================
if "📥 Data Ingestion" in page:
    st.header("📥 Google Drive → Supabase Ingestion")
    
    st.info("""
    **Automated Data Pipeline**
    - Connects to Google Drive shared folder
    - Normalizes 9+ source types (portfolios, facilities, customers, payments, risk, revenue, collections, marketing, industry)
    - Validates and cleanses data
    - Upserts to Supabase staging tables
    - Refreshes ML features automatically
    - Scheduled daily at 6 AM via Supabase Cron
    """)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Manual Ingestion")
        
        if st.button("🚀 Run Ingestion Now", type="primary", use_container_width=True):
            if not supabase or not drive:
                st.error("Services not initialized. Check configuration.")
            else:
                with st.spinner("🔄 Ingesting data from Google Drive..."):
                    try:
                        # Initialize ingestion engine
                        ingestion_engine = DataIngestionEngine(
                            supabase_url=configs["SUPABASE_URL"],
                            supabase_key=configs["SUPABASE_KEY"],
                            gdrive_credentials=json.loads(configs["GDRIVE_SERVICE_ACCOUNT"])
                        )
                        
                        # Run ingestion
                        report = ingestion_engine.ingest_from_drive(configs["GDRIVE_FOLDER_ID"])
                        
                        # Display results
                        st.success("✅ Ingestion completed!")
                        
                        col_a, col_b, col_c, col_d = st.columns(4)
                        col_a.metric("Total Files", report['total_files'])
                        col_b.metric("Successful", report['successful'], delta_color="normal")
                        col_c.metric("Failed", report['failed'], delta_color="inverse")
                        col_d.metric("Skipped", report['skipped'], delta_color="off")
                        
                        # Detailed results
                        if report['details']:
                            st.subheader("Ingestion Details")
                            details_df = pd.DataFrame(report['details'])
                            
                            # Color code by status
                            def color_status(val):
                                if val == 'success':
                                    return f'background-color: {ABACO_THEME["accent_success"]}; color: white'
                                elif val == 'failed':
                                    return f'background-color: {ABACO_THEME["accent_danger"]}; color: white'
                                else:
                                    return f'background-color: {ABACO_THEME["accent_warning"]}; color: white'
                            
                            styled_df = details_df.style.applymap(color_status, subset=['status'])
                            st.dataframe(styled_df, use_container_width=True)
                        
                        # Quality scores
                        if report.get('quality_scores'):
                            st.subheader("Data Quality Scores")
                            quality_df = pd.DataFrame(report['quality_scores']).T
                            st.dataframe(quality_df, use_container_width=True)
                        
                    except Exception as e:
                        st.error(f"❌ Ingestion failed: {str(e)}")
    
    with col2:
        st.subheader("Configuration")
        st.text_input("Supabase URL", value=configs.get("SUPABASE_URL", ""), disabled=True)
        st.text_input("Drive Folder ID", value=configs.get("GDRIVE_FOLDER_ID", ""), disabled=True)
        
        st.divider()
        
        st.markdown("**Scheduled Ingestion**")
        st.code("Daily at 6:00 AM UTC", language="text")
        st.caption("Configured via Supabase Cron")
    
    # Cron setup instructions
    st.divider()
    st.subheader("⚙️ Supabase Cron Setup")
    
    st.markdown("""
    Run this SQL in **Supabase SQL Editor** to schedule automatic ingestion:
    
    cron_sql = """
-- Enable pg_cron extension
CREATE EXTENSION IF NOT EXISTS pg_cron;

-- Schedule daily ingestion at 6 AM UTC
SELECT cron.schedule(
    'daily-drive-ingestion',
    '0 6 * * *',
    $$
    SELECT net.http_post(
        url := 'https://your-app.vercel.app/api/ingest',
        headers := jsonb_build_object(
            'Authorization', 'Bearer ' || current_setting('app.supabase_service_key'),
            'Content-Type', 'application/json'
    );
);

-- Verify cron job
SELECT * FROM cron.job;
    """
    
    st.code(cron_sql, language="sql")

# ================== RISK ASSESSMENT MODULE ==================
elif "🎯 Risk Assessment" in page:
    st.header("🎯 Risk Assessment Dashboard")
    
    if not supabase:
        st.error("Supabase not configured")
    else:
        try:
            # Fetch ML features
            response = supabase.table('ml_feature_snapshots').select('*').execute()
            
            if not response.data:
                st.warning("⚠️ No feature data available. Run ingestion first.")
                df = pd.DataFrame(response.data)
                
                # High-risk classification (MYPE rules)
                df['high_risk'] = (
                    (df.get('avg_dpd', 0) > 90) |
                    (df.get('ltv', 0) > 80) |
                    (df.get('dpd_mean', 0) > 60) |
                    (df.get('collection_rate', 0) < 0.7) |
                    (df.get('default_risk_score', 0) > 0.7)
                )
                
                # Summary metrics
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("Total Clients", len(df))
                col2.metric("High-Risk Clients", df['high_risk'].sum(), 
                           delta=f"{df['high_risk'].sum()/len(df)*100:.1f}%")
                col3.metric("Avg DPD", f"{df.get('dpd_mean', pd.Series([0])).mean():.1f} days")
                col4.metric("Collection Rate", f"{df.get('collection_rate', pd.Series([0])).mean()*100:.1f}%")
                
                # Risk distribution
                st.subheader("Risk Distribution")
                
                col_a, col_b = st.columns(2)
                
                with col_a:
                    # DPD histogram
                    fig_dpd = px.histogram(
                        df, 
                        x='dpd_mean', 
                        nbins=30,
                        title="DPD Distribution",
                        labels={'dpd_mean': 'Average DPD (days)', 'count': 'Number of Clients'},
                        color_discrete_sequence=[ABACO_THEME['brand_primary_light']]
                    )
                    fig_dpd.update_layout(**PLOTLY_LAYOUT_4K)
                    st.plotly_chart(fig_dpd, use_container_width=True, config=PLOTLY_CONFIG_4K)
                
                with col_b:
                    # Risk score distribution
                    if 'default_risk_score' in df.columns:
                        fig_risk = px.histogram(
                            df,
                            x='default_risk_score',
                            nbins=20,
                            title="Default Risk Score Distribution",
                            labels={'default_risk_score': 'Risk Score', 'count': 'Number of Clients'},
                            color_discrete_sequence=[ABACO_THEME['brand_primary_medium']]
                        fig_risk.update_layout(**PLOTLY_LAYOUT_4K)
                        st.plotly_chart(fig_risk, use_container_width=True, config=PLOTLY_CONFIG_4K)
                
                # High-risk clients table
                st.subheader("High-Risk Clients")
                high_risk_df = df[df['high_risk']]
                
                if len(high_risk_df) > 0:
                    display_cols = ['customer_id', 'name', 'dpd_mean', 'collection_rate', 'default_risk_score']
                    available_cols = [col for col in display_cols if col in high_risk_df.columns]
                    st.dataframe(
                        high_risk_df[available_cols].sort_values('default_risk_score', ascending=False),
                        use_container_width=True
                else:
                    st.success("✅ No high-risk clients identified")
                
        except Exception as e:
            st.error(f"Error loading risk data: {str(e)}")

# ================== DASHBOARD OVERVIEW ==================
elif "📊 Dashboard Overview" in page:
    st.header("📊 Executive Dashboard")
    
    st.info("**Real-time Financial Intelligence**  \nComprehensive view of portfolio health, growth metrics, and predictive insights")
    
    # Placeholder metrics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("AUM", "$125.4M", "+12.3%")
    col2.metric("Active Clients", "3,847", "+156")
    col3.metric("Default Rate", "2.8%", "-0.4%")
    col4.metric("NRR", "112%", "+5%")
    
    
    # Sample chart
    st.subheader("Portfolio Growth Trend")
    dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='M')
    values = np.cumsum(np.random.randn(len(dates)) * 1000000 + 10000000)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=dates,
        y=values,
        mode='lines+markers',
        name='AUM',
        line=dict(color=ABACO_THEME['brand_primary_light'], width=3),
        marker=dict(size=8)
    ))
    
    fig.update_layout(**PLOTLY_LAYOUT_4K)
    fig.update_layout(title="Assets Under Management - 2024")
    st.plotly_chart(fig, use_container_width=True, config=PLOTLY_CONFIG_4K)

# ================== OTHER MODULES ==================
else:
    st.header(page)
    st.info("Module under development. Core ingestion and risk assessment modules are production-ready.")
    
    **Coming Soon:**
    - 📈 Growth Analysis: Current vs targets, gap analysis, monthly path projections
    - 💰 Revenue & Profitability: LTV:CAC by channel/segment, EBITDA analysis
    - 🔄 Roll Rate Analysis: DPD transition matrices, cure/default rates
    - 🎨 Data Quality Audit: Completeness scoring with PDF integration
    - 🤖 AI Insights: Gemini-powered summaries with rule-based fallback
    - 📤 Exports: CSV fact tables, Looker-ready data, Slack/HubSpot distribution

# ================== FOOTER ==================
st.caption(f"ABACO Financial Intelligence Platform v1.0 | Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}")
