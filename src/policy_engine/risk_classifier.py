"""
Risk Classification Module
==========================

Implements 4-tier risk classification system for AI models:
- Tier 1: Low Risk (automated approval)
- Tier 2: Medium Risk (technical review)
- Tier 3: High Risk (multi-stakeholder review)
- Tier 4: Critical Risk (full DAO vote + external audit)

Based on MicroAI DAO Framework enterprise specifications.
"""

from enum import Enum
from dataclasses import dataclass
from typing import Dict, List, Optional, Any
import json


class RiskTier(Enum):
    """AI model risk tiers."""
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4


@dataclass
class RiskAssessment:
    """Risk assessment result."""
    tier: RiskTier
    score: float  # 0-1 risk score
    factors: Dict[str, float]  # Individual risk factors
    approval_requirements: Dict[str, Any]
    reasoning: str
    recommendations: List[str]


class RiskClassifier:
    """
    Classifies AI models into risk tiers based on multiple factors.
    
    Risk Factors:
    - Impact scope (individual, group, society)
    - Decision autonomy (human-in-loop, automated)
    - Data sensitivity (public, private, protected)
    - Reversibility (easily reversible, permanent)
    - Regulatory requirements (none, moderate, high)
    """
    
    def __init__(self):
        """Initialize risk classifier with tier definitions."""
        self.tier_definitions = {
            RiskTier.LOW: {
                "description": "Low risk AI with minimal impact",
                "examples": ["Content recommendation", "Spam filtering", "Search ranking"],
                "approval_requirements": {
                    "voting_required": False,
                    "quorum": 0,
                    "majority": 0,
                    "technical_review": False,
                    "ethics_review": False,
                    "external_audit": False,
                    "automated_approval": True
                },
                "max_score": 0.25
            },
            RiskTier.MEDIUM: {
                "description": "Medium risk AI requiring technical oversight",
                "examples": ["Customer service automation", "Pricing optimization", "Content moderation"],
                "approval_requirements": {
                    "voting_required": True,
                    "quorum": 0.30,
                    "majority": 0.50,
                    "technical_review": True,
                    "ethics_review": False,
                    "external_audit": False,
                    "automated_approval": False
                },
                "max_score": 0.50
            },
            RiskTier.HIGH: {
                "description": "High risk AI with significant impact",
                "examples": ["Credit scoring", "Hiring decisions", "Medical diagnosis", "Legal assessment"],
                "approval_requirements": {
                    "voting_required": True,
                    "quorum": 0.50,
                    "majority": 0.66,
                    "technical_review": True,
                    "ethics_review": True,
                    "external_audit": False,
                    "automated_approval": False
                },
                "max_score": 0.75
            },
            RiskTier.CRITICAL: {
                "description": "Critical risk AI requiring maximum oversight",
                "examples": ["Autonomous vehicles", "Critical infrastructure", "Weapons systems", "Life support"],
                "approval_requirements": {
                    "voting_required": True,
                    "quorum": 0.75,
                    "majority": 0.80,
                    "technical_review": True,
                    "ethics_review": True,
                    "external_audit": True,
                    "automated_approval": False
                },
                "max_score": 1.0
            }
        }
    
    def assess_risk(
        self,
        model_name: str,
        model_type: str,
        use_case: str,
        impact_scope: str = "individual",  # individual, group, society
        decision_autonomy: str = "human_in_loop",  # human_in_loop, automated, fully_autonomous
        data_sensitivity: str = "public",  # public, private, protected, highly_sensitive
        reversibility: str = "reversible",  # reversible, difficult, permanent
        regulatory_requirements: str = "none",  # none, moderate, high, critical
        additional_factors: Optional[Dict[str, float]] = None
    ) -> RiskAssessment:
        """
        Assess the risk tier of an AI model.
        
        Args:
            model_name: Name of the AI model
            model_type: Type of model (e.g., "classification", "generation", "recommendation")
            use_case: Description of the use case
            impact_scope: Scope of impact
            decision_autonomy: Level of automation
            data_sensitivity: Sensitivity of data used
            reversibility: How easily decisions can be reversed
            regulatory_requirements: Level of regulatory oversight
            additional_factors: Optional additional risk factors
        
        Returns:
            RiskAssessment with tier, score, and requirements
        """
        # Calculate individual risk factors
        factors = {
            "impact_scope": self._score_impact_scope(impact_scope),
            "decision_autonomy": self._score_decision_autonomy(decision_autonomy),
            "data_sensitivity": self._score_data_sensitivity(data_sensitivity),
            "reversibility": self._score_reversibility(reversibility),
            "regulatory_requirements": self._score_regulatory(regulatory_requirements)
        }
        
        # Add additional factors if provided
        if additional_factors:
            factors.update(additional_factors)
        
        # Calculate overall risk score (weighted average)
        weights = {
            "impact_scope": 0.25,
            "decision_autonomy": 0.25,
            "data_sensitivity": 0.20,
            "reversibility": 0.15,
            "regulatory_requirements": 0.15
        }
        
        risk_score = sum(
            factors.get(factor, 0) * weight
            for factor, weight in weights.items()
        )
        
        # Determine tier based on score
        tier = self._determine_tier(risk_score)
        
        # Get approval requirements
        approval_requirements = self.tier_definitions[tier]["approval_requirements"].copy()
        
        # Generate reasoning
        reasoning = self._generate_reasoning(
            model_name, model_type, use_case, tier, factors, risk_score
        )
        
        # Generate recommendations
        recommendations = self._generate_recommendations(tier, factors)
        
        return RiskAssessment(
            tier=tier,
            score=risk_score,
            factors=factors,
            approval_requirements=approval_requirements,
            reasoning=reasoning,
            recommendations=recommendations
        )
    
    def _score_impact_scope(self, scope: str) -> float:
        """Score the impact scope."""
        scores = {
            "individual": 0.2,
            "group": 0.5,
            "organization": 0.7,
            "society": 1.0
        }
        return scores.get(scope.lower(), 0.5)
    
    def _score_decision_autonomy(self, autonomy: str) -> float:
        """Score the decision autonomy level."""
        scores = {
            "human_in_loop": 0.2,
            "human_oversight": 0.4,
            "automated": 0.7,
            "fully_autonomous": 1.0
        }
        return scores.get(autonomy.lower(), 0.5)
    
    def _score_data_sensitivity(self, sensitivity: str) -> float:
        """Score the data sensitivity level."""
        scores = {
            "public": 0.1,
            "internal": 0.3,
            "private": 0.6,
            "protected": 0.8,
            "highly_sensitive": 1.0
        }
        return scores.get(sensitivity.lower(), 0.5)
    
    def _score_reversibility(self, reversibility: str) -> float:
        """Score the reversibility of decisions."""
        scores = {
            "reversible": 0.1,
            "difficult": 0.5,
            "very_difficult": 0.8,
            "permanent": 1.0
        }
        return scores.get(reversibility.lower(), 0.5)
    
    def _score_regulatory(self, requirements: str) -> float:
        """Score the regulatory requirements."""
        scores = {
            "none": 0.0,
            "minimal": 0.2,
            "moderate": 0.5,
            "high": 0.8,
            "critical": 1.0
        }
        return scores.get(requirements.lower(), 0.3)
    
    def _determine_tier(self, risk_score: float) -> RiskTier:
        """Determine risk tier from score."""
        if risk_score <= 0.25:
            return RiskTier.LOW
        elif risk_score <= 0.50:
            return RiskTier.MEDIUM
        elif risk_score <= 0.75:
            return RiskTier.HIGH
        else:
            return RiskTier.CRITICAL
    
    def _generate_reasoning(
        self,
        model_name: str,
        model_type: str,
        use_case: str,
        tier: RiskTier,
        factors: Dict[str, float],
        risk_score: float
    ) -> str:
        """Generate human-readable reasoning for the risk assessment."""
        reasoning_parts = [
            f"Model '{model_name}' ({model_type}) for use case '{use_case}' "
            f"has been classified as {tier.name} risk (score: {risk_score:.3f}).",
            "\nKey risk factors:"
        ]
        
        # Sort factors by score (highest first)
        sorted_factors = sorted(factors.items(), key=lambda x: x[1], reverse=True)
        
        for factor, score in sorted_factors[:3]:  # Top 3 factors
            factor_name = factor.replace("_", " ").title()
            risk_level = "low" if score < 0.3 else "moderate" if score < 0.7 else "high"
            reasoning_parts.append(f"  - {factor_name}: {score:.2f} ({risk_level})")
        
        return "\n".join(reasoning_parts)
    
    def _generate_recommendations(
        self,
        tier: RiskTier,
        factors: Dict[str, float]
    ) -> List[str]:
        """Generate recommendations based on risk assessment."""
        recommendations = []
        
        # Tier-specific recommendations
        if tier == RiskTier.LOW:
            recommendations.append("Automated approval enabled - periodic review recommended")
        elif tier == RiskTier.MEDIUM:
            recommendations.append("Technical review required before deployment")
            recommendations.append("Monitor performance metrics closely")
        elif tier == RiskTier.HIGH:
            recommendations.append("Multi-stakeholder review required")
            recommendations.append("Ethics committee approval needed")
            recommendations.append("Implement human oversight mechanisms")
        elif tier == RiskTier.CRITICAL:
            recommendations.append("Full DAO vote required")
            recommendations.append("External audit mandatory")
            recommendations.append("Implement fail-safe mechanisms")
            recommendations.append("Continuous monitoring required")
        
        # Factor-specific recommendations
        if factors.get("data_sensitivity", 0) > 0.7:
            recommendations.append("Implement strong data encryption and access controls")
        
        if factors.get("reversibility", 0) > 0.7:
            recommendations.append("Implement decision logging and audit trail")
        
        if factors.get("decision_autonomy", 0) > 0.7:
            recommendations.append("Implement human override capabilities")
        
        return recommendations
    
    def get_tier_info(self, tier: RiskTier) -> Dict[str, Any]:
        """Get information about a specific risk tier."""
        return self.tier_definitions[tier].copy()
    
    def export_assessment(self, assessment: RiskAssessment) -> str:
        """Export risk assessment as JSON."""
        return json.dumps({
            "tier": assessment.tier.name,
            "tier_level": assessment.tier.value,
            "risk_score": assessment.score,
            "factors": assessment.factors,
            "approval_requirements": assessment.approval_requirements,
            "reasoning": assessment.reasoning,
            "recommendations": assessment.recommendations
        }, indent=2)


