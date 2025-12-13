"""
Unit Tests for Policy Validator
================================

Tests for the policy validation engine.
"""

import pytest
from src.policy_engine.risk_classifier import RiskClassifier, RiskTier


class TestRiskClassifier:
    """Test suite for Risk Classifier."""
    
    def test_low_risk_classification(self, risk_classifier, sample_risk_assessments):
        """Test low risk model classification."""
        assessment = risk_classifier.assess_risk(**sample_risk_assessments['low_risk'])
        
        assert assessment.tier == RiskTier.LOW
        assert assessment.score <= 0.25
        assert assessment.approval_requirements['automated_approval'] is True
        assert assessment.approval_requirements['voting_required'] is False
    
    def test_high_risk_classification(self, risk_classifier, sample_risk_assessments):
        """Test high risk model classification."""
        assessment = risk_classifier.assess_risk(**sample_risk_assessments['high_risk'])
        
        assert assessment.tier in [RiskTier.HIGH, RiskTier.CRITICAL]
        assert assessment.score > 0.50
        assert assessment.approval_requirements['voting_required'] is True
        assert assessment.approval_requirements['technical_review'] is True
    
    def test_risk_factors_calculation(self, risk_classifier):
        """Test individual risk factor calculations."""
        # Impact scope
        assert risk_classifier._score_impact_scope('individual') < 0.5
        assert risk_classifier._score_impact_scope('society') > 0.8
        
        # Decision autonomy
        assert risk_classifier._score_decision_autonomy('human_in_loop') < 0.5
        assert risk_classifier._score_decision_autonomy('fully_autonomous') > 0.8
        
        # Data sensitivity
        assert risk_classifier._score_data_sensitivity('public') < 0.3
        assert risk_classifier._score_data_sensitivity('highly_sensitive') > 0.8
        
        # Reversibility
        assert risk_classifier._score_reversibility('reversible') < 0.3
        assert risk_classifier._score_reversibility('permanent') > 0.8
        
        # Regulatory
        assert risk_classifier._score_regulatory('none') < 0.2
        assert risk_classifier._score_regulatory('critical') > 0.8
    
    def test_tier_determination(self, risk_classifier):
        """Test risk tier determination from score."""
        assert risk_classifier._determine_tier(0.20) == RiskTier.LOW
        assert risk_classifier._determine_tier(0.40) == RiskTier.MEDIUM
        assert risk_classifier._determine_tier(0.60) == RiskTier.HIGH
        assert risk_classifier._determine_tier(0.85) == RiskTier.CRITICAL
    
    def test_approval_requirements(self, risk_classifier):
        """Test approval requirements for different tiers."""
        # Low risk
        low_info = risk_classifier.get_tier_info(RiskTier.LOW)
        assert low_info['approval_requirements']['automated_approval'] is True
        
        # High risk
        high_info = risk_classifier.get_tier_info(RiskTier.HIGH)
        assert high_info['approval_requirements']['ethics_review'] is True
        assert high_info['approval_requirements']['quorum'] >= 0.50
        
        # Critical risk
        critical_info = risk_classifier.get_tier_info(RiskTier.CRITICAL)
        assert critical_info['approval_requirements']['external_audit'] is True
        assert critical_info['approval_requirements']['quorum'] >= 0.75
    
    def test_recommendations_generation(self, risk_classifier):
        """Test recommendation generation."""
        assessment = risk_classifier.assess_risk(
            model_name='TestModel',
            model_type='classification',
            use_case='Test use case',
            impact_scope='society',
            decision_autonomy='fully_autonomous',
            data_sensitivity='highly_sensitive',
            reversibility='permanent',
            regulatory_requirements='critical'
        )
        
        assert len(assessment.recommendations) > 0
        assert any('audit' in rec.lower() for rec in assessment.recommendations)
    
    def test_reasoning_generation(self, risk_classifier):
        """Test reasoning generation."""
        assessment = risk_classifier.assess_risk(
            model_name='TestModel',
            model_type='classification',
            use_case='Test use case',
            impact_scope='individual',
            decision_autonomy='automated',
            data_sensitivity='private',
            reversibility='reversible',
            regulatory_requirements='moderate'
        )
        
        assert 'TestModel' in assessment.reasoning
        assert 'risk' in assessment.reasoning.lower()
        assert len(assessment.reasoning) > 50  # Substantial reasoning
    
    def test_export_assessment(self, risk_classifier):
        """Test assessment export to JSON."""
        assessment = risk_classifier.assess_risk(
            model_name='TestModel',
            model_type='classification',
            use_case='Test',
            impact_scope='individual',
            decision_autonomy='automated',
            data_sensitivity='public',
            reversibility='reversible',
            regulatory_requirements='none'
        )
        
        json_export = risk_classifier.export_assessment(assessment)
        
        assert 'tier' in json_export
        assert 'risk_score' in json_export
        assert 'factors' in json_export
        assert 'approval_requirements' in json_export
