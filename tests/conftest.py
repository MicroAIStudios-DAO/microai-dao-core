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


@pytest.fixture
def sample_risk_assessments():
    """Fixture for sample risk assessments."""
    return {
        'low_risk': {
            'model_name': 'LowRiskModel',
            'model_type': 'classification',
            'use_case': 'Low risk use case',
            'impact_scope': 'individual',
            'decision_autonomy': 'human_in_loop',
            'data_sensitivity': 'public',
            'reversibility': 'reversible',
            'regulatory_requirements': 'none'
        },
        'low': {
            'impact': 0.2,
            'autonomy': 0.3,
            'data_sensitivity': 0.1,
            'reversibility': 0.9,
            'regulatory': 0.1
        },
        'medium': {
            'impact': 0.5,
            'autonomy': 0.5,
            'data_sensitivity': 0.4,
            'reversibility': 0.6,
            'regulatory': 0.4
        },
        'high': {
            'impact': 0.9,
            'autonomy': 0.8,
            'data_sensitivity': 0.9,
            'reversibility': 0.2,
            'regulatory': 0.8
        },
        'high_risk': {
            'model_name': 'HighRiskModel',
            'model_type': 'generative',
            'use_case': 'High risk use case',
            'impact_scope': 'society',
            'decision_autonomy': 'fully_autonomous',
            'data_sensitivity': 'highly_sensitive',
            'reversibility': 'permanent',
            'regulatory_requirements': 'critical'
        },
        'critical': {
            'impact': 1.0,
            'autonomy': 0.95,
            'data_sensitivity': 1.0,
            'reversibility': 0.1,
            'regulatory': 1.0
        }
    }



@pytest.fixture
def app():
    """Fixture for Flask application."""
    from api.app import app as flask_app
    flask_app.config['TESTING'] = True
    flask_app.config['JWT_SECRET_KEY'] = 'test-secret-key'
    flask_app.config['DATABASE_URL'] = 'sqlite:///:memory:'
    return flask_app


@pytest.fixture
def client(app):
    """Fixture for Flask test client."""
    return app.test_client()


@pytest.fixture
def auth_headers(client):
    """Fixture for authenticated request headers."""
    # Create a test user and get JWT token
    from api.middleware.auth import create_tokens
    tokens = create_tokens(identity='test_user', additional_claims={'role': 'admin'})
    return {
        'Authorization': f"Bearer {tokens['access_token']}",
        'Content-Type': 'application/json'
    }
