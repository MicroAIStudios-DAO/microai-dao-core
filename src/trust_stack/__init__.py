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

__all__ = [
    'EventLogger',
    'TrustEvent',
    'MerkleTree',
    'MerkleProof',
    'AttestationGenerator',
    'Attestation',
    'ProofVerifier',
    'VerificationResult',
]

__version__ = '1.0.0'
