"""
Trust Accumulator Module
========================
Implements geometric trust decay based on violation history.

Formula: T(t) = T₀ × Π(1 - vᵢ)

Trust is multiplicatively reduced by each violation,
making recovery increasingly difficult over time.
"""

from typing import List, Dict, Any
from dataclasses import dataclass
from datetime import datetime, timedelta


@dataclass
class Violation:
    """Records a single violation event."""
    severity: float  # 0.0 to 1.0 (higher = more severe)
    timestamp: datetime
    description: str
    category: str  # e.g., 'ethical', 'compliance', 'financial'
    resolved: bool = False


class TrustAccumulator:
    """
    Manages trust score with geometric decay and recovery.

    Features:
    - Geometric decay on violations
    - Time-based recovery mechanism
    - Category-weighted violations
    - Trust floor to prevent permanent zero
    """

    # Category weights (some violations are more damaging)
    CATEGORY_WEIGHTS = {
        'ethical': 1.2,      # Ethics violations weighted higher
        'compliance': 1.1,   # Compliance issues moderately weighted
        'financial': 1.0,    # Financial issues standard weight
        'operational': 0.8,  # Operational issues slightly lower
        'communication': 0.6 # Communication issues lowest weight
    }

    def __init__(
        self,
        initial_trust: float = 1.0,
        trust_floor: float = 0.1,
        recovery_rate: float = 0.01,  # Daily recovery rate
        decay_half_life_days: float = 90.0  # Violations decay over time
    ):
        """
        Initialize trust accumulator.

        Args:
            initial_trust: Starting trust level (default 1.0)
            trust_floor: Minimum trust level (prevents permanent zero)
            recovery_rate: Daily trust recovery rate
            decay_half_life_days: Days for violation impact to halve
        """
        self.initial_trust = initial_trust
        self.trust_floor = trust_floor
        self.recovery_rate = recovery_rate
        self.decay_half_life = decay_half_life_days
        self.violations: List[Violation] = []
        self._current_trust = initial_trust
        self._last_update = datetime.now()

    def add_violation(
        self,
        severity: float,
        description: str,
        category: str = 'operational'
    ) -> float:
        """
        Record a violation and update trust.

        Args:
            severity: Violation severity (0.0 to 1.0)
            description: Description of the violation
            category: Violation category for weighting

        Returns:
            New trust level after violation
        """
        violation = Violation(
            severity=min(max(severity, 0.0), 1.0),  # Clamp to [0, 1]
            timestamp=datetime.now(),
            description=description,
            category=category
        )
        self.violations.append(violation)

        # Apply category weight
        weight = self.CATEGORY_WEIGHTS.get(category, 1.0)
        effective_severity = min(violation.severity * weight, 0.99)  # Cap at 0.99

        # Geometric decay
        self._current_trust *= (1 - effective_severity)

        # Apply floor
        self._current_trust = max(self._current_trust, self.trust_floor)
        self._last_update = datetime.now()

        return self._current_trust

    def get_trust(self, apply_recovery: bool = True) -> float:
        """
        Get current trust level with optional time-based recovery.

        Args:
            apply_recovery: Whether to apply time-based recovery

        Returns:
            Current trust level
        """
        if apply_recovery:
            self._apply_recovery()
        return self._current_trust

    def _apply_recovery(self) -> None:
        """Apply time-based trust recovery."""
        now = datetime.now()
        days_elapsed = (now - self._last_update).total_seconds() / 86400

        if days_elapsed > 0 and self._current_trust < self.initial_trust:
            # Asymptotic recovery toward initial trust
            recovery = self.recovery_rate * days_elapsed
            gap = self.initial_trust - self._current_trust
            self._current_trust += gap * min(recovery, 0.5)  # Cap recovery per update
            self._last_update = now

    def compute_from_violations(
        self,
        violations: List[float],
        initial_trust: float = 1.0
    ) -> float:
        """
        Compute trust from a list of violation severities.

        Static computation without modifying state.

        Args:
            violations: List of violation severities
            initial_trust: Starting trust level

        Returns:
            Computed trust level
        """
        trust = initial_trust
        for severity in violations:
            trust *= (1 - severity)
            if trust < self.trust_floor:
                return self.trust_floor
        return trust

    def get_violation_history(self) -> List[Dict[str, Any]]:
        """Get formatted violation history."""
        return [
            {
                'severity': v.severity,
                'timestamp': v.timestamp.isoformat(),
                'description': v.description,
                'category': v.category,
                'resolved': v.resolved
            }
            for v in self.violations
        ]

    def resolve_violation(self, index: int, recovery_bonus: float = 0.05) -> bool:
        """
        Mark a violation as resolved with trust recovery bonus.

        Args:
            index: Index of violation to resolve
            recovery_bonus: Trust recovery for resolving

        Returns:
            Success status
        """
        if 0 <= index < len(self.violations):
            if not self.violations[index].resolved:
                self.violations[index].resolved = True
                # Bonus recovery for addressing violations
                self._current_trust = min(
                    self._current_trust + recovery_bonus,
                    self.initial_trust
                )
                return True
        return False

    def get_trust_report(self) -> Dict[str, Any]:
        """Generate comprehensive trust report."""
        unresolved = [v for v in self.violations if not v.resolved]
        resolved = [v for v in self.violations if v.resolved]

        return {
            'current_trust': self._current_trust,
            'initial_trust': self.initial_trust,
            'trust_floor': self.trust_floor,
            'total_violations': len(self.violations),
            'unresolved_violations': len(unresolved),
            'resolved_violations': len(resolved),
            'worst_category': self._get_worst_category(),
            'recovery_rate': self.recovery_rate,
            'last_update': self._last_update.isoformat()
        }

    def _get_worst_category(self) -> str:
        """Find category with most severe violations."""
        if not self.violations:
            return 'none'

        category_scores = {}
        for v in self.violations:
            if v.category not in category_scores:
                category_scores[v.category] = 0
            category_scores[v.category] += v.severity

        return max(category_scores, key=category_scores.get)
