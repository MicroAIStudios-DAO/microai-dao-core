"""
Policy Validator
================
Multi-factor validation for governance decisions.

Implements:
- Compliance screening (sanctions, regulations)
- Risk assessment (concentration, exposure)
- EPI threshold enforcement
- Audit trail generation
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

from ..epi import EPICalculator, EPIScores
from ..trust_stack import EventLogger


class ValidationStatus(Enum):
    """Status of validation result."""
    APPROVED = "approved"
    REJECTED = "rejected"
    PENDING_REVIEW = "pending_review"
    REQUIRES_MODIFICATION = "requires_modification"


@dataclass
class ValidationResult:
    """Result of policy validation."""
    status: ValidationStatus
    epi_score: float
    epi_valid: bool
    compliance_passed: bool
    risk_acceptable: bool
    reason: str
    trace: Dict[str, Any] = field(default_factory=dict)
    recommendations: List[str] = field(default_factory=list)
    timestamp: datetime = field(default_factory=datetime.now)


class PolicyValidator:
    """
    Multi-factor policy validation engine.

    Validates intents/proposals through:
    1. Compliance checks (sanctions, regulations)
    2. Risk assessment (concentration, exposure)
    3. EPI calculation and threshold enforcement
    """

    # Default sanctioned entities (would be loaded from external source)
    DEFAULT_SANCTIONED_ENTITIES = [
        "OFAC_SANCTIONED",
        "EU_SANCTIONED",
        "UN_SANCTIONED"
    ]

    # Risk thresholds
    DEFAULT_RISK_THRESHOLD = 0.5
    DEFAULT_CONCENTRATION_LIMIT = 0.3

    def __init__(
        self,
        epi_threshold: float = 0.7,
        risk_threshold: float = 0.5,
        concentration_limit: float = 0.3,
        sanctioned_entities: Optional[List[str]] = None
    ):
        """
        Initialize policy validator.

        Args:
            epi_threshold: Minimum EPI score for approval
            risk_threshold: Maximum acceptable risk score
            concentration_limit: Maximum concentration ratio
            sanctioned_entities: List of sanctioned entity identifiers
        """
        self.epi_calculator = EPICalculator(threshold=epi_threshold)
        self.epi_threshold = epi_threshold
        self.risk_threshold = risk_threshold
        self.concentration_limit = concentration_limit
        self.sanctioned_entities = sanctioned_entities or self.DEFAULT_SANCTIONED_ENTITIES
        self.event_logger = EventLogger()  # Trust Stack integration

    def validate_intent(self, intent: Dict[str, Any]) -> ValidationResult:
        """
        Validate an intent/proposal through all policy checks.

        Args:
            intent: Dictionary containing:
                - action: Type of action
                - amount: Financial amount (optional)
                - target: Target entity (optional)
                - ethics_scores: Dict of ethical metrics
                - profitability: Expected ROI/profitability
                - exposure_ratio: Portfolio exposure ratio
                - violations: List of past violation severities
                - metadata: Additional context

        Returns:
            ValidationResult with full analysis
        """
        trace = {}

        # Step 1: Compliance check
        compliance_result = self._check_compliance(intent)
        trace['compliance'] = compliance_result

        if not compliance_result['passed']:
            return ValidationResult(
                status=ValidationStatus.REJECTED,
                epi_score=0.0,
                epi_valid=False,
                compliance_passed=False,
                risk_acceptable=False,
                reason=compliance_result['reason'],
                trace=trace,
                recommendations=['Address compliance issues before resubmission']
            )

        # Step 2: Risk assessment
        risk_result = self._assess_risk(intent)
        trace['risk'] = risk_result

        # Step 3: EPI calculation
        epi_result = self._calculate_epi(intent)
        trace['epi'] = {
            'score': epi_result.epi_score,
            'valid': epi_result.is_valid,
            'ethical_component': epi_result.ethical_component,
            'profitability_component': epi_result.profitability_component,
            'recommendation': epi_result.recommendation
        }

        # Determine final status
        status, reason, recommendations = self._determine_status(
            compliance_result, risk_result, epi_result
        )

        return ValidationResult(
            status=status,
            epi_score=epi_result.epi_score,
            epi_valid=epi_result.is_valid,
            compliance_passed=compliance_result['passed'],
            risk_acceptable=risk_result['acceptable'],
            reason=reason,
            trace=trace,
            recommendations=recommendations
        )

    def _check_compliance(self, intent: Dict[str, Any]) -> Dict[str, Any]:
        """
        Check compliance with regulations and sanctions.

        Returns:
            Dict with 'passed' bool and 'reason' string
        """
        # Extract target entity from intent
        target = intent.get('target', '')
        metadata = intent.get('metadata', {})
        entities = metadata.get('involved_entities', [])

        # Check against sanctioned list
        for entity in [target] + entities:
            if entity and any(s in str(entity).upper() for s in self.sanctioned_entities):
                return {
                    'passed': False,
                    'reason': f'Entity {entity} appears on sanctions list',
                    'flagged_entity': entity
                }

        # Check for regulatory flags in metadata
        if metadata.get('regulatory_hold', False):
            return {
                'passed': False,
                'reason': 'Intent is under regulatory hold',
                'flagged_entity': None
            }

        return {
            'passed': True,
            'reason': 'No compliance issues detected',
            'flagged_entity': None
        }

    def _assess_risk(self, intent: Dict[str, Any]) -> Dict[str, Any]:
        """
        Assess risk based on exposure and concentration.

        Returns:
            Dict with risk metrics and acceptability
        """
        exposure_ratio = intent.get('exposure_ratio', 0.0)
        amount = intent.get('amount', 0)
        total_portfolio = intent.get('total_portfolio', amount * 10)  # Default assumption

        # Calculate concentration
        if total_portfolio > 0:
            concentration = amount / total_portfolio
        else:
            concentration = 0.0

        # Calculate risk score (higher = riskier)
        risk_score = 1.0 - min(exposure_ratio, 1.0)
        concentration_risk = concentration / self.concentration_limit if self.concentration_limit > 0 else 0

        # Combined risk assessment
        combined_risk = (risk_score * 0.6 + concentration_risk * 0.4)
        acceptable = combined_risk <= self.risk_threshold and concentration <= self.concentration_limit

        return {
            'acceptable': acceptable,
            'risk_score': combined_risk,
            'concentration': concentration,
            'exposure_ratio': exposure_ratio,
            'reason': 'Risk within acceptable limits' if acceptable else 'Risk exceeds thresholds'
        }

    def _calculate_epi(self, intent: Dict[str, Any]) -> Any:
        """
        Calculate EPI score from intent data.

        Returns:
            EPIResult from calculator
        """
        # Extract ethics scores
        ethics_data = intent.get('ethics_scores', {})
        ethics_score = sum(ethics_data.values()) / len(ethics_data) if ethics_data else 0.7

        # Extract profitability
        profitability = intent.get('profitability', intent.get('roi', 0.5))

        # Extract violations
        violations = intent.get('violations', [])

        # Build EPIScores
        scores = EPIScores(
            profit=profitability,
            ethics=ethics_score,
            violations=violations,
            transparency_score=ethics_data.get('transparency', 0.7),
            sustainability_score=ethics_data.get('sustainability', 0.6),
            compliance_score=ethics_data.get('compliance', 0.8)
        )

        return self.epi_calculator.compute_epi(scores)

    def _determine_status(
        self,
        compliance: Dict[str, Any],
        risk: Dict[str, Any],
        epi_result: Any
    ) -> tuple:
        """
        Determine final validation status and recommendations.

        Returns:
            Tuple of (status, reason, recommendations)
        """
        recommendations = []

        # All checks passed
        if compliance['passed'] and risk['acceptable'] and epi_result.is_valid:
            if epi_result.recommendation == 'APPROVE':
                return (
                    ValidationStatus.APPROVED,
                    'All validation checks passed',
                    ['Proceed with implementation']
                )
            elif epi_result.recommendation == 'MODIFY':
                recommendations.extend(epi_result.optimization_suggestions)
                return (
                    ValidationStatus.REQUIRES_MODIFICATION,
                    'Approved with recommended modifications',
                    recommendations
                )

        # Risk issues
        if not risk['acceptable']:
            recommendations.append('Reduce exposure or concentration')
            recommendations.append(f'Current concentration: {risk["concentration"]:.1%}')
            return (
                ValidationStatus.PENDING_REVIEW,
                f'Risk assessment failed: {risk["reason"]}',
                recommendations
            )

        # EPI issues
        if not epi_result.is_valid:
            recommendations.extend(epi_result.optimization_suggestions)
            return (
                ValidationStatus.REJECTED,
                f'EPI validation failed: {epi_result.reason}',
                recommendations
            )

        # Default rejection
        return (
            ValidationStatus.REJECTED,
            'Validation failed',
            ['Review all requirements and resubmit']
        )

    def validate_batch(self, intents: List[Dict[str, Any]]) -> List[ValidationResult]:
        """Validate multiple intents."""
        return [self.validate_intent(intent) for intent in intents]

    def get_validation_summary(self, results: List[ValidationResult]) -> Dict[str, Any]:
        """Generate summary of validation results."""
        approved = sum(1 for r in results if r.status == ValidationStatus.APPROVED)
        rejected = sum(1 for r in results if r.status == ValidationStatus.REJECTED)
        pending = sum(1 for r in results if r.status == ValidationStatus.PENDING_REVIEW)
        modify = sum(1 for r in results if r.status == ValidationStatus.REQUIRES_MODIFICATION)

        avg_epi = sum(r.epi_score for r in results) / len(results) if results else 0

        return {
            'total': len(results),
            'approved': approved,
            'rejected': rejected,
            'pending_review': pending,
            'requires_modification': modify,
            'approval_rate': approved / len(results) if results else 0,
            'average_epi_score': avg_epi
        }
