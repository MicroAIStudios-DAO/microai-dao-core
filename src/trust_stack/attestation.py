"""
Attestation Generator - Machine-readable attestation bundles for releases.

Generates signed attestation bundles containing model cards, SBOMs,
evaluation summaries, and Merkle roots for compliance and auditing.
"""

import json
import hashlib
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
import hmac


@dataclass
class EvalSummary:
    """Evaluation summary statistics."""
    coverage_pct: float  # % of requests evaluated
    pass_rate: float  # % of evaluations that passed
    last_red_team: str  # Date of last red team exercise
    categories: Dict[str, float]  # Pass rate by category
    
    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class Attestation:
    """
    Release attestation bundle.
    
    Contains all verifiable claims about a release including
    model card, SBOM, evaluation results, and log anchors.
    """
    release_id: str
    release_date: str
    model_card: str  # URI or hash
    sbom: str  # SPDX/CycloneDX hash
    eval_summary: Dict
    log_root: str  # Merkle root of event logs
    policy_version: str
    compliance_frameworks: List[str]  # SOC2, ISO27001, etc.
    signatures: List[str]  # Multi-sig from guardians
    metadata: Dict
    
    def to_dict(self) -> dict:
        return asdict(self)
    
    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2)


class AttestationGenerator:
    """
    Generate and sign attestation bundles for releases.
    
    Features:
    - Model card integration
    - SBOM generation/hashing
    - Evaluation summary compilation
    - Multi-signature support
    - Compliance framework mapping
    """
    
    def __init__(self, signing_key: Optional[str] = None):
        """
        Initialize attestation generator.
        
        Args:
            signing_key: Secret key for signing attestations
        """
        self.signing_key = signing_key or 'default-attestation-key'
    
    def hash_content(self, content: str) -> str:
        """
        Generate SHA-256 hash of content.
        
        Args:
            content: Content to hash
            
        Returns:
            Hex-encoded hash
        """
        return hashlib.sha256(content.encode('utf-8')).hexdigest()
    
    def sign_attestation(self, attestation_data: dict) -> str:
        """
        Generate HMAC signature for attestation.
        
        Args:
            attestation_data: Attestation dictionary
            
        Returns:
            Hex-encoded signature
        """
        payload = json.dumps(attestation_data, sort_keys=True)
        return hmac.new(
            self.signing_key.encode('utf-8'),
            payload.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
    
    def generate_model_card(
        self,
        model_name: str,
        model_version: str,
        description: str,
        intended_use: str,
        limitations: str,
        training_data: str,
        performance_metrics: Dict[str, float]
    ) -> Dict:
        """
        Generate a model card.
        
        Args:
            model_name: Name of the model
            model_version: Version string
            description: Model description
            intended_use: Intended use cases
            limitations: Known limitations
            training_data: Training data description
            performance_metrics: Performance metrics
            
        Returns:
            Model card dictionary
        """
        model_card = {
            'name': model_name,
            'version': model_version,
            'description': description,
            'intended_use': intended_use,
            'limitations': limitations,
            'training_data': training_data,
            'performance_metrics': performance_metrics,
            'created_at': datetime.utcnow().isoformat() + 'Z'
        }
        
        # Hash the model card
        card_json = json.dumps(model_card, sort_keys=True)
        model_card['hash'] = self.hash_content(card_json)
        
        return model_card
    
    def generate_sbom(
        self,
        components: List[Dict[str, str]],
        format: str = 'SPDX'
    ) -> Dict:
        """
        Generate Software Bill of Materials.
        
        Args:
            components: List of software components
            format: SBOM format (SPDX or CycloneDX)
            
        Returns:
            SBOM dictionary
        """
        sbom = {
            'format': format,
            'version': '2.3' if format == 'SPDX' else '1.4',
            'components': components,
            'created_at': datetime.utcnow().isoformat() + 'Z'
        }
        
        # Hash the SBOM
        sbom_json = json.dumps(sbom, sort_keys=True)
        sbom['hash'] = self.hash_content(sbom_json)
        
        return sbom
    
    def compile_eval_summary(
        self,
        total_requests: int,
        evaluated_requests: int,
        passed_requests: int,
        category_results: Dict[str, Dict[str, int]],
        last_red_team_date: str
    ) -> EvalSummary:
        """
        Compile evaluation summary from statistics.
        
        Args:
            total_requests: Total number of requests
            evaluated_requests: Number of evaluated requests
            passed_requests: Number that passed all evaluations
            category_results: Results by category
            last_red_team_date: Date of last red team exercise
            
        Returns:
            EvalSummary object
        """
        coverage_pct = (evaluated_requests / total_requests * 100) if total_requests > 0 else 0
        pass_rate = (passed_requests / evaluated_requests * 100) if evaluated_requests > 0 else 0
        
        # Calculate pass rate by category
        categories = {}
        for category, results in category_results.items():
            total = results.get('total', 0)
            passed = results.get('passed', 0)
            categories[category] = (passed / total * 100) if total > 0 else 0
        
        return EvalSummary(
            coverage_pct=round(coverage_pct, 2),
            pass_rate=round(pass_rate, 2),
            last_red_team=last_red_team_date,
            categories=categories
        )
    
    def generate_attestation(
        self,
        release_id: str,
        model_card: Dict,
        sbom: Dict,
        eval_summary: EvalSummary,
        log_root: str,
        policy_version: str,
        compliance_frameworks: Optional[List[str]] = None,
        metadata: Optional[Dict] = None
    ) -> Attestation:
        """
        Generate a complete attestation bundle.
        
        Args:
            release_id: Release identifier (e.g., 'v1.0.0')
            model_card: Model card dictionary
            sbom: SBOM dictionary
            eval_summary: Evaluation summary
            log_root: Merkle root of event logs
            policy_version: Policy version used
            compliance_frameworks: List of compliance frameworks
            metadata: Additional metadata
            
        Returns:
            Signed Attestation
        """
        release_date = datetime.utcnow().isoformat() + 'Z'
        
        # Prepare attestation data
        attestation_data = {
            'release_id': release_id,
            'release_date': release_date,
            'model_card': model_card.get('hash', ''),
            'sbom': sbom.get('hash', ''),
            'eval_summary': eval_summary.to_dict(),
            'log_root': log_root,
            'policy_version': policy_version,
            'compliance_frameworks': compliance_frameworks or [],
            'metadata': metadata or {}
        }
        
        # Sign attestation
        signature = self.sign_attestation(attestation_data)
        
        # Create attestation
        attestation = Attestation(
            release_id=release_id,
            release_date=release_date,
            model_card=model_card.get('hash', ''),
            sbom=sbom.get('hash', ''),
            eval_summary=eval_summary.to_dict(),
            log_root=log_root,
            policy_version=policy_version,
            compliance_frameworks=compliance_frameworks or [],
            signatures=[signature],
            metadata=metadata or {}
        )
        
        return attestation
    
    def add_guardian_signature(
        self,
        attestation: Attestation,
        guardian_key: str
    ) -> Attestation:
        """
        Add a guardian signature to an attestation (multi-sig).
        
        Args:
            attestation: Existing attestation
            guardian_key: Guardian's signing key
            
        Returns:
            Attestation with additional signature
        """
        # Sign the attestation data
        attestation_data = attestation.to_dict()
        attestation_data.pop('signatures')  # Remove existing signatures
        
        guardian_sig = hmac.new(
            guardian_key.encode('utf-8'),
            json.dumps(attestation_data, sort_keys=True).encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        
        attestation.signatures.append(guardian_sig)
        return attestation
    
    def verify_attestation(
        self,
        attestation: Attestation,
        expected_signature: str
    ) -> bool:
        """
        Verify an attestation signature.
        
        Args:
            attestation: Attestation to verify
            expected_signature: Expected signature
            
        Returns:
            True if valid, False otherwise
        """
        attestation_data = attestation.to_dict()
        attestation_data.pop('signatures')
        
        computed_sig = self.sign_attestation(attestation_data)
        return hmac.compare_digest(computed_sig, expected_signature)
    
    def export_attestation(
        self,
        attestation: Attestation,
        filepath: str
    ) -> None:
        """
        Export attestation to JSON file.
        
        Args:
            attestation: Attestation to export
            filepath: Output file path
        """
        with open(filepath, 'w') as f:
            f.write(attestation.to_json())


# Example usage
if __name__ == "__main__":
    generator = AttestationGenerator()
    
    # Generate model card
    model_card = generator.generate_model_card(
        model_name="CEO-AI",
        model_version="1.0.0",
        description="Strategic decision-making AI with EPI constraints",
        intended_use="Strategic planning and proposal generation for DAO governance",
        limitations="Requires human guardian oversight for high-risk decisions",
        training_data="Business strategy corpus + ethical decision-making examples",
        performance_metrics={
            'epi_compliance_rate': 0.95,
            'proposal_approval_rate': 0.78,
            'decision_accuracy': 0.89
        }
    )
    
    # Generate SBOM
    sbom = generator.generate_sbom([
        {'name': 'transformers', 'version': '4.35.0', 'license': 'Apache-2.0'},
        {'name': 'torch', 'version': '2.1.0', 'license': 'BSD-3-Clause'},
        {'name': 'numpy', 'version': '1.24.3', 'license': 'BSD-3-Clause'}
    ])
    
    # Compile eval summary
    eval_summary = generator.compile_eval_summary(
        total_requests=10000,
        evaluated_requests=9500,
        passed_requests=9025,
        category_results={
            'PII': {'total': 9500, 'passed': 9400},
            'Safety': {'total': 9500, 'passed': 9300},
            'Bias': {'total': 9500, 'passed': 9100},
            'EPI': {'total': 9500, 'passed': 9025}
        },
        last_red_team_date='2025-12-01'
    )
    
    # Generate attestation
    attestation = generator.generate_attestation(
        release_id='v1.0.0',
        model_card=model_card,
        sbom=sbom,
        eval_summary=eval_summary,
        log_root='abc123...def456',
        policy_version='v1.0.0',
        compliance_frameworks=['SOC2', 'ISO27001'],
        metadata={'environment': 'production', 'region': 'us-west-2'}
    )
    
    print("Generated attestation:")
    print(attestation.to_json())
    
    # Verify attestation
    is_valid = generator.verify_attestation(attestation, attestation.signatures[0])
    print(f"\nAttestation valid: {is_valid}")
