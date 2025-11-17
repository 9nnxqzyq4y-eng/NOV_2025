"""KPI calculation engine for financial analytics"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional

class KPIEngine:
    """Calculate all financial KPIs - Requirement 3"""
    
    def calculate_aum(self, portfolios: pd.DataFrame) - float:
        """Assets Under Management"""
        return portfolios['balance'].sum() if not portfolios.empty else 0
    
    def calculate_active_clients(self, customers: pd.DataFrame) - int:
        """Count of active clients"""
        return len(customers[customers.get('is_active', True)])
    
    def calculate_churn_rate(self, customers: pd.DataFrame, period_days: int  90) - float:
        """Churn rate calculation"""
        if customers.empty:
            return 0
        
        cutoff_date  datetime.now() - timedelta(daysperiod_days)
        inactive  customers[customers['last_activity_date']  cutoff_date]
        return len(inactive) / len(customers) * 100
    
    def calculate_default_rate(self, risk_events: pd.DataFrame) - float:
        """Default rate (DPD  90)"""
        if risk_events.empty:
        return len(risk_events[risk_events['dpd']  90]) / len(risk_events) * 100
    
    def calculate_ltv_cac(self, customers: pd.DataFrame, channel: Optional[str]  None) - Dict:
        """LTV:CAC ratio by channel"""
            return {}
        
        if channel:
            customers  customers[customers['channel']  channel]
        
        ltv  customers['total_revenue'].sum()
        cac  customers['acquisition_cost'].sum()
        
        return {
            'ltv': ltv,
            'cac': cac,
            'ratio': ltv / cac if cac  0 else 0
        }
    
    def calculate_nrr(self, revenue: pd.DataFrame) - float:
        """Net Revenue Retention"""
        if revenue.empty:
        
        current_month  revenue[revenue['month']  revenue['month'].max()]
        previous_month  revenue[revenue['month']  revenue['month'].max() - 1]
        
        current_total  current_month['revenue'].sum()
        previous_total  previous_month['revenue'].sum()
        
        return (current_total / previous_total * 100) if previous_total  0 else 0
