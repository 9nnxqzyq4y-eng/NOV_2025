"""
Risk Assessment Dashboard Component
MYPE-specific risk scoring and approval evaluation

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from typing import Dict, List

from ..config.theme import ABACO_THEME, PLOTLY_LAYOUT_4K, PLOTLY_CONFIG_4K
from ..utils.business_rules import MYPEBusinessRules, RiskLevel, IndustryType

def render_risk_dashboard(features_df: pd.DataFrame):
    """
    Render comprehensive MYPE risk assessment dashboard
    
    Args:
        features_df: DataFrame from ml_feature_snapshots
    st.header("🎯 MYPE Risk Assessment Dashboard")
    
    st.info("""
    **Risk Classification based on MYPE 2025 Standards**  
    High-risk criteria: DPD >90 days OR LTV >80% OR Avg DPD >60 OR Collection Rate <70%
    """)
    
    # Apply MYPE business rules
    features_df['is_high_risk'] = features_df.apply(
        lambda row: MYPEBusinessRules.classify_high_risk({
            'dpd_mean': row.get('dpd_mean', 0),
            'ltv': row.get('utilization', 0) * 100,  # Convert to percentage
            'avg_dpd': row.get('dpd_mean', 0),
            'collection_rate': row.get('collection_rate', 1.0),
            'avg_risk_severity': row.get('default_risk_score', 0)
        })[0],
        axis=1
    )
    
    # Calculate NPL status
    features_df['is_npl'] = features_df['dpd_mean'].apply(
        lambda dpd: MYPEBusinessRules.classify_npl(dpd)[0]
    
    # Summary metrics
    col1, col2, col3, col4, col5 = st.columns(5)
    
    total_clients = len(features_df)
    high_risk_count = features_df['is_high_risk'].sum()
    npl_count = features_df['is_npl'].sum()
    avg_collection = features_df['collection_rate'].mean()
    avg_dpd = features_df['dpd_mean'].mean()
    
    col1.metric("Total Clients", f"{total_clients:,}")
    col2.metric(
        "High-Risk", 
        f"{high_risk_count:,}",
        delta=f"{high_risk_count/total_clients*100:.1f}%",
        delta_color="inverse"
    col3.metric(
        "NPL (180+ days)",
        f"{npl_count:,}",
        delta=f"{npl_count/total_clients*100:.1f}%",
    col4.metric(
        "Avg Collection Rate",
        f"{avg_collection*100:.1f}%",
        delta=f"{(avg_collection - MYPEBusinessRules.TARGET_COLLECTION_RATE)*100:+.1f}%",
        delta_color="normal"
    col5.metric(
        "Avg DPD",
        f"{avg_dpd:.0f} days",
    
    st.divider()
    
    # Risk distribution visualization
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.subheader("DPD Distribution by Risk Level")
        
        # Create DPD buckets
        features_df['dpd_bucket'] = pd.cut(
            features_df['dpd_mean'],
            bins=[0, 15, 30, 60, 90, 180, float('inf')],
            labels=['Current (0-15)', 'Watch (15-30)', 'Substandard (30-60)', 
                   'Doubtful (60-90)', 'High Risk (90-180)', 'NPL (180+)']
        )
        
        dpd_dist = features_df['dpd_bucket'].value_counts().sort_index()
        
        fig_dpd = go.Figure(data=[
            go.Bar(
                x=dpd_dist.index,
                y=dpd_dist.values,
                marker_color=ABACO_THEME['brand_primary_light'],
                text=dpd_dist.values,
                textposition='outside'
            )
        ])
        
        fig_dpd.update_layout(**PLOTLY_LAYOUT_4K)
        fig_dpd.update_layout(
            title="DPD Bucket Distribution",
            xaxis_title="DPD Range",
            yaxis_title="Number of Clients",
            showlegend=False
        fig_dpd.update_xaxis(tickangle=-45)
        
        st.plotly_chart(fig_dpd, use_container_width=True, config=PLOTLY_CONFIG_4K)
    
    with col_right:
        st.subheader("Collection Rate vs DPD")
        
        fig_scatter = px.scatter(
            features_df,
            x='dpd_mean',
            y='collection_rate',
            size='total_balance' if 'total_balance' in features_df.columns else None,
            color='is_high_risk',
            color_discrete_map={True: ABACO_THEME['accent_danger'], False: ABACO_THEME['accent_success']},
            hover_data=['customer_id', 'name'] if 'name' in features_df.columns else ['customer_id'],
            labels={
                'dpd_mean': 'Average DPD (days)',
                'collection_rate': 'Collection Rate',
                'is_high_risk': 'High Risk'
            }
        
        # Add threshold lines
        fig_scatter.add_hline(
            y=MYPEBusinessRules.HIGH_RISK_CRITERIA['collection_rate_threshold'],
            line_dash="dash",
            line_color=ABACO_THEME['accent_warning'],
            annotation_text="70% Collection Threshold"
        fig_scatter.add_vline(
            x=MYPEBusinessRules.HIGH_RISK_CRITERIA['dpd_threshold'],
            annotation_text="90 Days Threshold"
        
        fig_scatter.update_layout(**PLOTLY_LAYOUT_4K)
        fig_scatter.update_layout(title="Risk Profile Matrix")
        
        st.plotly_chart(fig_scatter, use_container_width=True, config=PLOTLY_CONFIG_4K)
    
    
    # High-risk clients table
    st.subheader("🚨 High-Risk Clients Requiring Attention")
    
    high_risk_df = features_df[features_df['is_high_risk']].copy()
    
    if len(high_risk_df) > 0:
        # Get risk reasons for each client
        high_risk_df['risk_reasons'] = high_risk_df.apply(
            lambda row: ', '.join(MYPEBusinessRules.classify_high_risk({
                'dpd_mean': row.get('dpd_mean', 0),
                'ltv': row.get('utilization', 0) * 100,
                'avg_dpd': row.get('dpd_mean', 0),
                'collection_rate': row.get('collection_rate', 1.0),
                'avg_risk_severity': row.get('default_risk_score', 0)
            })[1]),
            axis=1
        
        # Get NPL classification
        high_risk_df['npl_status'] = high_risk_df['dpd_mean'].apply(
            lambda dpd: MYPEBusinessRules.classify_npl(int(dpd))[1]
        
        display_cols = ['customer_id', 'name', 'dpd_mean', 'collection_rate', 
                       'default_risk_score', 'npl_status', 'risk_reasons']
        available_cols = [col for col in display_cols if col in high_risk_df.columns]
        
        # Format and display
        display_df = high_risk_df[available_cols].sort_values('dpd_mean', ascending=False)
        
        # Format percentages
        if 'collection_rate' in display_df.columns:
            display_df['collection_rate'] = (display_df['collection_rate'] * 100).round(1).astype(str) + '%'
        if 'default_risk_score' in display_df.columns:
            display_df['default_risk_score'] = (display_df['default_risk_score'] * 100).round(1).astype(str) + '%'
        
        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True
        
        # Export button
        csv = display_df.to_csv(index=False)
        st.download_button(
            label="📥 Download High-Risk Report (CSV)",
            data=csv,
            file_name=f"high_risk_clients_{pd.Timestamp.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
    else:
        st.success("✅ No high-risk clients identified")
    
    
    # NPL Analysis
    st.subheader("📊 Non-Performing Loans (NPL) Analysis")
    
    npl_df = features_df[features_df['is_npl']].copy()
    
    col_a, col_b, col_c = st.columns(3)
    
    with col_a:
        npl_total_balance = npl_df['total_balance'].sum() if 'total_balance' in npl_df.columns else 0
        total_portfolio_balance = features_df['total_balance'].sum() if 'total_balance' in features_df.columns else 1
        npl_ratio = npl_total_balance / total_portfolio_balance * 100 if total_portfolio_balance > 0 else 0
        
        st.metric(
            "NPL Balance",
            f"${npl_total_balance:,.0f}",
            delta=f"{npl_ratio:.1f}% of portfolio",
            delta_color="inverse"
    
    with col_b:
        avg_npl_dpd = npl_df['dpd_mean'].mean() if len(npl_df) > 0 else 0
            "Avg NPL DPD",
            f"{avg_npl_dpd:.0f} days"
    
    with col_c:
        npl_collection = npl_df['collection_rate'].mean() if len(npl_df) > 0 else 0
            "NPL Collection Rate",
            f"{npl_collection*100:.1f}%",

def render_approval_simulator():
    Render loan approval simulator using MYPE business rules
    st.header("🎯 Loan Approval Simulator")
    
    **MYPE 2025 Approval Standards**
    - Micro (<$50K): POD <35%, Collateral 1.0x
    - Small ($50K-$200K): POD <30%, Collateral 1.2x  
    - Medium (>$200K): POD <20%, Collateral 1.5x
    
    col1, col2 = st.columns(2)
    
    with col1:
        facility_amount = st.number_input(
            "Requested Facility Amount (USD)",
            min_value=1000,
            max_value=1_000_000,
            value=25_000,
            step=1000
        
        collateral_value = st.number_input(
            "Collateral Value (USD)",
            min_value=0,
            max_value=2_000_000,
            value=30_000,
        
        pod = st.slider(
            "Probability of Default (POD)",
            min_value=0.0,
            max_value=1.0,
            value=0.25,
            step=0.01,
            format="%.2f"
    
    with col2:
        dpd_mean = st.number_input(
            "Average DPD (days)",
            max_value=365,
            value=15,
            step=1
        
        collection_rate = st.slider(
            "Collection Rate",
            value=0.85,
        
        avg_risk_severity = st.slider(
            "Risk Severity Score",
            value=0.3,
    
    if st.button("🔍 Evaluate Approval", type="primary", use_container_width=True):
        customer_metrics = {
            'pod': pod,
            'dpd_mean': dpd_mean,
            'collection_rate': collection_rate,
            'avg_risk_severity': avg_risk_severity
        }
        
        decision = MYPEBusinessRules.evaluate_facility_approval(
            facility_amount=facility_amount,
            customer_metrics=customer_metrics,
            collateral_value=collateral_value
        
        # Display decision
        if decision.approved:
            st.success(f"✅ **APPROVED** - {decision.risk_level.value.upper()} Risk")
        else:
            st.error(f"❌ **DECLINED** - {decision.risk_level.value.upper()} Risk")
        
        # Decision details
        col_a, col_b, col_c = st.columns(3)
        
        with col_a:
            st.metric("Recommended Amount", f"${decision.recommended_amount:,.0f}")
        with col_b:
            st.metric("Required Collateral", f"${decision.required_collateral:,.0f}")
        with col_c:
            st.metric("POD", f"{decision.pod:.1%}")
        
        # Reasons
        st.subheader("Decision Rationale")
        for reason in decision.reasons:
            if "approved" in reason.lower():
                st.success(f"✓ {reason}")
            else:
                st.error(f"✗ {reason}")
        
        # Conditions
        if decision.conditions:
            st.subheader("Approval Conditions")
            for condition in decision.conditions:
                st.warning(f"⚠️ {condition}")
