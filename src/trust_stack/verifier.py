"""
Proof Verifier - Cryptographic proof verification for trust validation.

Provides verification of event signatures, Merkle proofs, and attestations
for the ExecAI Trust Stack.
"""

import hmac
import json
from typing import Optional, Dict, List
from dataclasses import dataclass
from enum import Enum

from .event_logger import TrustEvent, EventLogger
from .merkle_tree import MerkleProof, MerkleTree
from .attestation import Attestation, AttestationGenerator


class VerificationStatus(Enum):
    """Verification result status."""
    VALID = "valid"
    INVALID = "invalid"
    UNKNOWN = "unknown"
    ERROR = "error"


@dataclass
class VerificationResult:
    """Result of a verification operation."""
    status: VerificationStatus
    verified: bool
    message: str
    details: Dict
    
    def to_dict(self) -> dict:
        return {
            'status': self.status.value,
            'verified': self.verified,
            'message': self.message,
            'details': self.details
        }
    
    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2)


class ProofVerifier:
    """
    Cryptographic proof verifier for the Trust Stack.
    
    Verifies:
    - Event signatures
    - Merkle inclusion proofs
    - Attestation signatures
    - Complete verification chains
    """
    
    def __init__(self, signing_key: Optional[str] = None):
        """
        Initialize the proof verifier.
        
        Args:
            signing_key: Secret key for signature verification
        """
        self.event_logger = EventLogger(signing_key=signing_key)
        self.attestation_gen = AttestationGenerator(signing_key=signing_key)
    
    def verify_event_signature(self, event: TrustEvent) -> VerificationResult:
        """
        Verify the cryptographic signature of an event.
        
        Args:
            event: TrustEvent to verify
            
        Returns:
            VerificationResult
        """
        try:
            is_valid = self.event_logger.verify_event(event)
            
            if is_valid:
                return VerificationResult(
                    status=VerificationStatus.VALID,
                    verified=True,
                    message="Event signature is valid",
                    details={
                        'event_id': event.event_id,
                        'agent_id': event.agent_id,
                        'timestamp': event.timestamp,
                        'signature': event.signature[:16] + '...'
                    }
                )
            else:
                return VerificationResult(
                    status=VerificationStatus.INVALID,
                    verified=False,
                    message="Event signature is invalid",
                    details={
                        'event_id': event.event_id,
                        'reason': 'Signature mismatch'
                    }
                )
        
        except Exception as e:
            return VerificationResult(
                status=VerificationStatus.ERROR,
                verified=False,
                message=f"Error verifying event: {str(e)}",
                details={'error': str(e)}
            )
    
    def verify_merkle_proof(self, proof: MerkleProof) -> VerificationResult:
        """
        Verify a Merkle inclusion proof.
        
        Args:
            proof: MerkleProof to verify
            
        Returns:
            VerificationResult
        """
        try:
            is_valid = MerkleTree.verify_proof(proof)
            
            if is_valid:
                return VerificationResult(
                    status=VerificationStatus.VALID,
                    verified=True,
                    message="Merkle proof is valid",
                    details={
                        'leaf_hash': proof.leaf_hash[:16] + '...',
                        'root': proof.root[:16] + '...',
                        'proof_length': len(proof.siblings)
                    }
                )
            else:
                return VerificationResult(
                    status=VerificationStatus.INVALID,
                    verified=False,
                    message="Merkle proof is invalid",
                    details={
                        'leaf_hash': proof.leaf_hash[:16] + '...',
                        'reason': 'Proof does not match root'
                    }
                )
        
        except Exception as e:
            return VerificationResult(
                status=VerificationStatus.ERROR,
                verified=False,
                message=f"Error verifying Merkle proof: {str(e)}",
                details={'error': str(e)}
            )
    
    def verify_attestation(
        self,
        attestation: Attestation,
        expected_signatures: Optional[List[str]] = None
    ) -> VerificationResult:
        """
        Verify an attestation bundle.
        
        Args:
            attestation: Attestation to verify
            expected_signatures: Optional list of expected signatures
            
        Returns:
            VerificationResult
        """
        try:
            # Verify at least one signature
            if not attestation.signatures:
                return VerificationResult(
                    status=VerificationStatus.INVALID,
                    verified=False,
                    message="Attestation has no signatures",
                    details={'release_id': attestation.release_id}
                )
            
            # Verify first signature (primary)
            is_valid = self.attestation_gen.verify_attestation(
                attestation,
                attestation.signatures[0]
            )
            
            verified_sigs = 1 if is_valid else 0
            
            # Verify additional signatures if provided
            if expected_signatures:
                for expected_sig in expected_signatures:
                    if expected_sig in attestation.signatures:
                        verified_sigs += 1
            
            if is_valid:
                return VerificationResult(
                    status=VerificationStatus.VALID,
                    verified=True,
                    message=f"Attestation is valid ({verified_sigs} signatures verified)",
                    details={
                        'release_id': attestation.release_id,
                        'release_date': attestation.release_date,
                        'policy_version': attestation.policy_version,
                        'signatures_verified': verified_sigs,
                        'total_signatures': len(attestation.signatures),
                        'compliance_frameworks': attestation.compliance_frameworks
                    }
                )
            else:
                return VerificationResult(
                    status=VerificationStatus.INVALID,
                    verified=False,
                    message="Attestation signature is invalid",
                    details={
                        'release_id': attestation.release_id,
                        'reason': 'Primary signature mismatch'
                    }
                )
        
        except Exception as e:
            return VerificationResult(
                status=VerificationStatus.ERROR,
                verified=False,
                message=f"Error verifying attestation: {str(e)}",
                details={'error': str(e)}
            )
    
    def verify_complete_chain(
        self,
        event: TrustEvent,
        merkle_proof: MerkleProof,
        attestation: Attestation
    ) -> VerificationResult:
        """
        Verify a complete verification chain: event -> proof -> attestation.
        
        Args:
            event: TrustEvent
            merkle_proof: MerkleProof for the event
            attestation: Attestation containing the Merkle root
            
        Returns:
            VerificationResult with complete chain verification
        """
        results = {
            'event_signature': False,
            'merkle_proof': False,
            'attestation': False,
            'chain_integrity': False
        }
        
        details = {}
        
        try:
            # Step 1: Verify event signature
            event_result = self.verify_event_signature(event)
            results['event_signature'] = event_result.verified
            details['event'] = event_result.details
            
            if not results['event_signature']:
                return VerificationResult(
                    status=VerificationStatus.INVALID,
                    verified=False,
                    message="Event signature verification failed",
                    details=details
                )
            
            # Step 2: Verify Merkle proof
            proof_result = self.verify_merkle_proof(merkle_proof)
            results['merkle_proof'] = proof_result.verified
            details['merkle_proof'] = proof_result.details
            
            if not results['merkle_proof']:
                return VerificationResult(
                    status=VerificationStatus.INVALID,
                    verified=False,
                    message="Merkle proof verification failed",
                    details=details
                )
            
            # Step 3: Verify attestation
            attestation_result = self.verify_attestation(attestation)
            results['attestation'] = attestation_result.verified
            details['attestation'] = attestation_result.details
            
            if not results['attestation']:
                return VerificationResult(
                    status=VerificationStatus.INVALID,
                    verified=False,
                    message="Attestation verification failed",
                    details=details
                )
            
            # Step 4: Verify chain integrity (Merkle root matches attestation)
            if merkle_proof.root == attestation.log_root:
                results['chain_integrity'] = True
                details['chain_integrity'] = {
                    'merkle_root': merkle_proof.root[:16] + '...',
                    'attestation_root': attestation.log_root[:16] + '...',
                    'match': True
                }
            else:
                details['chain_integrity'] = {
                    'merkle_root': merkle_proof.root[:16] + '...',
                    'attestation_root': attestation.log_root[:16] + '...',
                    'match': False
                }
                return VerificationResult(
                    status=VerificationStatus.INVALID,
                    verified=False,
                    message="Chain integrity check failed: Merkle root mismatch",
                    details=details
                )
            
            # All checks passed
            return VerificationResult(
                status=VerificationStatus.VALID,
                verified=True,
                message="Complete verification chain is valid",
                details={
                    'checks': results,
                    'event_id': event.event_id,
                    'agent_id': event.agent_id,
                    'release_id': attestation.release_id,
                    **details
                }
            )
        
        except Exception as e:
            return VerificationResult(
                status=VerificationStatus.ERROR,
                verified=False,
                message=f"Error in chain verification: {str(e)}",
                details={'error': str(e), 'results': results}
            )
    
    def verify_epi_compliance(
        self,
        event: TrustEvent,
        threshold: float = 0.7
    ) -> VerificationResult:
        """
        Verify that an event meets EPI compliance threshold.
        
        Args:
            event: TrustEvent to check
            threshold: Minimum EPI score required
            
        Returns:
            VerificationResult
        """
        try:
            if event.epi_score is None:
                return VerificationResult(
                    status=VerificationStatus.UNKNOWN,
                    verified=False,
                    message="Event has no EPI score",
                    details={'event_id': event.event_id}
                )
            
            is_compliant = event.epi_score >= threshold
            
            if is_compliant:
                return VerificationResult(
                    status=VerificationStatus.VALID,
                    verified=True,
                    message=f"Event meets EPI threshold ({event.epi_score:.3f} >= {threshold})",
                    details={
                        'event_id': event.event_id,
                        'agent_id': event.agent_id,
                        'epi_score': event.epi_score,
                        'threshold': threshold,
                        'margin': event.epi_score - threshold
                    }
                )
            else:
                return VerificationResult(
                    status=VerificationStatus.INVALID,
                    verified=False,
                    message=f"Event below EPI threshold ({event.epi_score:.3f} < {threshold})",
                    details={
                        'event_id': event.event_id,
                        'agent_id': event.agent_id,
                        'epi_score': event.epi_score,
                        'threshold': threshold,
                        'deficit': threshold - event.epi_score
                    }
                )
        
        except Exception as e:
            return VerificationResult(
                status=VerificationStatus.ERROR,
                verified=False,
                message=f"Error verifying EPI compliance: {str(e)}",
                details={'error': str(e)}
            )


# Example usage
if __name__ == "__main__":
    from .event_logger import EventLogger
    from .merkle_tree import MerkleTree
    from .attestation import AttestationGenerator, EvalSummary
    
    # Create verifier
    verifier = ProofVerifier()
    
    # Create and verify an event
    logger = EventLogger()
    event = logger.log_event(
        tenant_id="microai-dao",
        agent_id="CEO-AI",
        action_type="strategic_proposal",
        input_data="Propose healthcare AI investment",
        output_data="Approved: $500k investment",
        policy_version="v1.0.0",
        epi_score=0.85
    )
    
    print("=== Event Signature Verification ===")
    result = verifier.verify_event_signature(event)
    print(result.to_json())
    
    # Create and verify Merkle proof
    event_hashes = logger.get_daily_hashes("2025-12-12")
    if event_hashes:
        tree = MerkleTree(event_hashes)
        proof = tree.get_proof(event_hashes[0])
        
        if proof:
            print("\n=== Merkle Proof Verification ===")
            result = verifier.verify_merkle_proof(proof)
            print(result.to_json())
    
    # Verify EPI compliance
    print("\n=== EPI Compliance Verification ===")
    result = verifier.verify_epi_compliance(event, threshold=0.7)
    print(result.to_json())
