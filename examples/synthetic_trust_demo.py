"""
Synthetic Trust Demo
===================

Demonstrates the synthetic trust framework components:
- Trust metrics calculation
- Decision verification
- Guardian oversight
- Anomaly detection

This example shows how to build stakeholder confidence through
transparent, verifiable AI governance.
"""

import sys
sys.path.insert(0, '/home/ubuntu/microai-dao-core')

from src.trust_stack import (
    EventLogger,
    TrustMetricsCalculator,
    DecisionVerifier,
    Decision,
    GuardianSystem,
    GuardianRole
)
from src.personas.ceo_ai import CEOAI
from src.personas.cfo_ai import CFOAI
from datetime import datetime
import hashlib
import hmac


def print_section(title):
    """Print a formatted section header."""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70 + "\n")


def demo_trust_metrics():
    """Demonstrate trust metrics calculation."""
    print_section("1. TRUST METRICS CALCULATION")
    
    # Initialize components
    logger = EventLogger()
    calculator = TrustMetricsCalculator(logger)
    
    # Simulate some AI decisions
    print("Simulating AI decisions...")
    ceo = CEOAI()
    
    decisions = [
        ("strategic_proposal", "Expand into healthcare AI market", 0.85, 0.80),
        ("strategic_proposal", "Partner with ethical AI consortium", 0.75, 0.90),
        ("strategic_proposal", "Launch transparency initiative", 0.70, 0.95),
        ("performance_review", "Q4 performance exceeded targets", 0.88, 0.82),
        ("market_analysis", "Healthcare AI market growing 25% YoY", 0.80, 0.75),
    ]
    
    for action_type, description, profit, ethics in decisions:
        result = ceo.generate_proposal(description)
        print(f"  ✓ {action_type}: EPI = {result['epi_score']:.3f}")
    
    print()
    
    # Calculate metrics
    print("Calculating trust metrics...")
    metrics = calculator.calculate_metrics()
    
    print(f"\nQuantitative Metrics:")
    print(f"  EPI Compliance Rate: {metrics.epi_compliance_rate:.1%} (target: >95%)")
    print(f"  Thought Log Completeness: {metrics.thought_log_completeness:.1%} (target: 100%)")
    print(f"  Guardian Veto Rate: {metrics.guardian_veto_rate:.1%} (target: <5%)")
    print(f"  Incident Response Time: {metrics.incident_response_time:.1f}h (target: <24h)")
    print(f"  Stakeholder Satisfaction: {metrics.stakeholder_satisfaction:.1%} (target: >80%)")
    print(f"\n  Overall Trust Score: {metrics.get_overall_score():.3f}")
    
    # Calculate qualitative indicators
    qualitative = calculator.calculate_qualitative_indicators(metrics)
    
    print(f"\nQualitative Indicators:")
    print(f"  Transparency: {qualitative.transparency:.1%}")
    print(f"  Predictability: {qualitative.predictability:.1%}")
    print(f"  Accountability: {qualitative.accountability:.1%}")
    print(f"  Fairness: {qualitative.fairness:.1%}")
    print(f"  Resilience: {qualitative.resilience:.1%}")
    print(f"\n  Average: {qualitative.get_average():.1%}")
    
    # Assess certification level
    level = calculator.assess_certification_level(metrics)
    print(f"\nCertification Level: {level.name}")
    
    return metrics, calculator


