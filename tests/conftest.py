"""
Pytest Configuration and Fixtures
==================================

Shared fixtures for all tests.
"""

import pytest
import sys
sys.path.insert(0, '/home/ubuntu/microai-dao-core')

from src.epi.calculator import EPICalculator, EPIScores
from src.policy_engine.risk_classifier import RiskClassifier
from src.ai_c_suite.model_registry import ModelRegistry
from src.trust_stack import EventLogger


@pytest.fixture
def epi_calculator():
    """Fixture for EPI calculator."""
    return EPICalculator()


@pytest.fixture
def risk_classifier():
    """Fixture for risk classifier."""
    return RiskClassifier()


@pytest.fixture
def model_registry():
    """Fixture for model registry with test database."""
    return ModelRegistry(db_path=":memory:")  # In-memory database for tests


@pytest.fixture
def event_logger():
    """Fixture for event logger with test database."""
    return EventLogger(db_path=":memory:")


@pytest.fixture
def sample_epi_scores():
    """Fixture for sample EPI scores."""
    return {
        'valid': EPIScores(profit=0.85, ethics=0.80, violations=[]),
        'invalid_low': EPIScores(profit=0.50, ethics=0.40, violations=[]),
        'with_violations': EPIScores(profit=0.90, ethics=0.85, violations=[0.1, 0.05]),
        'imbalanced': EPIScores(profit=0.95, ethics=0.50, violations=[])
    }
