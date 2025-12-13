"""
ExecAI Trust Stack - Cryptographic Verification Layer for AI Governance

This module provides tamper-evident event logging, Merkle tree anchoring,
attestation generation, and cryptographic proof verification for the
MicroAI DAO governance system.
"""

from .event_logger import EventLogger, TrustEvent
from .merkle_tree import MerkleTree, MerkleProof
from .attestation import AttestationGenerator, Attestation
from .verifier import ProofVerifier, VerificationResult
from .trust_metrics import TrustMetricsCalculator, TrustMetrics, QualitativeTrustIndicators, CertificationLevel
from .decision_verifier import DecisionVerifier, Decision, VerificationResult as DecisionVerificationResult
from .guardian_system import GuardianSystem, Guardian, GuardianRole, GuardianAction

__all__ = [
    'EventLogger',
    'TrustEvent',
    'MerkleTree',
    'MerkleProof',
    'AttestationGenerator',
    'Attestation',
    'ProofVerifier',
    'VerificationResult',
    'TrustMetricsCalculator',
    'TrustMetrics',
    'QualitativeTrustIndicators',
    'CertificationLevel',
    'DecisionVerifier',
    'Decision',
    'DecisionVerificationResult',
    'GuardianSystem',
    'Guardian',
    'GuardianRole',
    'GuardianAction',
]

__version__ = '1.0.0'
