"""
Unit Tests for EPI Calculator
==============================

Tests for the Ethical Performance Index calculator.
"""

import pytest
from src.epi.calculator import EPICalculator, EPIScores


class TestEPICalculator:
    """Test suite for EPI Calculator."""
    
    def test_harmonic_mean_calculation(self, epi_calculator):
        """Test harmonic mean calculation."""
        # Equal values
        result = epi_calculator.harmonic_mean(0.8, 0.8)
        assert result == 0.8
        
        # Different values
        result = epi_calculator.harmonic_mean(0.9, 0.7)
        assert 0.7 < result < 0.9
        
        # Zero handling
        result = epi_calculator.harmonic_mean(0.0, 0.8)
        assert result == 0.0
    
    def test_balance_penalty(self, epi_calculator):
        """Test balance penalty calculation."""
        # Perfectly balanced
        result = epi_calculator.balance_penalty(0.8, 0.8)
        assert result == 1.0
        
        # Imbalanced
        result = epi_calculator.balance_penalty(0.9, 0.5)
        assert result < 1.0
        
        # Maximum imbalance
        result = epi_calculator.balance_penalty(1.0, 0.0)
        assert result < 0.5
    
    def test_trust_accumulator(self, epi_calculator):
        """Test trust accumulator with violations."""
        # No violations
        result = epi_calculator.trust_accumulator([])
        assert result == 1.0
        
        # Single violation
        result = epi_calculator.trust_accumulator([0.1])
        assert result == 0.9
        
        # Multiple violations
        result = epi_calculator.trust_accumulator([0.1, 0.1])
        assert result == pytest.approx(0.81, rel=0.01)
        
        # Severe violations
        result = epi_calculator.trust_accumulator([0.5, 0.5])
        assert result == 0.25
    
    def test_compute_epi_valid(self, epi_calculator, sample_epi_scores):
        """Test EPI computation with valid scores."""
        epi, valid, trace = epi_calculator.compute_epi(sample_epi_scores['valid'])
        
        assert epi >= 0.7
        assert valid is True
        assert 'hmean' in trace
        assert 'balance_penalty' in trace
        assert 'trust' in trace
        assert trace['reason'] == 'approved'
    
    def test_compute_epi_invalid(self, epi_calculator, sample_epi_scores):
        """Test EPI computation with invalid scores."""
        epi, valid, trace = epi_calculator.compute_epi(sample_epi_scores['invalid_low'])
        
        assert epi < 0.7
        assert valid is False
        assert trace['reason'] == 'rejected'
    
    def test_compute_epi_with_violations(self, epi_calculator, sample_epi_scores):
        """Test EPI computation with violations."""
        epi, valid, trace = epi_calculator.compute_epi(sample_epi_scores['with_violations'])
        
        # Violations should reduce EPI
        assert trace['trust'] < 1.0
        assert epi < 0.9  # Even with high profit/ethics, violations reduce score
    
    def test_compute_epi_imbalanced(self, epi_calculator, sample_epi_scores):
        """Test EPI computation with imbalanced profit/ethics."""
        epi, valid, trace = epi_calculator.compute_epi(sample_epi_scores['imbalanced'])
        
        # Imbalance should apply penalty
        assert trace['balance_penalty'] < 1.0
    
    def test_epi_threshold_boundary(self, epi_calculator):
        """Test EPI at threshold boundary."""
        # Just above threshold
        scores = EPIScores(profit=0.75, ethics=0.75, violations=[])
        epi, valid, _ = epi_calculator.compute_epi(scores, threshold=0.7)
        assert valid is True
        
        # Just below threshold
        scores = EPIScores(profit=0.65, ethics=0.65, violations=[])
        epi, valid, _ = epi_calculator.compute_epi(scores, threshold=0.7)
        assert valid is False
    
    def test_epi_components_range(self, epi_calculator):
        """Test that all EPI components are in valid range [0, 1]."""
        scores = EPIScores(profit=0.8, ethics=0.7, violations=[0.1])
        epi, valid, trace = epi_calculator.compute_epi(scores)
        
        assert 0 <= trace['hmean'] <= 1
        assert 0 <= trace['balance_penalty'] <= 1
        assert 0 <= trace['trust'] <= 1
        assert 0 <= epi <= 1
