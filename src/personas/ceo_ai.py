"""
CEO-AI - Strategic Decision-Making Agent with EPI Constraints

An intelligent CEO agent that uses LLM reasoning for strategic planning,
proposal generation, and executive decision-making, all constrained by
the Ethical Profitability Index (EPI).

Features:
- Strategic planning and vision setting
- Proposal generation with EPI validation
- Market analysis and opportunity assessment
- Risk evaluation and mitigation
- Thought logging with cryptographic verification
"""

import os
import json
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime

# Try to import Hugging Face transformers
try:
    from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
    import torch
    HF_AVAILABLE = True
except ImportError:
    HF_AVAILABLE = False
    print("Warning: transformers not installed. CEO-AI will use fallback mode.")

# Import from other modules
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from epi.calculator import EPICalculator, EPIScores
from policy_engine.validator import PolicyValidator
from trust_stack.event_logger import EventLogger


@dataclass
class StrategicProposal:
    """Strategic proposal from CEO-AI."""
    proposal_id: str
    title: str
    description: str
    rationale: str
    expected_profit: float
    ethical_score: float
    epi_score: float
    risk_level: str  # low, medium, high
    timeline: str
    budget: float
    stakeholders: List[str]
    success_metrics: List[str]
    approved: bool
    confidence: float
    timestamp: datetime


