"""
Feature Engineering Module - 28+ Dimensions
Transforms raw data into ML-ready features for predictive analytics

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from scipy import stats

class FeatureEngineer:
    """Enterprise-grade feature engineering for financial analytics"""
    
    # Customer type mappings
    CUSTOMER_TYPES  {
        'B2B': ['empresa', 'corporativo', 'business', 'b2b'],
        'B2C': ['persona', 'individual', 'consumer', 'b2c'],
        'B2G': ['gobierno', 'government', 'publico', 'b2g', 'municipal', 'estatal']
    }
    
    # Segmentation criteria (A-F based on performance)
    SEGMENTATION_THRESHOLDS  {
        'A': {'dpd_max': 0, 'utilization_min': 0.5, 'payment_ratio_min': 1.0},
        'B': {'dpd_max': 15, 'utilization_min': 0.3, 'payment_ratio_min': 0.9},
        'C': {'dpd_max': 30, 'utilization_min': 0.2, 'payment_ratio_min': 0.75},
        'D': {'dpd_max': 60, 'utilization_min': 0.1, 'payment_ratio_min': 0.5},
        'E': {'dpd_max': 90, 'utilization_min': 0.05, 'payment_ratio_min': 0.25},
        'F': {'dpd_max': float('inf'), 'utilization_min': 0, 'payment_ratio_min': 0}
    
    # DPD buckets for delinquency analysis
    DPD_BUCKETS  [0, 1, 15, 30, 45, 60, 90, 120, 180, float('inf')]
    DPD_LABELS  ['Current', '1-14', '15-29', '30-44', '45-59', '60-89', '90-119', '120-179', '180+']
    
    def classify_customer_type(self, customer_name: str, customer_data: Dict) - str:
        """Classify customer as B2B, B2C, or B2G - Requirement 2"""
        name_lower  customer_name.lower()
        
        for customer_type, keywords in self.CUSTOMER_TYPES.items():
            if any(keyword in name_lower for keyword in keywords):
                return customer_type
        
        return 'B2C'
    
    def calculate_segmentation(self, customer_metrics: Dict) - str:
        """Segment customers A-F based on performance - Requirement 2"""
        dpd  customer_metrics.get('avg_dpd', 0)
        utilization  customer_metrics.get('utilization', 0)
        payment_ratio  customer_metrics.get('payment_ratio', 0)
        
        for segment, thresholds in self.SEGMENTATION_THRESHOLDS.items():
            if (dpd  thresholds['dpd_max'] and
                utilization  thresholds['utilization_min'] and
                payment_ratio  thresholds['payment_ratio_min']):
                return segment
        
        return 'F'
    
    def bucket_dpd(self, dpd_value: float) - str:
        """Bucket DPD into categories - Requirement 2"""
        for i, threshold in enumerate(self.DPD_BUCKETS[1:]):
            if dpd_value  threshold:
                return self.DPD_LABELS[i]
        return self.DPD_LABELS[-1]
    
    def calculate_dpd_statistics(self, dpd_series: pd.Series) - Dict:
        """Calculate DPD statistics - Requirement 2"""
        return {
            'dpd_max': float(dpd_series.max()) if len(dpd_series)  0 else 0,
            'dpd_mean': float(dpd_series.mean()) if len(dpd_series)  0 else 0,
            'dpd_median': float(dpd_series.median()) if len(dpd_series)  0 else 0,
            'dpd_std': float(dpd_series.std()) if len(dpd_series)  0 else 0,
        }
    
    def calculate_utilization(self, balance: float, limit: float) - float:
        """Calculate credit utilization - Requirement 2"""
        if limit  0 or pd.isna(limit):
            return 0.0
        return min(balance / limit, 1.0)
    
    def calculate_weighted_apr(self, facilities: List[Dict]) - float:
        """Calculate weighted average APR - Requirement 2"""
        total_balance  sum(f.get('balance', 0) for f in facilities)
        if total_balance  0:
        
        weighted_sum  sum(f.get('balance', 0) * f.get('apr', 0) for f in facilities)
        return weighted_sum / total_balance
    
    def calculate_z_scores(self, df: pd.DataFrame, metrics: List[str]) - pd.DataFrame:
        """Calculate Z-scores - Requirement 2"""
        for metric in metrics:
            if metric in df.columns:
                mean  df[metric].mean()
                std  df[metric].std()
                if std  0:
                    df[f'{metric}_zscore']  (df[metric] - mean) / std
                else:
                    df[f'{metric}_zscore']  0
        return df