def demo_decision_verification():
    """Demonstrate cryptographic decision verification."""
    print_section("2. DECISION VERIFICATION")
    
    # Create a sample decision
    print("Creating AI decision...")
    
    decision_data = {
        'decision_id': 'dec_001',
        'agent_id': 'CEO-AI',
        'action_type': 'strategic_proposal',
        'timestamp': datetime.now().isoformat(),
        'profit_score': 0.85,
        'ethics_score': 0.80,
        'violations': [],
        'epi_score': 0.823,
        'reasoning': 'Healthcare AI investment aligns with ethical guidelines and provides strong ROI potential.',
        'signature': '',
        'reasoning_hash': ''
    }
    
    # Calculate reasoning hash
    decision_data['reasoning_hash'] = hashlib.sha256(
        decision_data['reasoning'].encode('utf-8')
    ).hexdigest()
    
    # Calculate signature
    verifier = DecisionVerifier()
    message = f"{decision_data['decision_id']}|{decision_data['agent_id']}|{decision_data['timestamp']}|{decision_data['epi_score']}"
    decision_data['signature'] = hmac.new(
        verifier.secret_key,
        message.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()
    
    decision = Decision(**decision_data)
    
    print(f"  Decision ID: {decision.decision_id}")
    print(f"  Agent: {decision.agent_id}")
    print(f"  Action: {decision.action_type}")
    print(f"  EPI Score: {decision.epi_score:.3f}")
    print()
    
    # Verify decision
    print("Verifying decision...")
    result = verifier.verify_decision(decision, decision.reasoning)
    
    print(f"\n  Overall: {'✅ VALID' if result.is_valid else '❌ INVALID'}")
    print(f"  Confidence: {result.confidence:.1%}")
    print(f"\n  Verification Checks:")
    print(f"    Signature: {'✅ PASS' if result.signature_valid else '❌ FAIL'}")
    print(f"    EPI Calculation: {'✅ PASS' if result.epi_valid else '❌ FAIL'}")
    print(f"    Reasoning Integrity: {'✅ PASS' if result.reasoning_valid else '❌ FAIL'}")
    
    print(f"\n  EPI Components:")
    print(f"    Claimed EPI: {decision.epi_score:.3f}")
    print(f"    Calculated EPI: {result.details['epi_check']['calculated_epi']:.3f}")
    print(f"    Threshold: {verifier.epi_threshold:.3f}")
    print(f"    Meets Threshold: {'Yes' if result.details['epi_check']['meets_threshold'] else 'No'}")
    
    # Generate full report
    print("\n" + "-" * 70)
    report = verifier.generate_verification_report(result, decision)
    print(report)
    
    return result


def demo_guardian_oversight():
    """Demonstrate guardian oversight system."""
    print_section("3. GUARDIAN OVERSIGHT")
    
    # Initialize guardian system
    system = GuardianSystem()
    
    print("Adding guardians...")
    
    # Add Class A guardian (full authority)
    guardian1 = system.add_guardian(
        guardian_id="guardian_001",
        name="Alice (Founder)",
        role=GuardianRole.CLASS_A,
        public_key="0x1234567890abcdef"
    )
    print(f"  ✓ {guardian1.name} - {guardian1.role.value}")
    
    # Add Class B guardian (limited authority)
    guardian2 = system.add_guardian(
        guardian_id="guardian_002",
        name="Bob (Advisor)",
        role=GuardianRole.CLASS_B,
        public_key="0xfedcba0987654321"
    )
    print(f"  ✓ {guardian2.name} - {guardian2.role.value}")
    
    # Add Observer
    guardian3 = system.add_guardian(
        guardian_id="guardian_003",
        name="Carol (Community Rep)",
        role=GuardianRole.OBSERVER,
        public_key="0xabcdef1234567890"
    )
    print(f"  ✓ {guardian3.name} - {guardian3.role.value}")
    
    print()
    
    # Demonstrate veto power
    print("Testing veto power...")
    
    veto_result = system.veto_proposal(
        guardian_id="guardian_001",
        proposal_id="prop_123",
        reason="EPI score of 0.65 is below threshold. Ethical concerns about data privacy.",
        signature="sig_abc123"
    )
    
    if veto_result['success']:
        print(f"  ✓ Veto successful")
        print(f"    Guardian: {veto_result['guardian']}")
        print(f"    Proposal: {veto_result['proposal_id']}")
        print(f"    Reason: {veto_result['reason']}")
    else:
        print(f"  ✗ Veto failed: {veto_result['error']}")
    
    print()
    
    # Test observer cannot veto
    print("Testing observer restrictions...")
    
    observer_veto = system.veto_proposal(
        guardian_id="guardian_003",
        proposal_id="prop_124",
        reason="I don't like this proposal",
        signature="sig_def456"
    )
    
    if not observer_veto['success']:
        print(f"  ✓ Observer correctly blocked from vetoing")
        print(f"    Error: {observer_veto['error']}")
    
    print()
    
    # Get system status
    print("System Status:")
    status = system.get_system_status()
    
    print(f"  Paused: {status['is_paused']}")
    print(f"  Total Guardians: {status['total_guardians']}")
    print(f"  Active Guardians: {status['active_guardians']}")
    print(f"  Class A Guardians: {status['class_a_guardians']}")
    print(f"  Total Vetoes: {status['total_vetoes']}")
    print(f"  Veto Rate: {status['veto_rate']:.1%}")
    
    print()
    
    # Get guardian stats
    print("Guardian Statistics:")
    for guardian_id in ['guardian_001', 'guardian_002', 'guardian_003']:
        stats = system.get_guardian_stats(guardian_id)
        if stats:
            print(f"\n  {stats['name']} ({stats['role']})")
            print(f"    Total Actions: {stats['total_actions']}")
            print(f"    Veto Count: {stats['veto_count']}")
            print(f"    Last Action: {stats['last_action_date']}")
    
    return system


def demo_anomaly_detection(calculator):
    """Demonstrate anomaly detection."""
    print_section("4. ANOMALY DETECTION")
    
    print("Analyzing decision patterns for anomalies...")
    
    # Get recent events
    logger = EventLogger()
    events = []
    
    # Simulate getting events (in production, would fetch from database)
    print("  Fetching recent events...")
    
    # Detect anomalies
    anomalies = calculator.detect_anomalies(events, lookback_days=7)
    
    if len(anomalies) == 0:
        print("\n  ✓ No anomalies detected")
        print("    System is operating normally")
    else:
        print(f"\n  ⚠ {len(anomalies)} anomalies detected:")
        for i, anomaly in enumerate(anomalies, 1):
            severity_icon = "🔴" if anomaly['severity'] == 'high' else "🟡"
            print(f"\n  {i}. {severity_icon} {anomaly['type'].upper()}")
            print(f"     Severity: {anomaly['severity']}")
            print(f"     Description: {anomaly['description']}")
            print(f"     Recommendation: {anomaly['recommendation']}")
    
    print()


def main():
    """Run the synthetic trust demonstration."""
    print("\n" + "=" * 70)
    print("  SYNTHETIC TRUST FRAMEWORK DEMONSTRATION")
    print("  Building Confidence in Autonomous AI Governance")
    print("=" * 70)
    
    try:
        # 1. Trust Metrics
        metrics, calculator = demo_trust_metrics()
        
        # 2. Decision Verification
        verification_result = demo_decision_verification()
        
        # 3. Guardian Oversight
        guardian_system = demo_guardian_oversight()
        
        # 4. Anomaly Detection
        demo_anomaly_detection(calculator)
        
        # Summary
        print_section("SUMMARY")
        
        print("Synthetic Trust Components Demonstrated:")
        print("  ✅ Trust Metrics Calculation")
        print("  ✅ Cryptographic Decision Verification")
        print("  ✅ Guardian Oversight System")
        print("  ✅ Anomaly Detection")
        print()
        
        print("Key Findings:")
        print(f"  Overall Trust Score: {metrics.get_overall_score():.3f}")
        print(f"  Decision Verification: {'✅ Valid' if verification_result.is_valid else '❌ Invalid'}")
        print(f"  Guardian Veto Rate: {metrics.guardian_veto_rate:.1%}")
        print(f"  System Status: {'⏸ Paused' if guardian_system.state.is_paused else '▶ Active'}")
        print()
        
        print("Next Steps:")
        print("  1. Deploy to testnet for real-world testing")
        print("  2. Schedule smart contract audit")
        print("  3. Conduct AI agent red team testing")
        print("  4. Launch public transparency portal")
        print("  5. Complete regulatory compliance review")
        print()
        
        print("=" * 70)
        print("  Demo completed successfully!")
        print("=" * 70 + "\n")
        
    except Exception as e:
        print(f"\n❌ Error during demo: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
