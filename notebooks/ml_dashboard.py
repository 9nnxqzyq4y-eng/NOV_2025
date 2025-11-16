#!/usr/bin/env python3
# notebooks/ml_dashboard.py

from __future__ import annotations

import os
from datetime import datetime
from typing import Optional

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from streamlit.delta_generator import DeltaGenerator
from supabase import Client, create_client

st: DeltaGenerator  # type: ignore

# ---------- Page ----------
st.set_page_config(page_title="ABACO ML Dashboard", layout="wide", initial_sidebar_state="expanded")

# ---------- ABACO theme ----------
ABACO = {
    "bg": "#030E19",
    "fg": "#CED4D9",
    "white": "#FFFFFF",
    "primary": "#C1A6FF",
    "primary_dark": "#5F4896",
    "success": "#10B981",
    "warning": "#FB923C",
    "error": "#DC2626",
    "info": "#3B82F6",
}
st.markdown(
    f"""
    <style>
      .stApp {{ background:{ABACO["bg"]}; color:{ABACO["fg"]}; }}
      .block-container {{ padding-top: 1.2rem; }}
      h1,h2,h3,h4 {{ color:{ABACO["white"]}; }}
      .metric > div:not(:first-child) span {{ color:{ABACO["white"]} !important; }}
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- Config ----------
def _get_cfg() -> dict:
    url = os.environ.get("SUPABASE_URL") or st.secrets.get("SUPABASE_URL", None)
    key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY") or st.secrets.get(
        "SUPABASE_SERVICE_ROLE_KEY", None
    )
    api = os.environ.get("NEXT_API_URL") or st.secrets.get("NEXT_API_URL", "http://localhost:3000")
    return {"SUPABASE_URL": url, "SUPABASE_KEY": key, "NEXT_API_URL": api}

cfg = _get_cfg()
if not cfg["SUPABASE_URL"] or not cfg["SUPABASE_KEY"]:
    st.error(
        "Supabase no configurado. Define SUPABASE_URL y SUPABASE_SERVICE_ROLE_KEY en env o .streamlit/secrets.toml"
    st.stop()

# ---------- Clients ----------
@st.cache_resource(show_spinner=False)
def get_supabase(url: str, key: str) -> Client:
    return create_client(url, key)

sb: Client = get_supabase(cfg["SUPABASE_URL"], cfg["SUPABASE_KEY"])

# ---------- Sidebar ----------
with st.sidebar:
    st.header("Configuration")
    window_days: int = st.slider("Metrics window (days)", 7, 120, 30)
    refresh_seconds: int = st.slider("Refresh interval (seconds)", 5, 120, 30)
    if st.button("Refresh"):
        st.rerun()

# ---------- Data ----------
@st.cache_data(ttl=60, show_spinner=False)
def read_table(schema: str, table: str) -> pd.DataFrame:
    # Prefer schema-qualified access; fallback to fully-qualified name if needed
    try:
        res = sb.postgrest.schema(schema).from_(table).select("*").execute()
    except Exception:
        res = sb.from_(f"{schema}.{table}").select("*").execute()
    data = res.data or []
    df = pd.DataFrame(data)
    if df.empty:
        return df

    # Parse timestamps
    for c in [c for c in df.columns if "time" in c or "date" in c or c == "created_at"]:
        try:
            df[c] = pd.to_datetime(df[c], errors="coerce", utc=True)
        except Exception:
            pass

    # Parse numerics
    for c in ["score", "prediction_score", "probability", "amount", "brier"]:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")
    return df

pred_df = read_table(
    "ml", "predictions"
)  # id, loan_id, score|prediction_score, label, model_version, created_at
fb_df = read_table(
    "ml", "feedback"
)  # id, prediction_id, loan_id, outcome_label, correct, created_at
mx_df = read_table("ml", "learning_metrics")  # id, metrics (json), created_at

# Harmonize score column name
if "score" not in pred_df.columns and "prediction_score" in pred_df.columns:
    pred_df = pred_df.rename(columns={"prediction_score": "score"})

# ---------- KPIs ----------
st.title("ABACO • ML Continue Learning Dashboard")

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.metric("Total predictions", f"{len(pred_df):,}")
with c2:
    st.metric("Feedback received", f"{len(fb_df):,}")
with c3:
    acc: Optional[float] = None
    if not fb_df.empty and "correct" in fb_df.columns:
        acc = float(pd.to_numeric(fb_df["correct"], errors="coerce").fillna(0).mean())
    st.metric("Overall accuracy", f"{acc:.1%}" if acc is not None else "N/A")
with c4:
    # Brier score via join on prediction_id -> predictions.id
    avg_brier: Optional[float] = None
    if (
        not fb_df.empty
        and not pred_df.empty
        and {"id", "score"}.issubset(pred_df.columns)
        and "prediction_id" in fb_df.columns
    ):
        j = fb_df.merge(
            pred_df[["id", "score"]], left_on="prediction_id", right_on="id", how="left"
        )
        if not j.empty and "score" in j.columns and "correct" in j.columns:
            p = pd.to_numeric(j["score"], errors="coerce")
            y = pd.to_numeric(j["correct"], errors="coerce").fillna(0.0)  # 1=correct, 0=incorrect
            brier = (p - y) ** 2
            if brier.notna().any():
                avg_brier = float(brier.mean())
    st.metric("Avg Brier score", f"{avg_brier:.3f}" if avg_brier is not None else "N/A")

st.divider()

# ---------- Charts ----------
# Score distribution
if not pred_df.empty and "score" in pred_df.columns:
    fig = go.Figure(go.Histogram(x=pred_df["score"], nbinsx=30))
    fig.update_layout(
        title="Prediction score distribution",
        height=360,
        margin=dict(l=10, r=10, t=40, b=10),
        paper_bgcolor=ABACO["bg"],
        plot_bgcolor=ABACO["bg"],
        font=dict(color=ABACO["fg"]),
    st.plotly_chart(fig, use_container_width=True)

# Label distribution
if not pred_df.empty and "label" in pred_df.columns:
    counts = pred_df["label"].value_counts().reset_index(names=["label", "count"])
    fig = px.bar(counts, x="label", y="count", title="Prediction label distribution", height=360)

# Rolling accuracy by day
if not fb_df.empty and "created_at" in fb_df.columns and "correct" in fb_df.columns:
    ts = (
        fb_df.assign(created_at=pd.to_datetime(fb_df["created_at"], errors="coerce", utc=True))
        .dropna(subset=["created_at"])
        .assign(
            correct=lambda x: pd.to_numeric(x["correct"], errors="coerce").fillna(0).astype(int)
        .set_index("created_at")
        .resample("1D")["correct"]
        .mean()
        .to_frame("acc")
        .rolling(window=max(1, min(window_days, 120)), min_periods=1)
        .reset_index()
    if not ts.empty:
        fig = go.Figure(go.Scatter(x=ts["created_at"], y=ts["acc"], mode="lines"))
        fig.update_layout(
            title=f"Accuracy trend (rolling {window_days}d)",
            yaxis_tickformat=".0%",
            height=360,
            margin=dict(l=10, r=10, t=40, b=10),
            paper_bgcolor=ABACO["bg"],
            plot_bgcolor=ABACO["bg"],
            font=dict(color=ABACO["fg"]),
        st.plotly_chart(fig, use_container_width=True)


# ---------- Tables ----------
if not pred_df.empty:
    st.subheader("Recent predictions")
    cols = [
        c
        for c in ["id", "loan_id", "score", "label", "model_version", "created_at"]
        if c in pred_df.columns
    ]
    view = (
        pred_df.sort_values("created_at", ascending=False)[cols].head(200).copy()
        if cols
        else pred_df.head(200)
    if "score" in view.columns:
        view["score"] = pd.to_numeric(view["score"], errors="coerce").map(
            lambda v: f"{v:.3f}" if pd.notna(v) else ""
    st.dataframe(view, use_container_width=True)
else:
    st.info("No predictions")

if not fb_df.empty:
    st.subheader("Recent feedback")
        for c in ["prediction_id", "loan_id", "outcome_label", "correct", "comments", "created_at"]
        if c in fb_df.columns
        fb_df.sort_values("created_at", ascending=False)[cols].head(200).copy()
        else fb_df.head(200)
    if "correct" in view.columns:
        view["correct"] = view["correct"].map(lambda v: "✅" if bool(v) else "❌")
    st.info("No feedback")

# ---------- Metrics history ----------
if not mx_df.empty and "metrics" in mx_df.columns and "created_at" in mx_df.columns:
    st.subheader("Model performance metrics history")
    m = mx_df.copy()
    m["created_at"] = pd.to_datetime(m["created_at"], errors="coerce", utc=True)
    m["metrics_parsed"] = m["metrics"].apply(lambda x: x if isinstance(x, dict) else {})
    m["accuracy"] = pd.to_numeric(
        m["metrics_parsed"].apply(lambda d: d.get("acc")), errors="coerce"
    m["brier"] = pd.to_numeric(m["metrics_parsed"].apply(lambda d: d.get("brier")), errors="coerce")

    c1, c2 = st.columns(2)
    if m["accuracy"].notna().any():
        fig = go.Figure(go.Scatter(x=m["created_at"], y=m["accuracy"], mode="lines+markers"))
            title="Accuracy over time",
            height=320,
        c1.plotly_chart(fig, use_container_width=True)
    if m["brier"].notna().any():
        fig = go.Figure(go.Scatter(x=m["created_at"], y=m["brier"], mode="lines+markers"))
            title="Brier score over time (lower is better)",
        c2.plotly_chart(fig, use_container_width=True)
