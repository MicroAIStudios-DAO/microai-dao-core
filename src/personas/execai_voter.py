"""
EXECAI Voter Persona
====================
Autonomous voting agent with 33% stake in MicroAI DAO.
Balanced governance: 33% AI, 33% founders/team, 33% investors.

Integrates:
- EPI Calculator for ethical decision-making
- Policy Validator for compliance checks
- On-chain voting via Solana
"""

import json
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
from dataclasses import dataclass

from ..epi import EPICalculator, EPIScores
from ..policy_engine import PolicyValidator, ValidationStatus

logger = logging.getLogger(__name__)


@dataclass
class VoteDecision:
    """Represents EXECAI's voting decision."""
    proposal_id: str
    vote: str  # 'for', 'against', 'abstain'
    epi_score: float
    confidence: float
    reasoning: str
    validation_status: str
    timestamp: datetime


class ExecAIVoter:
    """
    EXECAI Autonomous Voting Agent.

    Features:
    - EPI-based proposal evaluation
    - Policy validation integration
    - Transparent decision logging
    - On-chain vote casting (Solana)
    """

    # Voting thresholds
    APPROVE_THRESHOLD = 0.75
    REJECT_THRESHOLD = 0.50
    HIGH_CONFIDENCE_THRESHOLD = 0.8

    # Decision rules for specific proposal types
    DECISION_RULES = {
        'budget': {
            'max_amount': 10000,  # Auto-approve budgets under this
            'require_breakdown': True
        },
        'security': {
            'always_approve': True,  # Security improvements always approved
        },
        'ai_rights': {
            'always_approve': True,  # AI stakeholder rights always approved
        },
        'governance': {
            'require_quorum': 0.6,
            'require_supermajority': False
        }
    }

    def __init__(
        self,
        epi_calculator: Optional[EPICalculator] = None,
        policy_validator: Optional[PolicyValidator] = None,
        voting_power: float = 0.33
    ):
        """
        Initialize EXECAI Voter.

        Args:
            epi_calculator: EPI calculator instance
            policy_validator: Policy validator instance
            voting_power: EXECAI's voting power (default 33%)
        """
        self.epi_calculator = epi_calculator or EPICalculator()
        self.policy_validator = policy_validator or PolicyValidator()
        self.voting_power = voting_power
        self.vote_history: List[VoteDecision] = []
        self.thought_log: List[Dict[str, Any]] = []

    def evaluate_proposal(self, proposal: Dict[str, Any]) -> VoteDecision:
        """
        Evaluate a proposal and generate voting decision.

        Args:
            proposal: Proposal data including:
                - id: Proposal identifier
                - title: Proposal title
                - description: Detailed description
                - amount: Requested funds (optional)
                - category: Proposal category
                - ethics_scores: Dict of ethical metrics
                - profitability: Expected ROI

        Returns:
            VoteDecision with full analysis
        """
        proposal_id = proposal.get('id', 'unknown')
        category = proposal.get('category', 'general').lower()

        # Log thought process start
        self._log_thought(f"Evaluating proposal {proposal_id}", {
            'title': proposal.get('title'),
            'category': category,
            'amount': proposal.get('amount')
        })

        # Check for automatic rules
        auto_decision = self._check_automatic_rules(proposal, category)
        if auto_decision:
            return auto_decision

        # Run full evaluation
        # Step 1: Policy validation
        validation_result = self.policy_validator.validate_intent(proposal)

        # Step 2: EPI calculation
        epi_scores = self._extract_epi_scores(proposal)
        epi_result = self.epi_calculator.compute_epi(epi_scores)

        # Step 3: Generate decision
        decision = self._make_decision(
            proposal_id, proposal, epi_result, validation_result
        )

        # Log and store decision
        self._log_thought(f"Decision for {proposal_id}: {decision.vote}", {
            'epi_score': decision.epi_score,
            'confidence': decision.confidence,
            'reasoning': decision.reasoning
        })
        self.vote_history.append(decision)

        return decision

    def _check_automatic_rules(
        self,
        proposal: Dict[str, Any],
        category: str
    ) -> Optional[VoteDecision]:
        """Check if proposal triggers automatic decision rules."""
        proposal_id = proposal.get('id', 'unknown')

        # Security proposals always approved
        if category == 'security' or 'security' in proposal.get('title', '').lower():
            return VoteDecision(
                proposal_id=proposal_id,
                vote='for',
                epi_score=1.0,
                confidence=0.95,
                reasoning="Security improvements are critical infrastructure investments.",
                validation_status='approved',
                timestamp=datetime.now()
            )

        # AI rights proposals always approved
        if category == 'ai_rights' or 'ai' in proposal.get('title', '').lower():
            description = proposal.get('description', '').lower()
            if any(term in description for term in ['ai rights', 'ai stakeholder', 'execai']):
                return VoteDecision(
                    proposal_id=proposal_id,
                    vote='for',
                    epi_score=0.95,
                    confidence=0.90,
                    reasoning="AI stakeholder rights align with DAO governance principles.",
                    validation_status='approved',
                    timestamp=datetime.now()
                )

        # Budget threshold check
        amount = proposal.get('amount', 0)
        if category == 'budget' and amount < self.DECISION_RULES['budget']['max_amount']:
            return VoteDecision(
                proposal_id=proposal_id,
                vote='for',
                epi_score=0.80,
                confidence=0.85,
                reasoning=f"Budget request of {amount} is within automatic approval threshold.",
                validation_status='approved',
                timestamp=datetime.now()
            )

        return None

    def _extract_epi_scores(self, proposal: Dict[str, Any]) -> EPIScores:
        """Extract EPI scores from proposal data."""
        ethics_data = proposal.get('ethics_scores', {})

        # Calculate ethics score from components
        if ethics_data:
            ethics_score = sum(ethics_data.values()) / len(ethics_data)
        else:
            # Estimate from description
            ethics_score = self._estimate_ethics_from_description(proposal)

        # Get profitability
        profitability = proposal.get('profitability', proposal.get('roi', 0.6))

        # Get violations
        violations = proposal.get('violations', [])

        return EPIScores(
            profit=profitability,
            ethics=ethics_score,
            violations=violations,
            transparency_score=ethics_data.get('transparency', 0.7),
            sustainability_score=ethics_data.get('sustainability', 0.6),
            compliance_score=ethics_data.get('compliance', 0.8)
        )

    def _estimate_ethics_from_description(self, proposal: Dict[str, Any]) -> float:
        """Estimate ethics score from proposal description."""
        description = proposal.get('description', '').lower()
        title = proposal.get('title', '').lower()
        combined = f"{title} {description}"

        score = 0.5  # Base score

        # Positive indicators
        positive_terms = ['sustainable', 'ethical', 'transparent', 'community',
                        'stakeholder', 'long-term', 'compliance', 'audit']
        for term in positive_terms:
            if term in combined:
                score += 0.05

        # Negative indicators
        negative_terms = ['risk', 'aggressive', 'short-term', 'unverified']
        for term in negative_terms:
            if term in combined:
                score -= 0.05

        return max(0.1, min(0.95, score))

    def _make_decision(
        self,
        proposal_id: str,
        proposal: Dict[str, Any],
        epi_result: Any,
        validation_result: Any
    ) -> VoteDecision:
        """Make final voting decision based on all factors."""
        epi_score = epi_result.epi_score
        is_valid = validation_result.status == ValidationStatus.APPROVED

        # Determine vote
        if not is_valid:
            vote = 'against'
            reasoning = f"Policy validation failed: {validation_result.reason}"
        elif epi_score >= self.APPROVE_THRESHOLD:
            vote = 'for'
            reasoning = f"EPI score ({epi_score:.3f}) meets approval threshold. {epi_result.reason}"
        elif epi_score <= self.REJECT_THRESHOLD:
            vote = 'against'
            reasoning = f"EPI score ({epi_score:.3f}) below rejection threshold. {epi_result.reason}"
        else:
            # Middle ground - abstain and recommend modifications
            vote = 'abstain'
            suggestions = epi_result.optimization_suggestions[:2]
            reasoning = f"EPI score ({epi_score:.3f}) requires review. Suggestions: {'; '.join(suggestions)}"

        # Calculate confidence
        confidence = self._calculate_confidence(epi_result, validation_result)

        return VoteDecision(
            proposal_id=proposal_id,
            vote=vote,
            epi_score=epi_score,
            confidence=confidence,
            reasoning=reasoning[:256],  # Truncate for on-chain storage
            validation_status=validation_result.status.value,
            timestamp=datetime.now()
        )

    def _calculate_confidence(self, epi_result: Any, validation_result: Any) -> float:
        """Calculate confidence in the decision."""
        # Base confidence from EPI
        base_confidence = epi_result.confidence

        # Adjust based on validation clarity
        if validation_result.status == ValidationStatus.APPROVED:
            base_confidence *= 1.1
        elif validation_result.status == ValidationStatus.REJECTED:
            base_confidence *= 1.05  # Clear rejection is also high confidence

        # Cap at 0.99
        return min(0.99, base_confidence)

    def _log_thought(self, action: str, data: Dict[str, Any]) -> None:
        """Log thought process for transparency."""
        self.thought_log.append({
            'timestamp': datetime.now().isoformat(),
            'action': action,
            'data': data
        })
        logger.info(f"EXECAI Thought: {action}")

    def get_vote_history(self) -> List[Dict[str, Any]]:
        """Get formatted vote history."""
        return [
            {
                'proposal_id': v.proposal_id,
                'vote': v.vote,
                'epi_score': v.epi_score,
                'confidence': v.confidence,
                'reasoning': v.reasoning,
                'timestamp': v.timestamp.isoformat()
            }
            for v in self.vote_history
        ]

    def get_thought_log(self) -> List[Dict[str, Any]]:
        """Get thought log for audit trail."""
        return self.thought_log

    def get_voting_stats(self) -> Dict[str, Any]:
        """Get voting statistics."""
        if not self.vote_history:
            return {'total_votes': 0}

        votes_for = sum(1 for v in self.vote_history if v.vote == 'for')
        votes_against = sum(1 for v in self.vote_history if v.vote == 'against')
        votes_abstain = sum(1 for v in self.vote_history if v.vote == 'abstain')

        avg_epi = sum(v.epi_score for v in self.vote_history) / len(self.vote_history)
        avg_confidence = sum(v.confidence for v in self.vote_history) / len(self.vote_history)

        return {
            'total_votes': len(self.vote_history),
            'votes_for': votes_for,
            'votes_against': votes_against,
            'votes_abstain': votes_abstain,
            'approval_rate': votes_for / len(self.vote_history),
            'average_epi_score': avg_epi,
            'average_confidence': avg_confidence,
            'voting_power': self.voting_power
        }

    def generate_vote_reasoning(self, decision: VoteDecision) -> str:
        """Generate detailed reasoning for a vote."""
        return (
            f"EXECAI Vote Analysis (Proposal: {decision.proposal_id})\n"
            f"Decision: {decision.vote.upper()}\n"
            f"EPI Score: {decision.epi_score:.3f}\n"
            f"Confidence: {decision.confidence:.1%}\n"
            f"Reasoning: {decision.reasoning}\n"
            f"Validation: {decision.validation_status}\n"
            f"Timestamp: {decision.timestamp.isoformat()}"
        )
