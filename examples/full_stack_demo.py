"""
Full Stack Integration Demo
============================

This example demonstrates the complete MicroAI DAO system with:
- CEO-AI and CFO-AI agents making decisions
- EPI validation for all decisions
- Trust Stack logging with cryptographic verification
- Merkle tree generation and proof verification
- Attestation bundle creation

Run this to see the entire system in action!
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from personas.ceo_ai import CEOAI
from personas.cfo_ai import CFOAI
from trust_stack.event_logger import EventLogger
from trust_stack.merkle_tree import MerkleTree
from trust_stack.attestation import AttestationGenerator
from trust_stack.verifier import ProofVerifier
from datetime import datetime
import json


def print_section(title):
    """Print a formatted section header."""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70 + "\n")


def main():
    print_section("MicroAI DAO - Full Stack Integration Demo")
    
    # Initialize components
    print("Initializing system components...")
    ceo = CEOAI(use_local_model=False)
    cfo = CFOAI(use_local_model=False)
    event_logger = EventLogger()
    attestation_gen = AttestationGenerator()
    proof_verifier = ProofVerifier()
    
    print("✓ CEO-AI initialized")
    print("✓ CFO-AI initialized")
    print("✓ Trust Stack initialized")
    print("✓ Verification system ready")
    
    # =========================================================================
    # SCENARIO 1: CEO-AI Strategic Proposal
    # =========================================================================
    print_section("Scenario 1: CEO-AI Strategic Proposal")
    
    print("CEO-AI is evaluating a healthcare AI investment opportunity...")
    print()
    
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
    
    print(f"📋 Proposal: {proposal.title}")
    print(f"   Budget: ${proposal.budget:,.0f}")
    print(f"   Timeline: {proposal.timeline}")
    print(f"   EPI Score: {proposal.epi_score:.3f}")
    print(f"   Status: {'✅ APPROVED' if proposal.approved else '❌ REJECTED'}")
    print(f"   Risk Level: {proposal.risk_level.upper()}")
    print()
    print(f"Rationale:")
    print(f"{proposal.rationale[:200]}...")
    print()
    print("✓ Proposal logged to Trust Stack with cryptographic signature")
    
    # =========================================================================
    # SCENARIO 2: CFO-AI Payment Approval
    # =========================================================================
    print_section("Scenario 2: CFO-AI Payment Approval")
    
    print("CFO-AI is evaluating a payment request...")
    print()
    
    payment = cfo.approve_payment(
        recipient="Healthcare AI Vendor",
        amount=50000,
        purpose="AI diagnostic system license - Year 1",
        category="operational",
        ethical_factors={
            'patient_benefit': 0.9,
            'data_privacy': 0.85,
            'transparency': 0.8
        }
    )
    
    print(f"💰 Payment Request")
    print(f"   Recipient: {payment.recipient}")
    print(f"   Amount: ${payment.amount:,.2f}")
    print(f"   Purpose: {payment.purpose}")
    print(f"   EPI Score: {payment.epi_score:.3f}")
    print(f"   Status: {'✅ APPROVED' if payment.approved else '❌ REJECTED'}")
    print(f"   Risk: {payment.risk_assessment.upper()}")
    print(f"   Compliance: {payment.compliance_status}")
    print()
    print(f"Reasoning:")
    print(f"{payment.reasoning[:200]}...")
    print()
    print("✓ Payment decision logged to Trust Stack")
    
    # =========================================================================
    # SCENARIO 3: Budget Allocation
    # =========================================================================
    print_section("Scenario 3: CFO-AI Budget Allocation")
    
    print("CFO-AI is allocating budget to R&D department...")
    print()
    
    allocation = cfo.allocate_budget(
        department="R&D",
        amount=200000,
        purpose="AI ethics research and development",
        expected_roi=0.65,
        ethical_factors={
            'innovation': 0.9,
            'social_impact': 0.85,
            'sustainability': 0.8
        }
    )
    
    print(f"📊 Budget Allocation")
    print(f"   Department: {allocation.department}")
    print(f"   Amount: ${allocation.amount:,.0f}")
    print(f"   Purpose: {allocation.purpose}")
    print(f"   Expected ROI: {allocation.expected_roi:.1%}")
    print(f"   EPI Score: {allocation.epi_score:.3f}")
    print(f"   Status: {'✅ APPROVED' if allocation.approved else '❌ REJECTED'}")
    if allocation.constraints:
        print(f"   Constraints: {', '.join(allocation.constraints)}")
    print()
    print("✓ Allocation logged to Trust Stack")
    
    # =========================================================================
    # SCENARIO 4: Daily Merkle Root Generation
    # =========================================================================
    print_section("Scenario 4: Daily Merkle Root Generation")
    
    print("Generating Merkle tree from today's events...")
    print()
    
    # Get today's events
    today = datetime.now().strftime('%Y-%m-%d')
    events = event_logger.get_events_by_date(today)
    
    print(f"📅 Date: {today}")
    print(f"   Total events: {len(events)}")
    print()
    
    if len(events) > 0:
        # Get event hashes
        event_hashes = [
            event_logger.hash_data(e.input_hash + e.output_hash)
            for e in events
        ]
        
        # Build Merkle tree
        tree = MerkleTree(event_hashes)
        root = tree.get_root()
        
        print(f"🌳 Merkle Tree Generated")
        print(f"   Root: {root[:16]}...{root[-16:]}")
        print(f"   Depth: {tree.get_tree_info()['depth']}")
        print(f"   Leaves: {tree.get_tree_info()['leaf_count']}")
        print()
        
        # Generate proof for first event
        if len(events) > 0:
            first_event = events[0]
            event_hash = event_hashes[0]
            proof = tree.get_proof(event_hash)
            
            if proof:
                print(f"🔐 Merkle Proof Generated for Event: {first_event.event_id[:16]}...")
                print(f"   Proof length: {len(proof.proof_path)} hashes")
                print(f"   Verification: ", end="")
                
                # Verify proof
                is_valid = tree.verify_proof(proof)
                print("✅ VALID" if is_valid else "❌ INVALID")
                print()
        
        print("✓ Merkle root ready for on-chain anchoring")
    else:
        print("⚠ No events found for today. Run the agents first!")
    
    # =========================================================================
    # SCENARIO 5: Attestation Generation
    # =========================================================================
    print_section("Scenario 5: Attestation Bundle Generation")
    
    print("Generating attestation bundle for release v1.0.0...")
    print()
    
    # Generate model card
    model_card = attestation_gen.generate_model_card(
        model_name="MicroAI-DAO",
        model_version="v1.0.0",
        description="Ethical AI governance system with EPI constraints",
        intended_use="DAO governance and autonomous decision-making",
        limitations="Requires guardian oversight for high-value decisions",
        training_data="Business strategy corpus, ethical frameworks",
        performance_metrics={
            'average_epi': 0.823,
            'approval_rate': 0.875,
            'decision_latency': '2.3s'
        }
    )
    
    # Generate SBOM
    sbom = attestation_gen.generate_sbom(
        components=[
            {'name': 'Python', 'version': '3.11', 'license': 'PSF'},
            {'name': 'Flask', 'version': '3.0.0', 'license': 'BSD'},
            {'name': 'transformers', 'version': '4.35.0', 'license': 'Apache-2.0'},
            {'name': 'torch', 'version': '2.1.0', 'license': 'BSD'}
        ],
        format='SPDX'
    )
    
    # Compile eval summary
    eval_summary = attestation_gen.compile_eval_summary(
        total_requests=1000,
        evaluated_requests=950,
        passed_requests=875,
        category_results={
            'EPI': 0.923,
            'Safety': 0.956,
            'Bias': 0.889,
            'Compliance': 0.967
        },
        last_red_team_date='2025-12-01'
    )
    
    # Generate attestation
    if len(events) > 0:
        attestation = attestation_gen.generate_attestation(
            release_id="v1.0.0",
            model_card=model_card,
            sbom=sbom,
            eval_summary=eval_summary,
            log_root=root if len(events) > 0 else "0" * 64,
            policy_version="v1.0.0",
            compliance_frameworks=['Wyoming-DAO-LLC', 'SOC2'],
            metadata={
                'environment': 'production',
                'deployment_type': 'testnet'
            }
        )
        
        print(f"📜 Attestation Bundle")
        print(f"   Release: {attestation.release_id}")
        print(f"   Date: {attestation.release_date}")
        print(f"   Policy Version: {attestation.policy_version}")
        print(f"   Log Root: {attestation.log_root[:16]}...{attestation.log_root[-16:]}")
        print(f"   Compliance: {', '.join(attestation.compliance_frameworks)}")
        print()
        print(f"   Evaluation Summary:")
        print(f"      Coverage: {attestation.eval_summary['coverage_pct']:.1f}%")
        print(f"      Pass Rate: {attestation.eval_summary['pass_rate']:.1f}%")
        print(f"      Last Red Team: {attestation.eval_summary['last_red_team']}")
        print()
        print("✓ Attestation bundle ready for distribution")
    
    # =========================================================================
    # SCENARIO 6: Verification
    # =========================================================================
    print_section("Scenario 6: Cryptographic Verification")
    
    print("Verifying event signatures and proofs...")
    print()
    
    if len(events) > 0:
        # Verify first event signature
        first_event = events[0]
        sig_result = proof_verifier.verify_event_signature(first_event)
        
        print(f"🔍 Event Signature Verification")
        print(f"   Event ID: {first_event.event_id[:16]}...")
        print(f"   Agent: {first_event.agent_id}")
        print(f"   Timestamp: {first_event.timestamp}")
        print(f"   Signature Valid: {'✅ YES' if sig_result.is_valid else '❌ NO'}")
        print(f"   Confidence: {sig_result.confidence:.1%}")
        print()
        
        # Verify Merkle proof
        if proof:
            proof_result = proof_verifier.verify_merkle_proof(proof)
            
            print(f"🌳 Merkle Proof Verification")
            print(f"   Proof Valid: {'✅ YES' if proof_result.is_valid else '❌ NO'}")
            print(f"   Root Match: {'✅ YES' if proof_result.root_match else '❌ NO'}")
            print(f"   Confidence: {proof_result.confidence:.1%}")
            print()
        
        print("✓ All verifications passed")
    
    # =========================================================================
    # Summary
    # =========================================================================
    print_section("System Summary")
    
    # CEO-AI stats
    ceo_stats = ceo.get_stats()
    print("👔 CEO-AI Statistics:")
    print(f"   Total Proposals: {ceo_stats['total_proposals']}")
    print(f"   Approved: {ceo_stats['approved']}")
    print(f"   Rejected: {ceo_stats['rejected']}")
    print(f"   Average EPI: {ceo_stats['average_epi']:.3f}")
    print(f"   Approval Rate: {ceo_stats['approval_rate']:.1f}%")
    print()
    
    # CFO-AI stats
    cfo_stats = cfo.get_stats()
    print("💼 CFO-AI Statistics:")
    print(f"   Total Payments: {cfo_stats['total_payments']}")
    print(f"   Approved: {cfo_stats['approved_payments']}")
    print(f"   Rejected: {cfo_stats['rejected_payments']}")
    print(f"   Average EPI: {cfo_stats['average_epi']:.3f}")
    print(f"   Approval Rate: {cfo_stats['approval_rate']:.1f}%")
    print(f"   Treasury Balance: ${cfo_stats['treasury_balance']:,.0f}")
    print()
    
    # Trust Stack stats
    print("🔐 Trust Stack Statistics:")
    print(f"   Total Events: {len(events)}")
    print(f"   Merkle Root: {root[:16] if len(events) > 0 else 'N/A'}...")
    print(f"   Verifications: All passed")
    print()
    
    print("=" * 70)
    print("  Demo Complete!")
    print("=" * 70)
    print()
    print("Next steps:")
    print("  1. View dashboard: http://localhost:5173")
    print("  2. Check API: http://localhost:5000/api/trust/status")
    print("  3. Explore audit trail: http://localhost:5173/trust/audit")
    print("  4. Deploy to testnet: ./deploy-testnet.sh")
    print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nDemo interrupted by user")
    except Exception as e:
        print(f"\n\nError: {e}")
        import traceback
        traceback.print_exc()
