"""
CFO-AI - Financial Decision-Making Agent with EPI Constraints

An intelligent CFO agent that handles budget allocation, payment approvals,
treasury management, and financial planning, all constrained by EPI.

Features:
- Budget allocation with EPI validation
- Payment approval workflow
- Treasury management and optimization
- Financial forecasting and risk assessment
- Compliance checking for financial decisions
"""

import os
import json
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime

# Try to import Hugging Face transformers
try:
    from transformers import pipeline
    import torch
    HF_AVAILABLE = True
except ImportError:
    HF_AVAILABLE = False

# Import from other modules
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from epi.calculator import EPICalculator, EPIScores
from policy_engine.validator import PolicyValidator
from trust_stack.event_logger import EventLogger


@dataclass
class PaymentDecision:
    """Payment approval decision from CFO-AI."""
    payment_id: str
    recipient: str
    amount: float
    purpose: str
    category: str  # operational, investment, compensation, etc.
    epi_score: float
    approved: bool
    risk_assessment: str
    compliance_status: str
    reasoning: str
    timestamp: datetime


@dataclass
class BudgetAllocation:
    """Budget allocation decision."""
    allocation_id: str
    department: str
    amount: float
    purpose: str
    epi_score: float
    approved: bool
    constraints: List[str]
    expected_roi: float
    timestamp: datetime