# Example usage
if __name__ == "__main__":
    classifier = RiskClassifier()
    
    # Example 1: Low risk - content recommendation
    assessment1 = classifier.assess_risk(
        model_name="ContentRecommender-v1",
        model_type="recommendation",
        use_case="Recommend articles to users",
        impact_scope="individual",
        decision_autonomy="automated",
        data_sensitivity="public",
        reversibility="reversible",
        regulatory_requirements="none"
    )
    
    print("=" * 70)
    print("Example 1: Content Recommendation")
    print("=" * 70)
    print(f"Tier: {assessment1.tier.name}")
    print(f"Score: {assessment1.score:.3f}")
    print(f"\n{assessment1.reasoning}")
    print(f"\nRecommendations:")
    for rec in assessment1.recommendations:
        print(f"  - {rec}")
    
    # Example 2: High risk - credit scoring
    assessment2 = classifier.assess_risk(
        model_name="CreditScorer-v2",
        model_type="classification",
        use_case="Determine creditworthiness for loan applications",
        impact_scope="individual",
        decision_autonomy="automated",
        data_sensitivity="protected",
        reversibility="difficult",
        regulatory_requirements="high"
    )
    
    print("\n" + "=" * 70)
    print("Example 2: Credit Scoring")
    print("=" * 70)
    print(f"Tier: {assessment2.tier.name}")
    print(f"Score: {assessment2.score:.3f}")
    print(f"\n{assessment2.reasoning}")
    print(f"\nApproval Requirements:")
    for key, value in assessment2.approval_requirements.items():
        print(f"  - {key}: {value}")
    print(f"\nRecommendations:")
    for rec in assessment2.recommendations:
        print(f"  - {rec}")
