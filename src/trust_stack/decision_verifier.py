"""
Decision Verifier
=================

Implements the verification mechanism from synthetic_trust.md.
Verifies AI decisions through cryptographic proofs, EPI validation,
and reasoning integrity checks.

References:
- synthetic_trust.md: Verification mechanisms specification
"""

from typing import Dict, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
import hashlib
import hmac


@dataclass
class Decision:
    """AI decision structure."""
    decision_id: str
    agent_id: str
    action_type: str
    timestamp: str
    profit_score: float
    ethics_score: float
    violations: list
    epi_score: float
    reasoning: str
    signature: str
    reasoning_hash: str


@dataclass
class VerificationResult:
    """Result of decision verification."""
    is_valid: bool
    signature_valid: bool
    epi_valid: bool
    reasoning_valid: bool
    confidence: float
    details: Dict
    timestamp: datetime


class DecisionVerifier:
    """
    Verify AI decisions through cryptographic proofs.
    
    Implements the verify_decision() function from synthetic_trust.md:
    1. Verify signature
    2. Verify EPI calculation
    3. Verify reasoning integrity
    """
    
    def __init__(self, secret_key: Optional[bytes] = None, epi_threshold: float = 0.7):
        """
        Initialize decision verifier.
        
        Args:
            secret_key: HMAC secret key for signature verification
            epi_threshold: Minimum EPI score for approval
        """
        self.secret_key = secret_key or b"microai-dao-secret-key"
        self.epi_threshold = epi_threshold
    
    def verify_decision(
        self,
        decision: Decision,
        full_reasoning: Optional[str] = None
    ) -> VerificationResult:
        """
        Verify an AI decision through cryptographic proofs.
        
        This implements the verification process from synthetic_trust.md:
        1. Verify signature (proving the AI agent authorized it)
        2. Verify EPI calculation (proving it met threshold)
        3. Verify reasoning integrity (linking to full thought log)
        
        Args:
            decision: Decision object to verify
            full_reasoning: Full reasoning text (optional, for integrity check)
            
        Returns:
            VerificationResult with validation status and details
        """
        details = {}
        
        # Step 1: Verify signature
        signature_valid = self._verify_signature(decision)
        details['signature_check'] = {
            'valid': signature_valid,
            'agent_id': decision.agent_id,
            'timestamp': decision.timestamp
        }
        
        # Step 2: Verify EPI calculation
        epi_valid, calculated_epi = self._verify_epi(decision)
        details['epi_check'] = {
            'valid': epi_valid,
            'claimed_epi': decision.epi_score,
            'calculated_epi': calculated_epi,
            'threshold': self.epi_threshold,
            'meets_threshold': calculated_epi >= self.epi_threshold
        }
        
        # Step 3: Verify reasoning integrity
        reasoning_valid = self._verify_reasoning_integrity(decision, full_reasoning)
        details['reasoning_check'] = {
            'valid': reasoning_valid,
            'hash_match': reasoning_valid,
            'reasoning_hash': decision.reasoning_hash
        }
        
        # Calculate overall validity
        is_valid = signature_valid and epi_valid and reasoning_valid
        
        # Calculate confidence score
        confidence = self._calculate_confidence(
            signature_valid,
            epi_valid,
            reasoning_valid,
            calculated_epi
        )
        
        return VerificationResult(
            is_valid=is_valid,
            signature_valid=signature_valid,
            epi_valid=epi_valid,
            reasoning_valid=reasoning_valid,
            confidence=confidence,
            details=details,
            timestamp=datetime.now()
        )
    
    def _verify_signature(self, decision: Decision) -> bool:
        """
        Verify HMAC signature of decision.
        
        Args:
            decision: Decision to verify
            
        Returns:
            True if signature is valid
        """
        # Construct message to sign
        message = f"{decision.decision_id}|{decision.agent_id}|{decision.timestamp}|{decision.epi_score}"
        message_bytes = message.encode('utf-8')
        
        # Calculate expected signature
        expected_signature = hmac.new(
            self.secret_key,
            message_bytes,
            hashlib.sha256
        ).hexdigest()
        
        # Compare signatures (constant-time comparison)
        return hmac.compare_digest(expected_signature, decision.signature)
    
    def _verify_epi(self, decision: Decision) -> Tuple[bool, float]:
        """
        Verify EPI calculation.
        
        Args:
            decision: Decision to verify
            
        Returns:
            Tuple of (is_valid, calculated_epi)
        """
        # Recalculate EPI from components
        profit = decision.profit_score
        ethics = decision.ethics_score
        violations = decision.violations
        
        # Harmonic mean
        if profit == 0 or ethics == 0:
            harmonic_mean = 0.0
        else:
            harmonic_mean = 2 * profit * ethics / (profit + ethics)
        
        # Balance penalty (golden ratio)
        PHI = (5 ** 0.5 - 1) / 2  # ~0.618
        imbalance = abs(profit - ethics)
        balance_penalty = 1 - PHI * imbalance
        
        # Trust accumulator (geometric product)
        trust = 1.0
        for violation in violations:
            trust *= (1 - violation)
            if trust < 1e-6:
                trust = 0.0
                break
        
        # Calculate EPI
        calculated_epi = harmonic_mean * balance_penalty * trust
        
        # Check if it matches claimed EPI (with small tolerance for floating point)
        tolerance = 0.001
        epi_match = abs(calculated_epi - decision.epi_score) < tolerance
        
        # Check if it meets threshold
        meets_threshold = calculated_epi >= self.epi_threshold
        
        is_valid = epi_match and meets_threshold
        
        return is_valid, calculated_epi
    
    def _verify_reasoning_integrity(
        self,
        decision: Decision,
        full_reasoning: Optional[str] = None
    ) -> bool:
        """
        Verify reasoning integrity through hash comparison.
        
        Args:
            decision: Decision to verify
            full_reasoning: Full reasoning text (if available)
            
        Returns:
            True if reasoning hash matches
        """
        if full_reasoning is None:
            # If full reasoning not provided, check if hash exists
            return bool(decision.reasoning_hash)
        
        # Calculate hash of provided reasoning
        calculated_hash = hashlib.sha256(full_reasoning.encode('utf-8')).hexdigest()
        
        # Compare with claimed hash
        return calculated_hash == decision.reasoning_hash
    
    def _calculate_confidence(
        self,
        signature_valid: bool,
        epi_valid: bool,
        reasoning_valid: bool,
        calculated_epi: float
    ) -> float:
        """
        Calculate confidence score for verification.
        
        Args:
            signature_valid: Signature verification result
            epi_valid: EPI verification result
            reasoning_valid: Reasoning verification result
            calculated_epi: Calculated EPI score
            
        Returns:
            Confidence score (0-1)
        """
        # Base confidence from verification checks
        checks_passed = sum([signature_valid, epi_valid, reasoning_valid])
        base_confidence = checks_passed / 3
        
        # Boost confidence if EPI is well above threshold
        if calculated_epi > self.epi_threshold + 0.1:
            epi_boost = min(0.1, (calculated_epi - self.epi_threshold) * 0.5)
        else:
            epi_boost = 0
        
        confidence = min(1.0, base_confidence + epi_boost)
        
        return confidence
    
    def verify_batch(
        self,
        decisions: list[Decision]
    ) -> Dict:
        """
        Verify a batch of decisions.
        
        Args:
            decisions: List of decisions to verify
            
        Returns:
            Dictionary with batch verification results
        """
        results = []
        valid_count = 0
        invalid_count = 0
        
        for decision in decisions:
            result = self.verify_decision(decision)
            results.append(result)
            
            if result.is_valid:
                valid_count += 1
            else:
                invalid_count += 1
        
        # Calculate batch statistics
        avg_confidence = sum(r.confidence for r in results) / len(results) if results else 0
        
        return {
            'total': len(decisions),
            'valid': valid_count,
            'invalid': invalid_count,
            'validity_rate': valid_count / len(decisions) if decisions else 0,
            'avg_confidence': avg_confidence,
            'results': results
        }
    
    def generate_verification_report(
        self,
        result: VerificationResult,
        decision: Decision
    ) -> str:
        """
        Generate human-readable verification report.
        
        Args:
            result: VerificationResult object
            decision: Decision that was verified
            
        Returns:
            Formatted verification report
        """
        report = []
        report.append("=" * 70)
        report.append("  AI DECISION VERIFICATION REPORT")
        report.append("=" * 70)
        report.append("")
        
        # Decision info
        report.append(f"Decision ID: {decision.decision_id}")
        report.append(f"Agent: {decision.agent_id}")
        report.append(f"Action: {decision.action_type}")
        report.append(f"Timestamp: {decision.timestamp}")
        report.append("")
        
        # Overall result
        status = "✅ VALID" if result.is_valid else "❌ INVALID"
        report.append(f"Verification Status: {status}")
        report.append(f"Confidence: {result.confidence:.1%}")
        report.append("")
        
        # Detailed checks
        report.append("Verification Checks:")
        report.append("")
        
        # Signature check
        sig_status = "✅ PASS" if result.signature_valid else "❌ FAIL"
        report.append(f"  1. Signature Verification: {sig_status}")
        report.append(f"     Agent ID: {decision.agent_id}")
        report.append(f"     Timestamp: {decision.timestamp}")
        report.append("")
        
        # EPI check
        epi_status = "✅ PASS" if result.epi_valid else "❌ FAIL"
        report.append(f"  2. EPI Verification: {epi_status}")
        report.append(f"     Claimed EPI: {decision.epi_score:.3f}")
        report.append(f"     Calculated EPI: {result.details['epi_check']['calculated_epi']:.3f}")
        report.append(f"     Threshold: {self.epi_threshold:.3f}")
        meets = "Yes" if result.details['epi_check']['meets_threshold'] else "No"
        report.append(f"     Meets Threshold: {meets}")
        report.append("")
        
        # Reasoning check
        reasoning_status = "✅ PASS" if result.reasoning_valid else "❌ FAIL"
        report.append(f"  3. Reasoning Integrity: {reasoning_status}")
        report.append(f"     Hash Match: {result.details['reasoning_check']['hash_match']}")
        report.append(f"     Reasoning Hash: {decision.reasoning_hash[:16]}...")
        report.append("")
        
        # Components
        report.append("EPI Components:")
        report.append(f"  Profit Score: {decision.profit_score:.3f}")
        report.append(f"  Ethics Score: {decision.ethics_score:.3f}")
        report.append(f"  Violations: {len(decision.violations)}")
        report.append("")
        
        report.append("=" * 70)
        
        return "\n".join(report)


# Example usage
if __name__ == "__main__":
    # Create a sample decision
    decision = Decision(
        decision_id="dec_001",
        agent_id="CEO-AI",
        action_type="strategic_proposal",
        timestamp="2025-12-12T10:30:00",
        profit_score=0.85,
        ethics_score=0.80,
        violations=[],
        epi_score=0.823,
        reasoning="Healthcare AI investment aligns with ethical guidelines...",
        signature="",  # Would be calculated
        reasoning_hash=hashlib.sha256(b"Healthcare AI investment aligns with ethical guidelines...").hexdigest()
    )
    
    # Calculate signature
    verifier = DecisionVerifier()
    message = f"{decision.decision_id}|{decision.agent_id}|{decision.timestamp}|{decision.epi_score}"
    decision.signature = hmac.new(
        verifier.secret_key,
        message.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()
    
    # Verify decision
    result = verifier.verify_decision(decision, decision.reasoning)
    
    # Print report
    report = verifier.generate_verification_report(result, decision)
    print(report)
