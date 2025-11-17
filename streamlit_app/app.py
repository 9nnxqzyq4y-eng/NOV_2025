"""
ABACO Financial Intelligence Platform
Enterprise-grade financial analytics with 4K visualizations
Production-ready Google Drive → Supabase ingestion pipeline

import json
import warnings
from datetime import datetime
import streamlit as st
import pandas as pd
import plotly.express as px
from google.oauth2 import service_account
from supabase import create_client
from abaco_runtime.agent_orchestrator import DataIngestionEngine
from streamlit_app.config.theme import ABACO_THEME, PLOTLY_LAYOUT_4K, CUSTOM_CSS, PLOTLY_CONFIG_4K
warnings.filterwarnings("ignore")
#  PAGE CONFIGURATION 
st.set_page_config(
    page_title="ABACO Financial Intelligence Platform",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)
# Apply custom CSS
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
#  HEADER 
st.markdown(
    """
    <h1 style='text-align: center; margin-bottom: 0;'>ABACO Financial Intelligence Platform</h1>
    <p style='text-align: center; color: #9b87f5; font-size: 18px; margin-top: 0;'>
        Superior predictive intelligence for strategic financial decisions
    </p>
""",
    unsafe_allow_html=True,
st.divider()
#  CONFIGURATION & SECRETS 
@st.cache_resource
def get_configs():
    """Load configuration from Streamlit secrets"""
    try:
        # Use direct access to fail fast if secrets are missing
        return {
            "SUPABASE_URL": st.secrets["SUPABASE_URL"],
            "SUPABASE_KEY": st.secrets["SUPABASE_SERVICE_KEY"],
            "GDRIVE_SERVICE_ACCOUNT": st.secrets["GDRIVE_SERVICE_ACCOUNT"],
            "GDRIVE_FOLDER_ID": st.secrets["GDRIVE_FOLDER_ID"],
        }
    except Exception as e:
        st.error(f"Configuration error: {str(e)}")
        st.info("Please configure secrets in `.streamlit/secrets.toml`")
        return {}
configs = get_configs()
#  INITIALIZE CLIENTS 
def init_supabase():
    """Initialize Supabase client"""
    if not configs.get("SUPABASE_URL") or not configs.get("SUPABASE_KEY"):
        st.warning("Supabase credentials not configured")
        return None
    return create_client(configs["SUPABASE_URL"], configs["SUPABASE_KEY"])
def _validate_gdrive_credentials():
    """Validates Google Drive service account credentials."""
    gdrive_creds = configs.get("GDRIVE_SERVICE_ACCOUNT")
    if not gdrive_creds:
        st.warning("Google Drive credentials not configured.")
        credentials_dict = json.loads(gdrive_creds)
        _ = service_account.Credentials.from_service_account_info(
            credentials_dict, scopes=["https://www.googleapis.com/auth/drive.readonly"]
        )
        return None  # build('drive', 'v3', credentials=credentials)
        st.error(f"Failed to initialize Google Drive: {str(e)}")
supabase = init_supabase()
_validate_gdrive_credentials()
#  SIDEBAR NAVIGATION 
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
        "📤 Exports & Reports",
    ],
st.sidebar.divider()
#  HELPER FUNCTIONS 
def load_and_process_risk_data():
    """Fetches and processes risk data from Supabase."""
    response = supabase.table("ml_feature_snapshots").select("*").execute()
    if not response.data:
        st.warning("⚠️ No feature data available. Run ingestion first.")
    df = pd.DataFrame(response.data)
    # High-risk classification (MYPE rules)
    df["high_risk"] = (
        (df.get("avg_dpd", 0) > 90)
        | (df.get("ltv", 0) > 80)
        | (df.get("dpd_mean", 0) > 60)
        | (df.get("collection_rate", 0) < 0.7)
        | (df.get("default_risk_score", 0) > 0.7)
    )
    return df
def display_risk_metrics(df):
    """Displays summary metrics for the risk dashboard."""
    col1, col2, col3, col4 = st.columns(4)  # type: ignore
    col1.metric("Total Clients", len(df))
    col2.metric(
        "High-Risk Clients",
        df["high_risk"].sum(),
        delta=f"{df['high_risk'].sum()/len(df)*100:.1f}%",
    col3.metric("Avg DPD",
                f"{df.get('dpd_mean', pd.Series([0])).mean():.1f} days")
    col4.metric("Collection Rate",
                f"{df.get('collection_rate', pd.Series([0])).mean()*100:.1f}%")
def _style_ingestion_details(df: pd.DataFrame) -> pd.io.formats.style.Styler:
    """Applies color styling to the ingestion details dataframe."""
    def color_status(val):
        if val == "success":
            return f'background-color: {ABACO_THEME["accent_success"]}; color: white'
        elif val == "failed":
            return f'background-color: {ABACO_THEME["accent_danger"]}; color: white'
        return f'background-color: {ABACO_THEME["accent_warning"]}; color: white'
    return df.style.map(color_status, subset=["status"])
def _display_ingestion_report(report: dict):
    """Displays the metrics and detailed results from an ingestion run."""
    st.success("✅ Ingestion completed!")
    col_a, col_b, col_c, col_d = st.columns(4)
    col_a.metric("Total Files", report["total_files"])
    col_b.metric("Successful", report["successful"], delta_color="normal")
    col_c.metric("Failed", report["failed"], delta_color="inverse")
    col_d.metric("Skipped", report["skipped"], delta_color="off")
    if report["details"]:
        st.subheader("Ingestion Details")
        details_df = pd.DataFrame(report["details"])
        styled_df = _style_ingestion_details(details_df)
        st.dataframe(styled_df, use_container_width=True)
    if report.get("quality_scores"):
        st.subheader("Data Quality Scores")
        quality_df = pd.DataFrame(report["quality_scores"]).T
        st.dataframe(quality_df, use_container_width=True)
def _run_ingestion():
    """Initializes and runs the data ingestion engine."""
    with st.spinner("🔄 Ingesting data from Google Drive..."):
        try:
            ingestion_engine = DataIngestionEngine(
                supabase_url=configs["SUPABASE_URL"],
                supabase_key=configs["SUPABASE_KEY"],
                gdrive_credentials=json.loads(configs["GDRIVE_SERVICE_ACCOUNT"]),
            )
            report = ingestion_engine.ingest_from_drive(configs["GDRIVE_FOLDER_ID"])
            _display_ingestion_report(report)
        except Exception as e:
            st.error(f"❌ Ingestion failed: {str(e)}")
#  INGESTION MODULE 
if "📥 Data Ingestion" in page:
    st.header("📥 Google Drive → Supabase Ingestion")
    st.info(
        """
    **Automated Data Pipeline**
    - Connects to Google Drive, normalizes 9+ source types (portfolios,
      facilities, customers, payments, risk, revenue, etc.)
    - Validates and cleanses data
    - Upserts to Supabase staging tables
    - Refreshes ML features
    - Scheduled daily at 6 AM via Supabase Cron
    col1, col2 = st.columns([2, 1])
    with col1:
        st.subheader("Manual Ingestion")
        if st.button("🚀 Run Ingestion Now", type="primary", use_container_width=True):
            if not supabase or not configs.get("GDRIVE_SERVICE_ACCOUNT"):
                st.error("Services not initialized. Check configuration.")
            else:
                _run_ingestion()
    with col2:
        st.subheader("Configuration")
        st.text_input("Supabase URL", value=configs.get("SUPABASE_URL", ""),
                       disabled=True)
        st.text_input("Drive Folder ID",
                       value=configs.get("GDRIVE_FOLDER_ID", ""), disabled=True)
        st.divider()
        st.markdown("**Scheduled Ingestion**")
        st.code("Daily at 6:00 AM UTC", language="text")
        st.caption("Configured via Supabase Cron")
    # Cron setup instructions
    st.divider()
    st.subheader("⚙️ Supabase Cron Setup")
    st.markdown(
    Run this SQL in the **Supabase SQL Editor** to schedule automatic ingestion:
    st.code(
        """-- Enable pg_cron extension
CREATE EXTENSION IF NOT EXISTS pg_cron;
-- Schedule daily ingestion at 6 AM UTC
SELECT cron.schedule(
    'daily-drive-ingestion',
    '0 6 * * *',
    $$
    SELECT net.http_post(
        url:='https://your-app.vercel.app/api/ingest',
        headers:=jsonb_build_object(
            'Authorization', 'Bearer ' || current_setting('app.supabase_service_key'),
            'Content-Type', 'application/json'
    );
);
-- Verify cron job
SELECT * FROM cron.job;
        language="sql",
#  RISK ASSESSMENT MODULE 
elif "🎯 Risk Assessment" in page:
    st.header("🎯 Risk Assessment Dashboard")
    if not supabase:
        st.error("Supabase not configured")
    else:
        df = load_and_process_risk_data()
        if df is not None:
            display_risk_metrics(df)
            st.subheader("Risk Distribution")
            col_a, col_b = st.columns(2)
            with col_a:
                fig_dpd = px.histogram(
                    df,
                    x="dpd_mean",
                    nbins=30,
                    title="DPD Distribution",
                    labels={"dpd_mean": "Average DPD (days)",
                            "count": "Number of Clients"},
                    color_discrete_sequence=[ABACO_THEME["brand_primary_light"]],
                )
                fig_dpd.update_layout(**PLOTLY_LAYOUT_4K)
                st.plotly_chart(
                    fig_dpd, use_container_width=True, config=PLOTLY_CONFIG_4K)
            with col_b:
                if "default_risk_score" in df.columns:
                    fig_risk = px.histogram(
                        df,
                        x="default_risk_score",
                        nbins=20,
                        title="Default Risk Score Distribution",
                        labels={"default_risk_score": "Risk Score", "count": "Number of Clients"},
                        color_discrete_sequence=[ABACO_THEME["brand_primary_medium"]],
                    )
                    fig_risk.update_layout(**PLOTLY_LAYOUT_4K)
                    st.plotly_chart(
                        fig_risk, use_container_width=True, config=PLOTLY_CONFIG_4K)
            st.subheader("High-Risk Clients")
            high_risk_df = df[df["high_risk"]]
            if not high_risk_df.empty:
                display_cols = [
                    "customer_id",
                    "name",
                    "dpd_mean",
                    "collection_rate",
                    "default_risk_score",
                ]
                available_cols = [
                    col for col in display_cols if col in high_risk_df.columns]
                st.dataframe(
                    high_risk_df[available_cols].sort_values(
                        "default_risk_score", ascending=False),
                    use_container_width=True,
                st.success("✅ No high-risk clients identified")
#  DASHBOARD OVERVIEW 
elif "📊 Dashboard Overview" in page:
    st.header("📊 Executive Dashboard")
        "**Real-time Financial Intelligence**  \nComprehensive view of "
        "portfolio health, growth metrics, and predictive insights"
    st.markdown("---")
    st.subheader("Key Performance Indicators")
    st.info("KPI data will be loaded and displayed here.")
#  OTHER MODULES 
else:
    st.header(page)
        "Module under development. Core ingestion and risk assessment modules are production-ready."
    **Coming Soon:**
    - **� Growth Analysis**: Current vs targets, gap analysis, monthly path projections
    - **💰 Revenue & Profitability**: LTV:CAC by channel/segment, EBITDA analysis
    - **🔄 Roll Rate Analysis**: DPD transition matrices, cure/default rates
    - **🎨 Data Quality Audit**: Completeness scoring with PDF integration
    - **🤖 AI Insights**: Gemini-powered summaries with rule-based fallback
    - **📤 Exports**: CSV fact tables, Looker-ready data, Slack/HubSpot distribution
#  FOOTER 
st.caption(
    "ABACO Financial Intelligence Platform v1.0 | Last updated: "
    f"{datetime.now().strftime('%Y-%m-%d %H:%M UTC')}"
