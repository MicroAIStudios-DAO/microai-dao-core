"""
Unified EPI Calculator
======================
Combines the clean mathematical model from EPI-governance with
the rich stakeholder analysis from microai-dao.

Core Formula: EPI = H(P, E) × B(P, E) × T(V)
- H(P, E): Harmonic mean (non-compensatory aggregation)
- B(P, E): Golden ratio balance penalty
- T(V): Geometric trust decay from violations
"""

import numpy as np
from typing import Tuple, List, Dict, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime

# Mathematical constants
PHI = (np.sqrt(5) - 1) / 2  # Golden ratio conjugate ≈ 0.618
GOLDEN_RATIO = (1 + np.sqrt(5)) / 2  # φ ≈ 1.618


@dataclass
class StakeholderImpact:
    """Represents impact on a specific stakeholder group."""
    stakeholder_type: str
    impact_score: float  # -1.0 to 1.0 (negative = harmful, positive = beneficial)
    weight: float  # 0.0 to 1.0 (importance of this stakeholder)
    confidence: float  # 0.0 to 1.0 (confidence in the assessment)


@dataclass
class EPIScores:
    """Input scores for EPI computation."""
    profit: float
    ethics: float
    violations: List[float] = field(default_factory=list)
    stakeholder_sentiment: float = 0.5
    stakeholder_impacts: Optional[List[StakeholderImpact]] = None
    transparency_score: float = 0.7
    sustainability_score: float = 0.6
    compliance_score: float = 0.8


@dataclass
class EPIResult:
    """Result of EPI calculation."""
    epi_score: float
    is_valid: bool
    ethical_component: float
    profitability_component: float
    balance_ratio: float
    harmonic_mean: float
    balance_penalty: float
    trust: float
    golden_ratio_deviation: float
    recommendation: str
    confidence: float
    reason: str
    optimization_suggestions: List[str] = field(default_factory=list)


