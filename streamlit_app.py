"""ABACO Financial Intelligence Platform - Streamlit Dashboard"""

import io
import json
import re
from datetime import datetime, timezone
import warnings
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from supabase import create_client
import streamlit as st
warnings.filterwarnings("ignore")
ABACO_THEME = {
    "colors": {
        "primary": "#C1A6FF",
        "primary_dark": "#5F4896",
        "dark": "#030E19",
        "muted": "#6D7D8E",
        "success": "#10B981",
        "warning": "#FB923C",
        "error": "#DC2626",
    }
}
PAGE_TITLE = "ABACO Financial Intelligence"
PAGE_LAYOUT = "wide"
INITIAL_SIDEBAR_STATE = "collapsed"
st.set_page_config(
    page_title=PAGE_TITLE,
    layout=PAGE_LAYOUT,
    initial_sidebar_state=INITIAL_SIDEBAR_STATE,
)
PLOT_BG_COLOR = "rgba(0,0,0,0)"
FONT_COLOR = "white"
HOVERMODE_UNIFIED = "x unified"
HOVERMODE_CLOSEST = "closest"
GDRIVE_SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]
GDRIVE_API_VERSION = "v3"
TABLE_MAP = {
    "portfolio": "raw_portfolios",
    "facility": "raw_facilities",
    "customer": "raw_customers",
    "payment": "raw_payments",
    "risk": "raw_risk_events",
PRIMARY_KEYS = {
    "raw_portfolios": ["workbook_name", "portfolio_name"],
    "raw_facilities": ["facility_code"],
    "raw_customers": ["customer_code"],
    "raw_payments": ["payment_code"],
    "raw_risk_events": ["customer_code", "event_date", "event_type"],
COL_WORKBOOK_NAME = "workbook_name"
COL_REFRESH_DATE = "refresh_date"
COL_AVG_DPD = "avg_dpd"
COL_LTV = "ltv"
COL_COLLECTION_RATE = "collection_rate"
COL_AVG_RISK_SEVERITY = "avg_risk_severity"
COL_CUSTOMER_CODE = "customer_code"
COL_NAME = "name"
COL_HIGH_RISK = "high_risk"
HIGH_RISK_DPD_THRESHOLD = 90
HIGH_RISK_DPD_MODERATE = 60
HIGH_RISK_LTV_THRESHOLD = 80
LOW_COLLECTION_RATE_THRESHOLD = 0.70
HIGH_RISK_SEVERITY_THRESHOLD = 0.7
LABEL_HIGH_RISK_CLIENTS = "High-Risk Clients"
LABEL_AVG_DPD = "Average DPD (days)"
LABEL_AVG_LTV = "Average LTV (%)"
LABEL_COLLECTION_RATE = "Collection Rate (%)"
LABEL_DPD_DISTRIBUTION = "Days Past Due Distribution"
LABEL_LTV_DISTRIBUTION = "Loan-to-Value Distribution"
LABEL_RISK_MATRIX = "Risk Matrix (DPD vs LTV)"
st.markdown(
    f"""
    <style>
        body {{ background: {ABACO_THEME['colors']['dark']}; color: {FONT_COLOR}; }}
        .stButton > button {{ background: {ABACO_THEME['colors']['primary']}; color: {FONT_COLOR}; border: none; }}
        .metric-number {{ font-size: 2rem; font-weight: 700; }}
        .stMetric {{ background: rgba({int('C1', 16)}, {int('A6', 16)}, {int('FF', 16)}, 0.1); padding: 1rem; border-radius: 0.5rem; }}
    </style>
    """,
    unsafe_allow_html=True,
@st.cache_resource
def get_configs():
    """Load configuration from Streamlit secrets."""
    return {
        "SUPABASE_URL": st.secrets["SUPABASE_URL"],
        "SUPABASE_KEY": st.secrets["SUPABASE_SERVICE_KEY"],
        "GDRIVE_SERVICE_ACCOUNT": json.loads(st.secrets["GDRIVE_SERVICE_ACCOUNT"]),
        "GDRIVE_FOLDER_ID": st.secrets["GDRIVE_FOLDER_ID"],
configs = get_configs()
def init_clients():
    """Initialize Supabase and Google Drive clients."""
    supabase_client = create_client(configs["SUPABASE_URL"], configs["SUPABASE_KEY"])
    credentials = service_account.Credentials.from_service_account_info(
        configs["GDRIVE_SERVICE_ACCOUNT"],
        scopes=GDRIVE_SCOPES,
    )
    drive_client = build("drive", GDRIVE_API_VERSION, credentials=credentials)
    return supabase_client, drive_client
supabase, drive = init_clients()
def normalize_df(df: pd.DataFrame, source: str) -> pd.DataFrame:
    """Normalize DataFrame column names and data types."""
    df.columns = [
        re.sub(r"[^a-z0-9_]", "_", col.strip().lower().replace(" ", "_")) for col in df.columns
    ]
    for col in df.columns:
        if df[col].dtype == "object":
            df[col] = (
                df[col]
                .astype(str)
                .str.replace(r"[\$,₡,€,%]", "", regex=True)
                .str.replace(",", "", regex=True)
                .str.strip()
            )
            df[col] = pd.to_numeric(df[col], errors="coerce")
        if "date" in col:
            df[col] = pd.to_datetime(df[col], errors="coerce")
    df[COL_WORKBOOK_NAME] = source
    df[COL_REFRESH_DATE] = datetime.now(timezone.utc)
    return df.drop_duplicates()
def ingest_from_drive():
    """Ingest files from Google Drive and upsert to Supabase."""
    try:
        query = (
            f"'{configs['GDRIVE_FOLDER_ID']}' in parents "
            "and mimeType != 'application/vnd.google-apps.folder' "
            "and trashed = false"
        )
        results = drive.files().list(q=query, fields="files(id, name, mimeType)").execute()
        files = results.get("files", [])
        if not files:
            st.warning("No files found in shared folder.")
            return
        progress_bar = st.progress(0)
        status_text = st.empty()
        for idx, file in enumerate(files):
            file_id, file_name, mime_type = file["id"], file["name"], file["mimeType"]
            status_text.text(f"Processing: {file_name}")
            request = drive.files().get_media(fileId=file_id)
            fh = io.BytesIO()
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while not done:
                _, done = downloader.next_chunk()
            fh.seek(0)
            if mime_type.endswith("sheet") or file_name.endswith(".xlsx"):
                df = pd.read_excel(fh)
            elif mime_type == "text/csv" or file_name.endswith(".csv"):
                df = pd.read_csv(fh)
            else:
                st.warning(f"Skipping unsupported file: {file_name}")
                continue
            df = normalize_df(df, file_name)
            table = next(
                (dest for key, dest in TABLE_MAP.items() if key in file_name.lower()),
                None,
            if not table:
                st.warning(f"No staging table mapping for file: {file_name}")
            key_cols = PRIMARY_KEYS.get(table, ["id"])
            data = df.to_dict(orient="records")
            supabase.table(table).upsert(
                data, returning="minimal", on_conflict=",".join(key_cols)
            ).execute()
            st.success(f"✓ {file_name}: upserted {len(data)} rows into {table}")
            progress_bar.progress((idx + 1) / len(files))
        supabase.rpc("refresh_ml_features").execute()
        st.success("✓ ML features refreshed successfully.")
    except Exception as exc:
        st.error(f"Ingestion failed: {exc}")
st.sidebar.header("🔄 Data Management")
if st.sidebar.button("▶ Run Google Drive Ingestion", use_container_width=True):
    with st.spinner("Ingesting from Google Drive..."):
        ingest_from_drive()
st.sidebar.markdown("---")
st.sidebar.info(
    "**Cron Scheduler**: Configure in Supabase SQL editor:\n"
    "`SELECT cron.schedule('daily-ingest', '0 6 * * *', 'SELECT refresh_ml_features();');`"
st.title("🏦 ABACO Financial Intelligence Platform")
st.markdown("Real-time risk assessment and portfolio analytics")
st.subheader("📊 Risk Assessment Dashboard")
try:
    result = supabase.table("ml_feature_snapshots").select("*").execute()
    records = result.data or []
    if not records:
        st.warning("No feature snapshots available. Run the ingestion worker first.")
    else:
        df = pd.DataFrame(records)
        df[COL_HIGH_RISK] = (
            (df[COL_AVG_DPD] >= HIGH_RISK_DPD_THRESHOLD)
            | (df[COL_LTV] >= HIGH_RISK_LTV_THRESHOLD)
            | (df[COL_COLLECTION_RATE] <= LOW_COLLECTION_RATE_THRESHOLD)
            | (df[COL_AVG_RISK_SEVERITY] >= HIGH_RISK_SEVERITY_THRESHOLD)
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric(
                LABEL_HIGH_RISK_CLIENTS,
                int(df[COL_HIGH_RISK].sum()),
                delta=None,
        with col2:
                LABEL_AVG_DPD,
                f"{df[COL_AVG_DPD].mean():.1f}",
        with col3:
                LABEL_AVG_LTV,
                f"{df[COL_LTV].mean():.1f}",
        with col4:
                LABEL_COLLECTION_RATE,
                f"{df[COL_COLLECTION_RATE].mean() * 100:.1f}",
        st.markdown("#### ⚠️ High-Risk Portfolio")
        high_risk_df = df.loc[
            df[COL_HIGH_RISK],
            [
                COL_CUSTOMER_CODE,
                COL_NAME,
                COL_AVG_DPD,
                COL_LTV,
                COL_COLLECTION_RATE,
                COL_AVG_RISK_SEVERITY,
            ],
        ].sort_values(COL_AVG_RISK_SEVERITY, ascending=False)
        if len(high_risk_df) > 0:
            st.dataframe(
                high_risk_df,
                use_container_width=True,
                hide_index=True,
        else:
            st.info("No high-risk clients detected.")
        st.markdown("#### 📈 Distributions")
        col1, col2 = st.columns(2)
            fig_dpd = px.histogram(
                df,
                x=COL_AVG_DPD,
                nbins=25,
                title=LABEL_DPD_DISTRIBUTION,
                color_discrete_sequence=[ABACO_THEME["colors"]["primary"]],
                labels={COL_AVG_DPD: "Days Past Due", "count": "Count"},
            fig_dpd.update_layout(
                hovermode=HOVERMODE_UNIFIED,
                plot_bgcolor=PLOT_BG_COLOR,
                paper_bgcolor=PLOT_BG_COLOR,
                font={"color": FONT_COLOR},
            st.plotly_chart(fig_dpd, use_container_width=True)
            fig_ltv = px.histogram(
                x=COL_LTV,
                title=LABEL_LTV_DISTRIBUTION,
                color_discrete_sequence=[ABACO_THEME["colors"]["warning"]],
                labels={COL_LTV: "LTV (%)", "count": "Count"},
            fig_ltv.update_layout(
            st.plotly_chart(fig_ltv, use_container_width=True)
        fig_scatter = px.scatter(
            df,
            x=COL_AVG_DPD,
            y=COL_LTV,
            size=COL_COLLECTION_RATE,
            color=COL_AVG_RISK_SEVERITY,
            hover_data=[COL_CUSTOMER_CODE, COL_NAME],
            title=LABEL_RISK_MATRIX,
            color_continuous_scale="RdYlGn_r",
            labels={
                COL_AVG_DPD: "Average DPD (days)",
                COL_LTV: "LTV (%)",
                COL_AVG_RISK_SEVERITY: "Risk Severity",
            },
        fig_scatter.update_layout(
            hovermode=HOVERMODE_CLOSEST,
            plot_bgcolor=PLOT_BG_COLOR,
            paper_bgcolor=PLOT_BG_COLOR,
            font={"color": FONT_COLOR},
        st.plotly_chart(fig_scatter, use_container_width=True)
except Exception as exc:
    st.error(f"Dashboard error: {exc}")
