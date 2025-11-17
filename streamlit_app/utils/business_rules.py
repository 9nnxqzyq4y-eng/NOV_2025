"""
Business Rules Engine - MYPE 2025 Standards
Implements approval thresholds, risk classification, and industry-specific logic
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

class RiskLevel(Enum):
    """Risk classification levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class IndustryType(Enum):
    """MYPE industry classifications"""
    TRADE = "trade"
    SERVICES = "services"
    MANUFACTURING = "manufacturing"
    AGRICULTURE = "agriculture"
    CONSTRUCTION = "construction"
    TRANSPORT = "transport"
    OTHER = "other"

@dataclass
class ApprovalDecision:
    """Loan approval decision with reasoning"""
    approved: bool
    risk_level: RiskLevel
    recommended_amount: float
    required_collateral: float
    conditions: List[str]
    reasons: List[str]
    pod: float  # Probability of Default

class MYPEBusinessRules:
    """
    Business rules based on MYPE 2025 report analysis
    
    Key Statistics from Report:
    - MYPE contribution to GDP: 48.8%
    - Typical facility size: $5K-$50K for micro, $50K-$200K for small
    - E-invoice threshold: $1K (Hacienda compliance)
    - Target rotation: 5.5x
    - NPL threshold: 180+ days
    """
    
    FACILITY_THRESHOLDS = {
        'micro': {
            'max_amount': 50_000,
            'max_pod': 0.35,
            'min_collateral_ratio': 1.0,
            'risk_level': RiskLevel.LOW
        },
        'small': {
            'max_amount': 200_000,
            'max_pod': 0.30,
            'min_collateral_ratio': 1.2,
            'risk_level': RiskLevel.MEDIUM
        },
        'medium': {
            'max_amount': float('inf'),
            'max_pod': 0.20,
            'min_collateral_ratio': 1.5,
            'risk_level': RiskLevel.HIGH
        }
    }
    
    # High-risk client criteria (MYPE-specific)
    HIGH_RISK_CRITERIA = {
        'dpd_threshold': 90,  # Days past due
        'ltv_threshold': 80,  # Loan-to-value %
        'avg_dpd_threshold': 60,
        'collection_rate_threshold': 0.70,  # 70%
        'avg_risk_severity_threshold': 0.7
    }
    
    # Industry GDP contribution (from MYPE report)
    INDUSTRY_GDP_CONTRIBUTION = {
        IndustryType.TRADE: 0.25,  # 25%
        IndustryType.SERVICES: 0.30,  # 30%
        IndustryType.MANUFACTURING: 0.20,  # 20%
        IndustryType.AGRICULTURE: 0.15,  # 15%
        IndustryType.CONSTRUCTION: 0.07,  # 7%
        IndustryType.TRANSPORT: 0.03,  # 3%
    }
    
    # E-invoice compliance threshold (Hacienda)
    EINVOICE_THRESHOLD = 1_000  # USD
    
    # Target metrics
    TARGET_ROTATION = 5.5  # Times per year
    NPL_DAYS_THRESHOLD = 180  # Days for NPL classification
    TARGET_COLLECTION_RATE = 0.85  # 85%
    
    @staticmethod
    def classify_high_risk(customer_metrics: Dict) -> Tuple[bool, List[str]]:
        """
        Classify if customer is high-risk based on MYPE criteria
        
        Args:
            customer_metrics: Dict with dpd, ltv, collection_rate, etc.
            
        Returns:
            (is_high_risk, reasons)
        """
        is_high_risk = False
        reasons = []
        
        criteria = MYPEBusinessRules.HIGH_RISK_CRITERIA
        
        # Check DPD
        if customer_metrics.get('dpd_mean', 0) > criteria['dpd_threshold']:
            is_high_risk = True
            reasons.append(f"DPD {customer_metrics['dpd_mean']:.0f} days > {criteria['dpd_threshold']} threshold")
        
        # Check LTV
        if customer_metrics.get('ltv', 0) > criteria['ltv_threshold']:
            is_high_risk = True
            reasons.append(f"LTV {customer_metrics['ltv']:.1f}% > {criteria['ltv_threshold']}% threshold")
        
        # Check average DPD
        if customer_metrics.get('avg_dpd', 0) > criteria['avg_dpd_threshold']:
            is_high_risk = True
            reasons.append(f"Avg DPD {customer_metrics['avg_dpd']:.0f} > {criteria['avg_dpd_threshold']} threshold")
        
        # Check collection rate
        if customer_metrics.get('collection_rate', 1.0) < criteria['collection_rate_threshold']:
            is_high_risk = True
            reasons.append(f"Collection rate {customer_metrics['collection_rate']*100:.1f}% < {criteria['collection_rate_threshold']*100}% threshold")
        
        # Check risk severity
        if customer_metrics.get('avg_risk_severity', 0) > criteria['avg_risk_severity_threshold']:
            is_high_risk = True
            reasons.append(f"Risk severity {customer_metrics['avg_risk_severity']:.2f} > {criteria['avg_risk_severity_threshold']} threshold")
        
        return is_high_risk, reasons
    
    @staticmethod
    def evaluate_facility_approval(
        facility_amount: float,
        customer_metrics: Dict,
        collateral_value: float = 0.0
    ) -> ApprovalDecision:
        """Evaluate facility approval based on amount and risk profile"""
        pod = customer_metrics.get('pod', customer_metrics.get('default_risk_score', 0.5))
        # Determine facility tier
        if facility_amount <= MYPEBusinessRules.FACILITY_THRESHOLDS['micro']['max_amount']:
            tier = 'micro'
        elif facility_amount <= MYPEBusinessRules.FACILITY_THRESHOLDS['small']['max_amount']:
            tier = 'small'
        else:
            tier = 'medium'
        
        thresholds = MYPEBusinessRules.FACILITY_THRESHOLDS[tier]
        
        # Evaluation criteria
        conditions = []
        reasons = []
        approved = True
        recommended_amount = facility_amount
        
        # Check POD threshold
        if pod > thresholds['max_pod']:
            approved = False
            reasons.append(f"POD {pod:.2%} exceeds {thresholds['max_pod']:.2%} threshold for {tier} facilities")
            recommended_amount = 0
        
        # Check collateral requirements
        required_collateral = facility_amount * thresholds['min_collateral_ratio']
        if collateral_value < required_collateral:
            if tier == 'micro':
                conditions.append(f"Recommend personal guarantee (collateral shortfall: ${required_collateral - collateral_value:,.0f})")
            else:
                approved = False
                reasons.append(f"Insufficient collateral: ${collateral_value:,.0f} < ${required_collateral:,.0f} required")
                recommended_amount = collateral_value / thresholds['min_collateral_ratio']
        
        # Check high-risk classification
        is_high_risk, risk_reasons = MYPEBusinessRules.classify_high_risk(customer_metrics)
        if is_high_risk:
            if tier in ['small', 'medium']:
                approved = False
                reasons.extend(risk_reasons)
                conditions.append("Enhanced monitoring required due to risk flags")
        
        # Additional conditions based on metrics
        if customer_metrics.get('collection_rate', 1.0) < MYPEBusinessRules.TARGET_COLLECTION_RATE:
            conditions.append(f"Collection rate {customer_metrics['collection_rate']*100:.1f}% below target {MYPEBusinessRules.TARGET_COLLECTION_RATE*100}%")
        
        if customer_metrics.get('dpd_mean', 0) > 30:
            conditions.append("Payment history shows delays - recommend bi-weekly monitoring")
        
        # E-invoice requirement
        if facility_amount >= MYPEBusinessRules.EINVOICE_THRESHOLD:
            conditions.append(f"E-invoice integration required (Hacienda compliance for amounts ≥ ${MYPEBusinessRules.EINVOICE_THRESHOLD:,.0f})")
        
        # Determine final risk level
        if pod <= 0.15:
            risk_level = RiskLevel.LOW
        elif pod <= 0.30:
            risk_level = RiskLevel.MEDIUM
        elif pod <= 0.50:
            risk_level = RiskLevel.HIGH
        else:
            risk_level = RiskLevel.CRITICAL
        
        # Success reasons
        if approved:
            reasons.append(f"{tier.title()} facility approved - POD {pod:.2%} within acceptable range")
            if collateral_value >= required_collateral:
                reasons.append(f"Adequate collateral coverage: {collateral_value/facility_amount:.1f}x")
        
        return ApprovalDecision(
            approved=approved,
            risk_level=risk_level,
            recommended_amount=recommended_amount,
            required_collateral=required_collateral,
            conditions=conditions,
            reasons=reasons,
            pod=pod
        )
    
    @staticmethod
    def calculate_industry_adjustment(industry: IndustryType) -> float:
        """
        Calculate risk adjustment factor based on industry.
        Higher GDP contribution -> lower adjustment (lower risk).
        """
        contribution = MYPEBusinessRules.INDUSTRY_GDP_CONTRIBUTION.get(industry, 0.05) # Industries with higher GDP contribution get favorable adjustment
        if contribution >= 0.25: # Trade, Services
            return 0.95 # 5% risk reduction
        elif contribution >= 0.15: # Manufacturing, Agriculture
            return 1.0 # Neutral
        else: # Construction, Transport, Other
            return 1.05 # 5% risk increase
    
    @staticmethod
    def check_rotation_target(
        total_revenue: float,
        avg_balance: float
    ) -> Tuple[float, bool, str]:
        """Check if customer meets rotation target (5.5x)"""
        if avg_balance <= 0:
            return 0.0, False, "No balance data available"
        
        rotation = total_revenue / avg_balance
        meets_target = rotation >= MYPEBusinessRules.TARGET_ROTATION
        
        if meets_target:
            message = f"Rotation {rotation:.1f}x meets target {MYPEBusinessRules.TARGET_ROTATION}x ✓"
        else:
            gap = MYPEBusinessRules.TARGET_ROTATION - rotation
            message = f"Rotation {rotation:.1f}x below target by {gap:.1f}x"
        
        return rotation, meets_target, message
    
    @staticmethod
    def classify_npl(dpd: int) -> Tuple[bool, str]:
        """Classify if account is Non-Performing Loan (NPL)"""
        if dpd >= MYPEBusinessRules.NPL_DAYS_THRESHOLD:
            return True, f"NPL - {dpd} days overdue"
        elif dpd >= 90:
            return False, f"High Risk - {dpd} days overdue"
        elif dpd >= 60:
            return False, f"Medium Risk - {dpd} days overdue"
        elif dpd >= 30:
            return False, f"Watch List - {dpd} days overdue"
        else:
            return False, "Current"
    
    @staticmethod
    def get_industry_benchmarks(industry: IndustryType) -> Dict:
        """Get industry-specific benchmarks"""
        # Base benchmarks from MYPE report
        benchmarks = {
            'target_rotation': MYPEBusinessRules.TARGET_ROTATION,
            'target_collection_rate': MYPEBusinessRules.TARGET_COLLECTION_RATE,
            'max_dpd': 30,
            'gdp_contribution': MYPEBusinessRules.INDUSTRY_GDP_CONTRIBUTION.get(industry, 0.05)
        }
        
        # Industry-specific adjustments
        if industry == IndustryType.TRADE:
            benchmarks['target_rotation'] = 6.0  # Higher turnover
            benchmarks['typical_facility_size'] = 25_000
        elif industry == IndustryType.SERVICES:
            benchmarks['target_rotation'] = 5.0
            benchmarks['typical_facility_size'] = 30_000
        elif industry == IndustryType.MANUFACTURING:
            benchmarks['target_rotation'] = 4.5  # Longer cycles
            benchmarks['typical_facility_size'] = 75_000
        elif industry == IndustryType.AGRICULTURE:
            benchmarks['target_rotation'] = 3.0  # Seasonal
            benchmarks['typical_facility_size'] = 40_000
            benchmarks['max_dpd'] = 60  # More tolerance for seasonal cash flow
        
        return benchmarks
