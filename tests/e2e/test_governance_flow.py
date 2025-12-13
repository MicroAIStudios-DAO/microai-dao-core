"""
End-to-End Tests for Governance Flow
=====================================

Tests for complete governance workflows from proposal to execution.
"""

import pytest
from datetime import datetime, timedelta


class TestCompleteGovernanceFlow:
    """Test complete governance flow."""
    
    def test_model_deployment_workflow(self):
        """
        Test complete model deployment workflow:
        1. Risk assessment
        2. Model registration
        3. EPI validation
        4. Proposal creation
        5. Voting
        6. Execution
        7. Trust logging
        """
        # Step 1: Risk Assessment
        from src.policy_engine.risk_classifier import RiskClassifier
        
        classifier = RiskClassifier()
        assessment = classifier.assess_risk(
            model_name='TestAI',
            model_type='classification',
            use_case='Customer service automation',
            impact_scope='individual',
            decision_autonomy='automated',
            data_sensitivity='private',
            reversibility='reversible',
            regulatory_requirements='moderate'
        )
        
        assert assessment.tier is not None
        assert assessment.score > 0
        
        # Step 2: Model Registration
        from src.ai_c_suite.model_registry import ModelRegistry
        
        registry = ModelRegistry(db_path=":memory:")
        model_id = registry.register_model(
            name='TestAI',
            model_type='classification',
            description='Test AI model',
            use_case='Customer service',
            risk_tier=assessment.tier.value,
            tags=['test', 'customer-service']
        )
        
        assert model_id is not None
        
        # Step 3: EPI Validation
        from src.epi.calculator import EPICalculator, EPIScores
        
        calculator = EPICalculator()
        scores = EPIScores(profit=0.85, ethics=0.80, violations=[])
        epi, valid, trace = calculator.compute_epi(scores)
        
        assert valid is True
        assert epi >= 0.7
        
        # Step 4: Proposal Creation (would be via API)
        # Step 5: Voting (would be via API)
        # Step 6: Execution (would be via smart contract)
        
        # Step 7: Trust Logging
        from src.trust_stack import EventLogger
        
        logger = EventLogger(db_path=":memory:")
        event = logger.log_event(
            event_type='model_deployment',
            agent_id='test-agent',
            input_data={'model_id': model_id},
            output_data={'status': 'deployed'},
            metadata={'epi_score': epi, 'risk_tier': assessment.tier.value}
        )
        
        assert event.id is not None
        assert event.signature is not None
    
    def test_high_risk_model_workflow(self):
        """
        Test workflow for high-risk model requiring guardian approval.
        """
        from src.policy_engine.risk_classifier import RiskClassifier, RiskTier
        
        classifier = RiskClassifier()
        assessment = classifier.assess_risk(
            model_name='CreditScoringAI',
            model_type='classification',
            use_case='Credit scoring',
            impact_scope='individual',
            decision_autonomy='fully_autonomous',
            data_sensitivity='highly_sensitive',
            reversibility='difficult',
            regulatory_requirements='critical'
        )
        
        # Should be high or critical risk
        assert assessment.tier in [RiskTier.HIGH, RiskTier.CRITICAL]
        
        # Should require voting and reviews
        assert assessment.approval_requirements['voting_required'] is True
        assert assessment.approval_requirements['technical_review'] is True
        assert assessment.approval_requirements['ethics_review'] is True
    
    def test_epi_rejection_workflow(self):
        """
        Test workflow when EPI validation fails.
        """
        from src.epi.calculator import EPICalculator, EPIScores
        
        calculator = EPICalculator()
        
        # Low ethics score
        scores = EPIScores(profit=0.90, ethics=0.40, violations=[])
        epi, valid, trace = calculator.compute_epi(scores)
        
        assert valid is False
        assert trace['reason'] == 'rejected'
        
        # Model should not be deployed
        # Proposal should be automatically rejected
    
    def test_trust_verification_workflow(self):
        """
        Test complete trust verification workflow.
        """
        from src.trust_stack import EventLogger
        from src.trust_stack.verifier import ProofVerifier
        
        # Log event
        logger = EventLogger(db_path=":memory:")
        event = logger.log_event(
            event_type='test_decision',
            agent_id='test-agent',
            input_data={'test': 'input'},
            output_data={'test': 'output'},
            metadata={'epi_score': 0.85}
        )
        
        # Generate proof
        verifier = ProofVerifier(db_path=":memory:")
        # Note: This would need the event to be in the verifier's database
        # In a real scenario, they would share the same database
        
        # Verify event (would check signature, hash, etc.)
        assert event.signature is not None
        assert event.input_hash is not None
        assert event.output_hash is not None
    
    def test_guardian_intervention_workflow(self):
        """
        Test guardian intervention in governance.
        """
        from src.trust_stack.guardian_system import GuardianSystem
        
        guardian_system = GuardianSystem()
        
        # Add guardian
        guardian_system.add_guardian(
            guardian_id='guardian-1',
            name='Test Guardian',
            role='Class A',
            wallet_address='0x1234567890123456789012345678901234567890'
        )
        
        # Guardian vetoes a proposal
        result = guardian_system.veto_proposal(
            guardian_id='guardian-1',
            proposal_id='test-proposal-123',
            reason='Safety concerns'
        )
        
        assert result['success'] is True
        assert result['action'] == 'veto'
    
    def test_multi_agent_coordination(self):
        """
        Test coordination between CEO-AI and CFO-AI.
        """
        # This would test:
        # 1. CEO-AI proposes strategic initiative
        # 2. CFO-AI evaluates financial impact
        # 3. Both decisions logged to Trust Stack
        # 4. EPI validation for both
        # 5. Proposal created if both pass
        pass
    
    def test_compliance_reporting_workflow(self):
        """
        Test compliance reporting and attestation generation.
        """
        from src.trust_stack.attestation import AttestationGenerator
        
        generator = AttestationGenerator(db_path=":memory:")
        
        # Generate attestation
        attestation = generator.generate_attestation(
            model_id='test-model',
            version='1.0.0',
            attestation_type='deployment',
            metadata={'compliance': 'SOC2'}
        )
        
        assert attestation.id is not None
        assert attestation.signature is not None
        assert 'model_card' in attestation.content