class CFOAI:
    """
    CFO-AI: Financial decision-making agent with EPI constraints.
    
    Handles all financial decisions including payments, budgets,
    and treasury management with EPI validation.
    """
    
    def __init__(
        self,
        model_name: str = "microsoft/Phi-3-mini-4k-instruct",
        epi_threshold: float = 0.7,
        use_local_model: bool = False
    ):
        """
        Initialize CFO-AI agent.
        
        Args:
            model_name: Hugging Face model for reasoning
            epi_threshold: Minimum EPI score for approval
            use_local_model: Whether to load model locally
        """
        self.agent_id = "CFO-AI"
        self.model_name = model_name
        self.epi_threshold = epi_threshold
        self.use_local_model = use_local_model
        
        # Initialize components
        self.epi_calculator = EPICalculator()
        self.policy_validator = PolicyValidator()
        self.event_logger = EventLogger()
        
        # Initialize LLM
        self.llm = None
        if HF_AVAILABLE and use_local_model:
            self._initialize_llm()
        
        # Decision history
        self.payments = []
        self.allocations = []
        self.treasury_balance = 1000000  # Starting balance (demo)
    
    def _initialize_llm(self):
        """Initialize Hugging Face LLM for reasoning."""
        try:
            print(f"Loading {self.model_name} for CFO-AI...")
            
            self.llm = pipeline(
                "text-generation",
                model=self.model_name,
                torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
                device_map="auto" if torch.cuda.is_available() else None,
                max_new_tokens=512,
                temperature=0.7
            )
            
            print(f"✓ CFO-AI model loaded")
            
        except Exception as e:
            print(f"Warning: Could not load model: {e}")
            self.llm = None
    
    def _generate_with_llm(self, prompt: str) -> str:
        """Generate text using LLM."""
        if self.llm:
            try:
                result = self.llm(prompt, max_new_tokens=512)
                return result[0]['generated_text'].replace(prompt, '').strip()
            except Exception as e:
                return self._fallback_reasoning(prompt)
        else:
            return self._fallback_reasoning(prompt)
    
    def _fallback_reasoning(self, prompt: str) -> str:
        """Fallback reasoning when LLM unavailable."""
        if "salary" in prompt.lower() or "compensation" in prompt.lower():
            return "Compensation payment approved pending compliance verification. Ensure tax withholding and employment law compliance."
        elif "vendor" in prompt.lower() or "supplier" in prompt.lower():
            return "Vendor payment approved. Verify invoice accuracy and contract terms before processing."
        elif "investment" in prompt.lower():
            return "Investment requires additional due diligence. Assess ROI potential, risk factors, and alignment with strategic goals."
        else:
            return "Financial decision requires careful review of budget impact, compliance requirements, and strategic alignment."
    
    def approve_payment(
        self,
        recipient: str,
        amount: float,
        purpose: str,
        category: str,
        ethical_factors: Optional[Dict[str, float]] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> PaymentDecision:
        """
        Approve or reject a payment with EPI validation.
        
        Args:
            recipient: Payment recipient
            amount: Payment amount
            purpose: Purpose of payment
            category: Payment category
            ethical_factors: Ethical considerations
            context: Additional context
            
        Returns:
            PaymentDecision with approval status
        """
        # Generate reasoning using LLM
        prompt = f"""As CFO, evaluate this payment request:

Recipient: {recipient}
Amount: ${amount:,.2f}
Purpose: {purpose}
Category: {category}

Assess:
1. Financial impact and budget availability
2. Compliance and regulatory requirements
3. Risk factors and mitigation
4. Ethical considerations

Decision reasoning:"""
        
        reasoning = self._generate_with_llm(prompt)
        
        # Calculate EPI score
        # For payments, profit is negative (expense), but we assess value
        # Normalize amount to 0-1 scale (assume max payment is $1M)
        normalized_amount = min(amount / 1000000, 1.0)
        
        # Ethics score from factors or default
        if ethical_factors:
            ethics_score = sum(ethical_factors.values()) / len(ethical_factors)
        else:
            # Default ethics based on category
            ethics_map = {
                'compensation': 0.9,  # High ethical value
                'operational': 0.7,
                'investment': 0.6,
                'vendor': 0.75,
                'charitable': 0.95
            }
            ethics_score = ethics_map.get(category, 0.7)
        
        # For payments, we invert the profit calculation
        # High value payments with high ethics get good EPI
        value_score = 1.0 - (normalized_amount * 0.5)  # Smaller payments = higher value score
        
        epi_scores = EPIScores(
            profit=value_score,
            ethics=ethics_score,
            violations=[],
            stakeholder_sentiment=ethical_factors.get('stakeholder_sentiment', 0.7) if ethical_factors else 0.7,
            transparency_score=0.9,  # Payments are transparent
            sustainability_score=ethical_factors.get('sustainability', 0.7) if ethical_factors else 0.7,
            compliance_score=0.9  # Assume compliance unless flagged
        )
        
        epi_result = self.epi_calculator.compute_epi(epi_scores)
        
        # Check budget availability
        budget_available = amount <= self.treasury_balance
        
        # Compliance check
        compliance_status = "compliant"
        if amount > 100000:
            compliance_status = "requires_guardian_approval"
        
        # Approval decision
        approved = (
            epi_result.is_valid and
            epi_result.epi_score >= self.epi_threshold and
            budget_available and
            compliance_status == "compliant"
        )
        
        # Risk assessment
        if amount > 500000:
            risk = "high"
        elif amount > 100000:
            risk = "medium"
        else:
            risk = "low"
        
        # Create decision
        decision = PaymentDecision(
            payment_id=f"PAY-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
            recipient=recipient,
            amount=amount,
            purpose=purpose,
            category=category,
            epi_score=epi_result.epi_score,
            approved=approved,
            risk_assessment=risk,
            compliance_status=compliance_status,
            reasoning=reasoning,
            timestamp=datetime.now()
        )
        
        # Update treasury if approved
        if approved:
            self.treasury_balance -= amount
        
        # Log decision
        self._log_payment_decision(decision, epi_result)
        
        # Store decision
        self.payments.append(decision)
        
        return decision
    
    def allocate_budget(
        self,
        department: str,
        amount: float,
        purpose: str,
        expected_roi: float,
        ethical_factors: Optional[Dict[str, float]] = None
    ) -> BudgetAllocation:
        """
        Allocate budget to a department with EPI validation.
        
        Args:
            department: Department name
            amount: Budget amount
            purpose: Purpose of allocation
            expected_roi: Expected return on investment
            ethical_factors: Ethical considerations
            
        Returns:
            BudgetAllocation decision
        """
        # Calculate EPI
        ethics_score = sum(ethical_factors.values()) / len(ethical_factors) if ethical_factors else 0.7
        
        epi_scores = EPIScores(
            profit=expected_roi,
            ethics=ethics_score,
            violations=[],
            stakeholder_sentiment=0.7,
            transparency_score=0.8,
            sustainability_score=0.7,
            compliance_score=0.9
        )
        
        epi_result = self.epi_calculator.compute_epi(epi_scores)
        
        # Check constraints
        constraints = []
        if amount > self.treasury_balance * 0.3:
            constraints.append("Exceeds 30% of treasury")
        if expected_roi < 0.1:
            constraints.append("Low expected ROI")
        
        # Approval
        approved = (
            epi_result.is_valid and
            epi_result.epi_score >= self.epi_threshold and
            len(constraints) == 0
        )
        
        allocation = BudgetAllocation(
            allocation_id=f"ALLOC-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
            department=department,
            amount=amount,
            purpose=purpose,
            epi_score=epi_result.epi_score,
            approved=approved,
            constraints=constraints,
            expected_roi=expected_roi,
            timestamp=datetime.now()
        )
        
        # Log decision
        self._log_allocation_decision(allocation, epi_result)
        
        self.allocations.append(allocation)
        
        return allocation
    
    def _log_payment_decision(self, decision: PaymentDecision, epi_result):
        """Log payment decision to Trust Stack."""
        try:
            evaluations = [
                self.event_logger.create_evaluation(
                    evaluator="epi-calculator",
                    category="EPI",
                    result="pass" if decision.approved else "fail",
                    confidence=epi_result.confidence
                ),
                self.event_logger.create_evaluation(
                    evaluator="compliance-check",
                    category="Compliance",
                    result="pass" if decision.compliance_status == "compliant" else "warning",
                    confidence=0.95
                )
            ]
            
            event = self.event_logger.log_event(
                tenant_id="microai-dao",
                agent_id=self.agent_id,
                action_type="payment",
                input_data=f"Payment to {decision.recipient}: ${decision.amount:,.2f} for {decision.purpose}",
                output_data=f"{'Approved' if decision.approved else 'Rejected'}: EPI={decision.epi_score:.3f}",
                policy_version="v1.0.0",
                epi_score=decision.epi_score,
                model=self.model_name,
                tools_called=["epi_calculator", "compliance_checker"],
                evaluations=evaluations
            )
            
            print(f"✓ Payment decision logged: {event.event_id}")
            
        except Exception as e:
            print(f"Warning: Could not log payment decision: {e}")
    
    def _log_allocation_decision(self, allocation: BudgetAllocation, epi_result):
        """Log budget allocation to Trust Stack."""
        try:
            evaluations = [
                self.event_logger.create_evaluation(
                    evaluator="epi-calculator",
                    category="EPI",
                    result="pass" if allocation.approved else "fail",
                    confidence=epi_result.confidence
                )
            ]
            
            event = self.event_logger.log_event(
                tenant_id="microai-dao",
                agent_id=self.agent_id,
                action_type="budget_allocation",
                input_data=f"Allocate ${allocation.amount:,.2f} to {allocation.department} for {allocation.purpose}",
                output_data=f"{'Approved' if allocation.approved else 'Rejected'}: EPI={allocation.epi_score:.3f}",
                policy_version="v1.0.0",
                epi_score=allocation.epi_score,
                model=self.model_name,
                tools_called=["epi_calculator", "budget_analyzer"],
                evaluations=evaluations
            )
            
        except Exception as e:
            print(f"Warning: Could not log allocation: {e}")
    
    def get_treasury_status(self) -> Dict[str, Any]:
        """Get current treasury status."""
        total_payments = sum(p.amount for p in self.payments if p.approved)
        total_allocations = sum(a.amount for a in self.allocations if a.approved)
        
        return {
            'balance': self.treasury_balance,
            'total_payments': total_payments,
            'total_allocations': total_allocations,
            'payment_count': len([p for p in self.payments if p.approved]),
            'allocation_count': len([a for a in self.allocations if a.approved])
        }
    
    def get_stats(self) -> Dict[str, Any]:
        """Get CFO-AI statistics."""
        if not self.payments:
            return {
                'total_payments': 0,
                'approved_payments': 0,
                'rejected_payments': 0,
                'average_epi': 0,
                'approval_rate': 0,
                'treasury_balance': self.treasury_balance
            }
        
        approved = sum(1 for p in self.payments if p.approved)
        total = len(self.payments)
        avg_epi = sum(p.epi_score for p in self.payments) / total
        
        return {
            'total_payments': total,
            'approved_payments': approved,
            'rejected_payments': total - approved,
            'average_epi': round(avg_epi, 3),
            'approval_rate': round(approved / total * 100, 1),
            'treasury_balance': self.treasury_balance,
            'model': self.model_name
        }


# Example usage
if __name__ == "__main__":
    cfo = CFOAI(use_local_model=False)
    
    # Approve a payment
    payment = cfo.approve_payment(
        recipient="Healthcare AI Vendor",
        amount=50000,
        purpose="AI diagnostic system license",
        category="operational",
        ethical_factors={
            'patient_benefit': 0.9,
            'data_privacy': 0.85,
            'transparency': 0.8
        }
    )
    
    print(f"\n{'='*60}")
    print(f"Payment Decision: {payment.recipient}")
    print(f"{'='*60}")
    print(f"Amount: ${payment.amount:,.2f}")
    print(f"EPI Score: {payment.epi_score:.3f}")
    print(f"Status: {'✓ APPROVED' if payment.approved else '✗ REJECTED'}")
    print(f"Risk: {payment.risk_assessment.upper()}")
    print(f"Compliance: {payment.compliance_status}")
    print(f"\nReasoning:\n{payment.reasoning}")
    print(f"{'='*60}\n")
    
    # Get treasury status
    treasury = cfo.get_treasury_status()
    print("Treasury Status:")
    print(json.dumps(treasury, indent=2))