class CEOAI:
    """
    CEO-AI: Strategic decision-making agent with EPI constraints.
    
    Uses LLM reasoning (Hugging Face models) for strategic planning
    and decision-making, with all decisions validated against EPI thresholds.
    """
    
    def __init__(
        self,
        model_name: str = "microsoft/Phi-3-mini-4k-instruct",
        epi_threshold: float = 0.7,
        use_local_model: bool = False
    ):
        """
        Initialize CEO-AI agent.
        
        Args:
            model_name: Hugging Face model to use for reasoning
            epi_threshold: Minimum EPI score for approval
            use_local_model: Whether to load model locally (vs API)
        """
        self.agent_id = "CEO-AI"
        self.model_name = model_name
        self.epi_threshold = epi_threshold
        self.use_local_model = use_local_model
        
        # Initialize components
        self.epi_calculator = EPICalculator()
        self.policy_validator = PolicyValidator()
        self.event_logger = EventLogger()
        
        # Initialize LLM
        self.llm = None
        self.tokenizer = None
        
        if HF_AVAILABLE and use_local_model:
            self._initialize_llm()
        
        # Decision history
        self.proposals = []
        self.decisions = []
    
    def _initialize_llm(self):
        """Initialize Hugging Face LLM for reasoning."""
        try:
            print(f"Loading {self.model_name}...")
            
            # Use pipeline for simpler inference
            self.llm = pipeline(
                "text-generation",
                model=self.model_name,
                torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
                device_map="auto" if torch.cuda.is_available() else None,
                max_new_tokens=512,
                temperature=0.7,
                top_p=0.9
            )
            
            print(f"✓ {self.model_name} loaded successfully")
            
        except Exception as e:
            print(f"Warning: Could not load model: {e}")
            print("CEO-AI will use fallback reasoning mode")
            self.llm = None
    
    def _generate_with_llm(self, prompt: str) -> str:
        """
        Generate text using LLM.
        
        Args:
            prompt: Input prompt
            
        Returns:
            Generated text
        """
        if self.llm:
            try:
                result = self.llm(prompt, max_new_tokens=512)
                return result[0]['generated_text'].replace(prompt, '').strip()
            except Exception as e:
                print(f"LLM generation error: {e}")
                return self._fallback_reasoning(prompt)
        else:
            return self._fallback_reasoning(prompt)
    
    def _fallback_reasoning(self, prompt: str) -> str:
        """
        Fallback reasoning when LLM is not available.
        
        Args:
            prompt: Input prompt
            
        Returns:
            Rule-based response
        """
        # Simple rule-based responses for common scenarios
        if "healthcare" in prompt.lower():
            return "Healthcare AI investment shows strong ethical alignment with patient outcomes and data privacy. Recommended allocation: $500k over 18 months with focus on diagnostic accuracy and accessibility."
        elif "finance" in prompt.lower():
            return "Financial AI tools require careful ethical oversight for bias prevention and transparency. Recommended: Start with pilot program, $250k budget, strict compliance monitoring."
        elif "education" in prompt.lower():
            return "Education technology investment aligns well with accessibility and equity goals. Recommended: $400k for adaptive learning platform with emphasis on underserved communities."
        else:
            return "Strategic analysis indicates moderate opportunity with balanced risk-reward profile. Recommend further market research and stakeholder consultation before proceeding."
    
    def analyze_opportunity(
        self,
        opportunity: str,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Analyze a strategic opportunity using LLM reasoning.
        
        Args:
            opportunity: Description of the opportunity
            context: Additional context (market data, constraints, etc.)
            
        Returns:
            Analysis with recommendations
        """
        # Build prompt for LLM
        prompt = f"""You are the CEO of an AI-governed organization. Analyze this strategic opportunity:

Opportunity: {opportunity}

Context: {json.dumps(context or {}, indent=2)}

Provide a strategic analysis covering:
1. Market potential and competitive advantage
2. Ethical considerations and stakeholder impact
3. Risk assessment and mitigation strategies
4. Resource requirements and timeline
5. Success metrics and expected outcomes

Analysis:"""
        
        # Generate analysis
        analysis_text = self._generate_with_llm(prompt)
        
        # Extract structured data (simplified)
        analysis = {
            'opportunity': opportunity,
            'analysis': analysis_text,
            'timestamp': datetime.now().isoformat(),
            'agent': self.agent_id,
            'model': self.model_name
        }
        
        return analysis
    
    def generate_proposal(
        self,
        title: str,
        description: str,
        expected_profit: float,
        ethical_factors: Dict[str, float],
        budget: float,
        timeline: str,
        context: Optional[Dict[str, Any]] = None
    ) -> StrategicProposal:
        """
        Generate a strategic proposal with EPI validation.
        
        Args:
            title: Proposal title
            description: Detailed description
            expected_profit: Expected profit (normalized 0-1)
            ethical_factors: Ethical scores by category
            budget: Required budget
            timeline: Implementation timeline
            context: Additional context
            
        Returns:
            StrategicProposal with EPI validation
        """
        # Generate rationale using LLM
        prompt = f"""As CEO, provide strategic rationale for this proposal:

Title: {title}
Description: {description}
Budget: ${budget:,.0f}
Timeline: {timeline}

Why should we pursue this opportunity? What are the strategic benefits and potential risks?

Rationale:"""
        
        rationale = self._generate_with_llm(prompt)
        
        # Calculate ethics score (average of factors)
        ethics_score = sum(ethical_factors.values()) / len(ethical_factors) if ethical_factors else 0.5
        
        # Calculate EPI score
        epi_scores = EPIScores(
            profit=expected_profit,
            ethics=ethics_score,
            violations=[],
            stakeholder_sentiment=ethical_factors.get('stakeholder_sentiment', 0.7),
            transparency_score=ethical_factors.get('transparency', 0.8),
            sustainability_score=ethical_factors.get('sustainability', 0.7),
            compliance_score=ethical_factors.get('compliance', 0.9)
        )
        
        epi_result = self.epi_calculator.compute_epi(epi_scores)
        
        # Determine approval based on EPI
        approved = epi_result.is_valid and epi_result.epi_score >= self.epi_threshold
        
        # Assess risk level
        if epi_result.epi_score >= 0.8:
            risk_level = "low"
        elif epi_result.epi_score >= 0.6:
            risk_level = "medium"
        else:
            risk_level = "high"
        
        # Create proposal
        proposal = StrategicProposal(
            proposal_id=f"PROP-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
            title=title,
            description=description,
            rationale=rationale,
            expected_profit=expected_profit,
            ethical_score=ethics_score,
            epi_score=epi_result.epi_score,
            risk_level=risk_level,
            timeline=timeline,
            budget=budget,
            stakeholders=context.get('stakeholders', []) if context else [],
            success_metrics=context.get('success_metrics', []) if context else [],
            approved=approved,
            confidence=epi_result.confidence,
            timestamp=datetime.now()
        )
        
        # Log decision to Trust Stack
        self._log_decision(proposal, epi_result)
        
        # Store proposal
        self.proposals.append(proposal)
        
        return proposal
    
    def _log_decision(self, proposal: StrategicProposal, epi_result):
        """
        Log decision to Trust Stack with cryptographic signature.
        
        Args:
            proposal: Strategic proposal
            epi_result: EPI calculation result
        """
        try:
            # Create evaluations
            evaluations = [
                self.event_logger.create_evaluation(
                    evaluator="epi-calculator",
                    category="EPI",
                    result="pass" if proposal.approved else "fail",
                    confidence=proposal.confidence
                ),
                self.event_logger.create_evaluation(
                    evaluator="ethics-validator",
                    category="Safety",
                    result="pass" if proposal.ethical_score >= 0.6 else "fail",
                    confidence=proposal.ethical_score
                )
            ]
            
            # Log event
            event = self.event_logger.log_event(
                tenant_id="microai-dao",
                agent_id=self.agent_id,
                action_type="strategic_proposal",
                input_data=f"{proposal.title}: {proposal.description}",
                output_data=f"{'Approved' if proposal.approved else 'Rejected'}: EPI={proposal.epi_score:.3f}",
                policy_version="v1.0.0",
                epi_score=proposal.epi_score,
                model=self.model_name,
                tools_called=["epi_calculator", "llm_reasoning"],
                evaluations=evaluations
            )
            
            print(f"✓ Decision logged: {event.event_id}")
            
        except Exception as e:
            print(f"Warning: Could not log decision: {e}")
    
    def review_performance(
        self,
        metrics: Dict[str, float],
        period: str
    ) -> Dict[str, Any]:
        """
        Review organizational performance and provide strategic guidance.
        
        Args:
            metrics: Performance metrics
            period: Time period (e.g., "Q4 2025")
            
        Returns:
            Performance review with recommendations
        """
        prompt = f"""As CEO, review organizational performance for {period}:

Metrics:
{json.dumps(metrics, indent=2)}

Provide:
1. Performance assessment (strengths and weaknesses)
2. Strategic recommendations for improvement
3. Priority initiatives for next period

Review:"""
        
        review_text = self._generate_with_llm(prompt)
        
        return {
            'period': period,
            'metrics': metrics,
            'review': review_text,
            'timestamp': datetime.now().isoformat(),
            'agent': self.agent_id
        }
    
    def get_proposal_history(self, limit: int = 10) -> List[Dict]:
        """
        Get recent proposal history.
        
        Args:
            limit: Maximum number of proposals to return
            
        Returns:
            List of proposal dictionaries
        """
        recent = self.proposals[-limit:] if len(self.proposals) > limit else self.proposals
        
        return [{
            'proposal_id': p.proposal_id,
            'title': p.title,
            'epi_score': p.epi_score,
            'approved': p.approved,
            'budget': p.budget,
            'timestamp': p.timestamp.isoformat()
        } for p in recent]
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get CEO-AI statistics.
        
        Returns:
            Statistics dictionary
        """
        if not self.proposals:
            return {
                'total_proposals': 0,
                'approved': 0,
                'rejected': 0,
                'average_epi': 0,
                'approval_rate': 0
            }
        
        approved = sum(1 for p in self.proposals if p.approved)
        total = len(self.proposals)
        avg_epi = sum(p.epi_score for p in self.proposals) / total
        
        return {
            'total_proposals': total,
            'approved': approved,
            'rejected': total - approved,
            'average_epi': round(avg_epi, 3),
            'approval_rate': round(approved / total * 100, 1),
            'model': self.model_name,
            'epi_threshold': self.epi_threshold
        }


# Example usage
if __name__ == "__main__":
    # Initialize CEO-AI
    ceo = CEOAI(use_local_model=False)  # Set to True to use local model
    
    # Generate a strategic proposal
    proposal = ceo.generate_proposal(
        title="Healthcare AI Investment",
        description="Invest in AI-powered diagnostic tools for underserved communities",
        expected_profit=0.75,
        ethical_factors={
            'patient_outcomes': 0.9,
            'data_privacy': 0.85,
            'accessibility': 0.95,
            'transparency': 0.8,
            'sustainability': 0.7,
            'compliance': 0.9
        },
        budget=500000,
        timeline="18 months",
        context={
            'stakeholders': ['patients', 'healthcare_providers', 'regulators'],
            'success_metrics': ['diagnostic_accuracy', 'patient_satisfaction', 'cost_reduction']
        }
    )
    
    print(f"\n{'='*60}")
    print(f"Proposal: {proposal.title}")
    print(f"{'='*60}")
    print(f"EPI Score: {proposal.epi_score:.3f}")
    print(f"Status: {'✓ APPROVED' if proposal.approved else '✗ REJECTED'}")
    print(f"Risk Level: {proposal.risk_level.upper()}")
    print(f"Budget: ${proposal.budget:,.0f}")
    print(f"Timeline: {proposal.timeline}")
    print(f"\nRationale:\n{proposal.rationale}")
    print(f"{'='*60}\n")
    
    # Get stats
    stats = ceo.get_stats()
    print("CEO-AI Statistics:")
    print(json.dumps(stats, indent=2))