class EPICalculator:
    """
    Unified Ethical Profitability Index Calculator.

    Combines:
    - EPI-governance: Clean math model, trust accumulator
    - microai-dao: Stakeholder analysis, optimization suggestions
    """

    # Default stakeholder weights (from microai-dao)
    DEFAULT_STAKEHOLDER_WEIGHTS = {
        "shareholders": 0.20,
        "employees": 0.20,
        "customers": 0.20,
        "community": 0.15,
        "environment": 0.15,
        "future_generations": 0.10
    }

    def __init__(
        self,
        threshold: float = 0.7,
        phi_weight: float = 1.0,
        stakeholder_weights: Optional[Dict[str, float]] = None
    ):
        """
        Initialize the EPI Calculator.

        Args:
            threshold: Minimum EPI score for approval (default 0.7)
            phi_weight: Weight for golden ratio balance penalty (default 1.0)
            stakeholder_weights: Custom stakeholder weights (optional)
        """
        self.threshold = threshold
        self.phi_weight = phi_weight
        self.stakeholder_weights = stakeholder_weights or self.DEFAULT_STAKEHOLDER_WEIGHTS

        # Thresholds for recommendations
        self.ethical_thresholds = {
            "minimum_acceptable": 0.6,
            "good": 0.75,
            "excellent": 0.9
        }
        self.profitability_thresholds = {
            "minimum_viable": 0.5,
            "target": 0.7,
            "exceptional": 0.9
        }

    @staticmethod
    def harmonic_mean(p: float, e: float) -> float:
        """
        Calculate harmonic mean: H = 2pe/(p+e)

        This ensures neither profit nor ethics can be zero
        without making the entire score zero (non-compensatory).
        """
        if p <= 0 or e <= 0:
            return 0.0
        return 2 * p * e / (p + e)

    def balance_penalty(self, p: float, e: float) -> float:
        """
        Calculate golden ratio balance penalty: B = 1 - φ|p-e|

        Penalizes imbalance between profit and ethics using
        the golden ratio conjugate (φ ≈ 0.618).
        """
        imbalance = abs(p - e)
        penalty = 1 - (self.phi_weight * PHI * imbalance)
        return max(0.0, penalty)

    @staticmethod
    def trust_accumulator(violations: List[float], initial_trust: float = 1.0) -> float:
        """
        Calculate geometric trust decay: T = T₀ × Π(1 - vᵢ)

        Each violation multiplicatively reduces trust,
        making recovery increasingly difficult.
        """
        trust = initial_trust
        for delta in violations:
            trust *= (1 - delta)
            if trust < 1e-6:
                return 0.0
        return trust

    def golden_ratio_deviation(self, p: float, e: float) -> float:
        """
        Measure deviation from optimal P/E ratio (≈ φ or 1/φ).

        The golden ratio represents natural balance point.
        """
        if e == 0:
            return float('inf')
        ratio = p / e
        return min(abs(ratio - GOLDEN_RATIO), abs(ratio - (1 / GOLDEN_RATIO)))

    def calculate_stakeholder_value(self, impacts: List[StakeholderImpact]) -> float:
        """
        Calculate weighted sum of stakeholder impacts.

        From microai-dao: Comprehensive stakeholder analysis.
        """
        if not impacts:
            return 0.5  # Default neutral score

        total_value = 0.0
        total_weight = 0.0

        for impact in impacts:
            weighted_impact = impact.impact_score * impact.weight * impact.confidence
            total_value += weighted_impact
            total_weight += impact.weight * impact.confidence

        if total_weight > 0:
            # Normalize to 0-1 range (from -1 to 1)
            return (total_value / total_weight + 1) / 2
        return 0.5

    def compute_epi(
        self,
        scores: EPIScores,
        include_sentiment: bool = False
    ) -> EPIResult:
        """
        Compute full EPI score with all components.

        Formula: EPI = H(P, E) × B(P, E) × T(V)

        Args:
            scores: Input scores for calculation
            include_sentiment: Whether to factor in stakeholder sentiment

        Returns:
            EPIResult with full analysis
        """
        # Calculate ethical component (enhanced with stakeholder analysis)
        if scores.stakeholder_impacts:
            stakeholder_value = self.calculate_stakeholder_value(scores.stakeholder_impacts)
            ethical_score = (
                stakeholder_value * 0.4 +
                scores.transparency_score * 0.2 +
                scores.sustainability_score * 0.2 +
                scores.compliance_score * 0.2
            )
        else:
            ethical_score = scores.ethics

        profitability_score = scores.profit

        # Core EPI calculation (from EPI-governance)
        hmean = self.harmonic_mean(profitability_score, ethical_score)
        penalty = self.balance_penalty(profitability_score, ethical_score)
        trust = self.trust_accumulator(scores.violations)

        # Calculate EPI
        epi = hmean * penalty * trust

        if include_sentiment:
            epi *= scores.stakeholder_sentiment

        # Calculate additional metrics
        gr_deviation = self.golden_ratio_deviation(profitability_score, ethical_score)
        balance_ratio = 1.0 / (1.0 + gr_deviation) if gr_deviation != float('inf') else 0.0

        # Determine validity and reason
        is_valid = epi >= self.threshold
        reason = self._determine_reason(epi, hmean, penalty, trust, ethical_score, profitability_score)

        # Generate recommendation
        recommendation = self._generate_recommendation(epi, ethical_score, profitability_score)

        # Calculate confidence
        confidence = self._calculate_confidence(scores, trust)

        # Generate optimization suggestions
        suggestions = self._generate_optimization_suggestions(
            ethical_score, profitability_score, balance_ratio
        )

        return EPIResult(
            epi_score=epi,
            is_valid=is_valid,
            ethical_component=ethical_score,
            profitability_component=profitability_score,
            balance_ratio=balance_ratio,
            harmonic_mean=hmean,
            balance_penalty=penalty,
            trust=trust,
            golden_ratio_deviation=gr_deviation,
            recommendation=recommendation,
            confidence=confidence,
            reason=reason,
            optimization_suggestions=suggestions
        )

    def _determine_reason(
        self, epi: float, hmean: float, penalty: float,
        trust: float, ethics: float, profit: float
    ) -> str:
        """Determine the reason for the EPI result."""
        if epi >= self.threshold:
            return 'approved'

        if hmean < 0.5:
            if ethics < profit:
                return 'rejected: ethical component too low'
            else:
                return 'rejected: profitability component too low'
        elif penalty < 0.7:
            return 'rejected: imbalance between profit and ethics'
        elif trust < 0.5:
            return 'rejected: trust compromised by violations'
        else:
            return f'rejected: EPI {epi:.3f} below threshold {self.threshold}'

    def _generate_recommendation(
        self, epi: float, ethical: float, profit: float
    ) -> str:
        """Generate recommendation based on EPI score."""
        if ethical < self.ethical_thresholds["minimum_acceptable"]:
            return "REJECT"
        if profit < self.profitability_thresholds["minimum_viable"]:
            return "REJECT"

        if epi >= 0.8:
            return "APPROVE"
        elif epi >= 0.6:
            return "MODIFY"
        else:
            return "REJECT"

    def _calculate_confidence(self, scores: EPIScores, trust: float) -> float:
        """Calculate confidence in the assessment."""
        if scores.stakeholder_impacts:
            ethical_confidence = np.mean([
                impact.confidence for impact in scores.stakeholder_impacts
            ])
        else:
            ethical_confidence = 0.7  # Default confidence

        # Trust factor affects confidence
        profitability_confidence = trust

        if ethical_confidence + profitability_confidence == 0:
            return 0.0

        return (2 * ethical_confidence * profitability_confidence) / (
            ethical_confidence + profitability_confidence
        )

    def _generate_optimization_suggestions(
        self, ethical: float, profit: float, balance: float
    ) -> List[str]:
        """Generate suggestions to improve EPI score."""
        suggestions = []

        if ethical < self.ethical_thresholds["good"]:
            suggestions.extend([
                "Increase stakeholder engagement and impact assessment",
                "Improve transparency in decision-making processes",
                "Enhance sustainability measures and long-term planning"
            ])

        if profit < self.profitability_thresholds["target"]:
            suggestions.extend([
                "Optimize cost structure and operational efficiency",
                "Explore additional revenue streams",
                "Reduce risk through diversification"
            ])

        if balance < 0.8:
            if ethical > profit * GOLDEN_RATIO:
                suggestions.append(
                    "Consider increasing profitability focus while maintaining ethics"
                )
            else:
                suggestions.append(
                    "Consider increasing ethical considerations for optimal balance"
                )

        return suggestions

    def optimize_for_golden_ratio(
        self,
        target_epi: float,
        current_ethics: float,
        violations: List[float]
    ) -> Dict[str, Any]:
        """
        Find optimal profit level to achieve target EPI.

        Uses search to find profit value that:
        1. Achieves target EPI
        2. Minimizes deviation from golden ratio
        """
        best_profit = 0.0
        best_epi = 0.0
        best_deviation = float('inf')

        for p in np.linspace(0.1, 1.0, 100):
            scores = EPIScores(profit=p, ethics=current_ethics, violations=violations)
            result = self.compute_epi(scores)
            deviation = self.golden_ratio_deviation(p, current_ethics)

            if abs(result.epi_score - target_epi) < 0.05 and deviation < best_deviation:
                best_profit = p
                best_epi = result.epi_score
                best_deviation = deviation

        return {
            'optimal_profit': best_profit,
            'achieved_epi': best_epi,
            'golden_ratio_deviation': best_deviation
        }
