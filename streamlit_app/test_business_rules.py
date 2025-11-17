"""
Unit tests for the MYPEBusinessRules engine.

import pytest
from streamlit_app.utils.business_rules import MYPEBusinessRules, RiskLevel, IndustryType
class TestMYPEBusinessRules:
    """Test suite for MYPEBusinessRules."""
    # Test data
    LOW_RISK_METRICS = {
        'dpd_mean': 10,
        'ltv': 50,
        'avg_dpd': 15,
        'collection_rate': 0.95,
        'avg_risk_severity': 0.2,
        'pod': 0.10
    }
    HIGH_RISK_DPD = {'dpd_mean': 95, 'ltv': 50, 'collection_rate': 0.9}
    HIGH_RISK_LTV = {'dpd_mean': 10, 'ltv': 85, 'collection_rate': 0.9}
    HIGH_RISK_COLLECTION = {'dpd_mean': 10, 'ltv': 50, 'collection_rate': 0.65}
    def test_classify_high_risk_when_low_risk(self):
        """Should not classify a client as high-risk if all metrics are good."""
        is_high_risk, reasons = MYPEBusinessRules.classify_high_risk(self.LOW_RISK_METRICS)
        assert not is_high_risk
        assert not reasons
    def test_classify_high_risk_due_to_dpd(self):
        """Should classify as high-risk due to high DPD."""
        is_high_risk, reasons = MYPEBusinessRules.classify_high_risk(self.HIGH_RISK_DPD)
        assert is_high_risk
        assert "DPD 95 days > 90 threshold" in reasons[0]
    def test_classify_high_risk_due_to_ltv(self):
        """Should classify as high-risk due to high LTV."""
        is_high_risk, reasons = MYPEBusinessRules.classify_high_risk(self.HIGH_RISK_LTV)
        assert "LTV 85.0% > 80% threshold" in reasons[0]
    def test_classify_high_risk_due_to_collection_rate(self):
        """Should classify as high-risk due to low collection rate."""
        is_high_risk, reasons = MYPEBusinessRules.classify_high_risk(self.HIGH_RISK_COLLECTION)
        assert "Collection rate 65.0% < 70.0% threshold" in reasons[0]
    @pytest.mark.parametrize("industry, expected_adjustment", [
        (IndustryType.TRADE, 0.95),
        (IndustryType.SERVICES, 0.95),
        (IndustryType.MANUFACTURING, 1.0),
        (IndustryType.AGRICULTURE, 1.0),
        (IndustryType.CONSTRUCTION, 1.05),
        (IndustryType.TRANSPORT, 1.05),
        (IndustryType.OTHER, 1.05),
    ])
    def test_calculate_industry_adjustment(self, industry, expected_adjustment):
        """Should return the correct risk adjustment factor for each industry."""
        adjustment = MYPEBusinessRules.calculate_industry_adjustment(industry)
        assert adjustment == pytest.approx(expected_adjustment)
    def test_check_rotation_target_meets_target(self):
        """Should confirm when rotation meets or exceeds the target."""
        rotation, meets_target, message = MYPEBusinessRules.check_rotation_target(
            total_revenue=600_000, avg_balance=100_000
        )
        assert rotation == pytest.approx(6.0)
        assert meets_target is True
        assert "meets target" in message
    def test_check_rotation_target_below_target(self):
        """Should report when rotation is below the target."""
            total_revenue=400_000, avg_balance=100_000
        assert rotation == pytest.approx(4.0)
        assert meets_target is False
        assert "below target" in message
    def test_check_rotation_target_zero_balance(self):
        """Should handle zero average balance to avoid division by zero."""
            total_revenue=100_000, avg_balance=0
        assert rotation == pytest.approx(0.0)
        assert "No balance data available" in message
    @pytest.mark.parametrize("dpd, expected_is_npl, expected_classification", [
        (200, True, "NPL - 200 days overdue"),
        (180, True, "NPL - 180 days overdue"),
        (179, False, "High Risk - 179 days overdue"),
        (90, False, "High Risk - 90 days overdue"),
        (89, False, "Medium Risk - 89 days overdue"),
        (60, False, "Medium Risk - 60 days overdue"),
        (59, False, "Watch List - 59 days overdue"),
        (30, False, "Watch List - 30 days overdue"),
        (29, False, "Current"),
        (0, False, "Current"),
    def test_classify_npl(self, dpd, expected_is_npl, expected_classification):
        """Should correctly classify accounts based on days past due."""
        is_npl, classification = MYPEBusinessRules.classify_npl(dpd)
        assert is_npl == expected_is_npl
        assert classification == expected_classification
    def test_get_industry_benchmarks_agriculture(self):
        """Should return adjusted benchmarks for specific industries like Agriculture."""
        benchmarks = MYPEBusinessRules.get_industry_benchmarks(IndustryType.AGRICULTURE)
        assert benchmarks['target_rotation'] == 3.0
        assert benchmarks['max_dpd'] == 60
    def test_get_industry_benchmarks_trade(self):
        """Should return adjusted benchmarks for industries like Trade."""
        benchmarks = MYPEBusinessRules.get_industry_benchmarks(IndustryType.TRADE)
        assert benchmarks['target_rotation'] == 6.0
        assert benchmarks['max_dpd'] == 30
    # --- Tests for evaluate_facility_approval ---
    def test_approve_micro_loan_fully_compliant(self):
        """Should approve a micro-loan that meets all criteria."""
        decision = MYPEBusinessRules.evaluate_facility_approval(
            facility_amount=25_000,
            customer_metrics=self.LOW_RISK_METRICS,
            collateral_value=30_000
        assert decision.approved is True
        assert decision.risk_level == RiskLevel.LOW
        assert "facility approved" in decision.reasons[0]
        assert "Adequate collateral coverage" in decision.reasons[1]
        assert not decision.conditions
    def test_approve_micro_loan_with_collateral_shortfall_condition(self):
        """Should approve a micro-loan with a personal guarantee condition for collateral shortfall."""
            facility_amount=40_000,
            collateral_value=30_000  # Shortfall of 10k
        assert "Recommend personal guarantee" in decision.conditions[0]
        assert "collateral shortfall: $10,000" in decision.conditions[0]
    def test_reject_small_loan_due_to_high_pod(self):
        """Should reject a small loan if the POD exceeds the tier's threshold."""
        high_pod_metrics = {**self.LOW_RISK_METRICS, 'pod': 0.40}
            facility_amount=100_000,
            customer_metrics=high_pod_metrics,
            collateral_value=120_000
        assert decision.approved is False
        assert decision.risk_level == RiskLevel.HIGH
        assert "POD 40.00% exceeds 30.00% threshold" in decision.reasons[0]
        assert decision.recommended_amount == 0
    def test_reject_medium_loan_due_to_insufficient_collateral(self):
        """Should reject a medium loan for insufficient collateral and recommend a lower amount."""
            facility_amount=250_000,
            collateral_value=300_000  # Required: 250k * 1.5 = 375k
        assert "Insufficient collateral" in decision.reasons[0]
        assert decision.recommended_amount == pytest.approx(300_000 / 1.5)  # 200k
    def test_reject_small_loan_due_to_high_risk_client(self):
        """Should reject a small or medium loan if the client is classified as high-risk."""
            facility_amount=150_000,
            customer_metrics=self.HIGH_RISK_DPD,
            collateral_value=200_000
        assert any("DPD 95 days > 90 threshold" in r for r in decision.reasons)
        assert "Enhanced monitoring required" in decision.conditions[0]
    def test_approve_but_add_e_invoice_condition(self):
        """Should add an e-invoice condition for loans over the threshold."""
            facility_amount=1_500,
            collateral_value=2_000
        assert any("E-invoice integration required" in c for c in decision.conditions)
    def test_approve_but_add_monitoring_condition_for_dpd(self):
        """Should add a monitoring condition for a client with a history of payment delays."""
        metrics_with_dpd = {**self.LOW_RISK_METRICS, 'dpd_mean': 45}
            facility_amount=20_000,
            customer_metrics=metrics_with_dpd,
            collateral_value=25_000
        assert any("recommend bi-weekly monitoring" in c for c in decision.conditions)
    def test_risk_level_classification_in_approval(self):
        """Should correctly assign a final risk level based on POD."""
        # Critical risk
        metrics_critical = {**self.LOW_RISK_METRICS, 'pod': 0.60}
            facility_amount=10_000,
            customer_metrics=metrics_critical,
            collateral_value=10_000
        assert decision.risk_level == RiskLevel.CRITICAL
        # High risk
        metrics_high = {**self.LOW_RISK_METRICS, 'pod': 0.45}
            customer_metrics=metrics_high,
