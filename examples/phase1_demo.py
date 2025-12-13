"""
Phase 1 Integration Demo
========================

Demonstrates the new enterprise features:
1. Risk-Tiered Classification
2. Model Registry
3. Database Schema

Shows how these integrate with existing EPI and Trust Stack systems.
"""

import sys
sys.path.insert(0, '/home/ubuntu/microai-dao-core')

from src.policy_engine.risk_classifier import RiskClassifier, RiskTier
from src.ai_c_suite.model_registry import ModelRegistry, ModelType, ModelStatus
from src.epi.calculator import EPICalculator, EPIScores
from datetime import datetime


def print_section(title):
    """Print a formatted section header."""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70 + "\n")


def demo_risk_classification():
    """Demonstrate risk classification system."""
    print_section("1. RISK-TIERED CLASSIFICATION")
    
    classifier = RiskClassifier()
    
    # Example 1: Low risk - content recommendation
    print("Example 1: Content Recommendation System")
    print("-" * 70)
    
    assessment1 = classifier.assess_risk(
        model_name="ContentRecommender-v1",
        model_type="recommendation",
        use_case="Recommend articles to users based on reading history",
        impact_scope="individual",
        decision_autonomy="automated",
        data_sensitivity="public",
        reversibility="reversible",
        regulatory_requirements="none"
    )
    
    print(f"Model: {assessment1.tier.name} Risk (Tier {assessment1.tier.value})")
    print(f"Risk Score: {assessment1.score:.3f}")
    print(f"\n{assessment1.reasoning}")
    print(f"\nApproval Requirements:")
    for key, value in assessment1.approval_requirements.items():
        print(f"  - {key}: {value}")
    print(f"\nRecommendations:")
    for rec in assessment1.recommendations:
        print(f"  - {rec}")
    
    # Example 2: High risk - credit scoring
    print("\n" + "-" * 70)
    print("Example 2: Credit Scoring System")
    print("-" * 70)
    
    assessment2 = classifier.assess_risk(
        model_name="CreditScorer-v2",
        model_type="classification",
        use_case="Determine creditworthiness for loan applications",
        impact_scope="individual",
        decision_autonomy="automated",
        data_sensitivity="protected",
        reversibility="difficult",
        regulatory_requirements="high"
    )
    
    print(f"Model: {assessment2.tier.name} Risk (Tier {assessment2.tier.value})")
    print(f"Risk Score: {assessment2.score:.3f}")
    print(f"\n{assessment2.reasoning}")
    print(f"\nApproval Requirements:")
    for key, value in assessment2.approval_requirements.items():
        print(f"  - {key}: {value}")
    
    # Example 3: Critical risk - autonomous vehicle
    print("\n" + "-" * 70)
    print("Example 3: Autonomous Vehicle Control")
    print("-" * 70)
    
    assessment3 = classifier.assess_risk(
        model_name="AutoDrive-v1",
        model_type="reinforcement",
        use_case="Control autonomous vehicle navigation and decision-making",
        impact_scope="society",
        decision_autonomy="fully_autonomous",
        data_sensitivity="private",
        reversibility="permanent",
        regulatory_requirements="critical"
    )
    
    print(f"Model: {assessment3.tier.name} Risk (Tier {assessment3.tier.value})")
    print(f"Risk Score: {assessment3.score:.3f}")
    print(f"\n{assessment3.reasoning}")
    print(f"\nApproval Requirements:")
    for key, value in assessment3.approval_requirements.items():
        print(f"  - {key}: {value}")
    
    return classifier, [assessment1, assessment2, assessment3]


def demo_model_registry():
    """Demonstrate model registry system."""
    print_section("2. MODEL REGISTRY")
    
    registry = ModelRegistry(db_path="phase1_demo_registry.db")
    
    # Register CEO-AI
    print("Registering CEO-AI...")
    ceo_model = registry.register_model(
        name="CEO-AI",
        model_type=ModelType.AGENT,
        description="Strategic planning and proposal generation agent with EPI validation",
        use_case="Generate strategic proposals, conduct market analysis, review performance",
        owner="MicroAI-DAO",
        initial_version="1.0.0",
        tags=["agent", "strategic", "governance", "epi"],
        risk_tier=2,
        metadata={
            "base_model": "microsoft/Phi-3-mini-4k-instruct",
            "epi_threshold": 0.7,
            "trust_stack_enabled": True
        }
    )
    
    print(f"✅ Registered: {ceo_model.name}")
    print(f"   Model ID: {ceo_model.model_id}")
    print(f"   Type: {ceo_model.model_type.value}")
    print(f"   Risk Tier: {ceo_model.risk_tier}")
    print(f"   Version: {ceo_model.current_version}")
    
    # Register CFO-AI
    print("\nRegistering CFO-AI...")
    cfo_model = registry.register_model(
        name="CFO-AI",
        model_type=ModelType.AGENT,
        description="Financial decision-making agent with EPI constraints",
        use_case="Process payments, allocate budgets, manage treasury operations",
        owner="MicroAI-DAO",
        initial_version="1.0.0",
        tags=["agent", "financial", "governance", "epi"],
        risk_tier=3,
        metadata={
            "base_model": "microsoft/Phi-3-mini-4k-instruct",
            "epi_threshold": 0.7,
            "trust_stack_enabled": True
        }
    )
    
    print(f"✅ Registered: {cfo_model.name}")
    print(f"   Model ID: {cfo_model.model_id}")
    print(f"   Type: {cfo_model.model_type.value}")
    print(f"   Risk Tier: {cfo_model.risk_tier}")
    print(f"   Version: {cfo_model.current_version}")
    
    # Add a new version to CEO-AI
    print("\nAdding new version to CEO-AI...")
    new_version = registry.add_version(
        model_id=ceo_model.model_id,
        version="1.1.0",
        model_hash="abc123def456",
        created_by="MicroAI-DAO",
        changes="Improved proposal generation with better context understanding",
        performance_metrics={
            "epi_compliance_rate": 0.95,
            "proposal_acceptance_rate": 0.82,
            "avg_epi_score": 0.85
        },
        epi_score=0.85
    )
    
    print(f"✅ Added version: {new_version.version}")
    print(f"   EPI Score: {new_version.epi_score:.3f}")
    print(f"   Performance Metrics:")
    for metric, value in new_version.performance_metrics.items():
        print(f"     - {metric}: {value:.3f}")
    
    # Update status
    print("\nUpdating CEO-AI status to DEPLOYED...")
    registry.update_status(ceo_model.model_id, ModelStatus.DEPLOYED, version="1.1.0")
    print("✅ Status updated")
    
    # Get registry stats
    print("\n" + "-" * 70)
    print("Registry Statistics")
    print("-" * 70)
    
    stats = registry.get_model_stats()
    print(f"Total Models: {stats['total_models']}")
    print(f"\nBy Type:")
    for model_type, count in stats['by_type'].items():
        print(f"  - {model_type}: {count}")
    print(f"\nBy Risk Tier:")
    for tier, count in stats['by_risk_tier'].items():
        print(f"  - Tier {tier}: {count}")
    
    return registry, [ceo_model, cfo_model]


def demo_integration():
    """Demonstrate integration of all Phase 1 features."""
    print_section("3. INTEGRATED WORKFLOW")
    
    print("Scenario: Deploying a new AI model with full governance")
    print("-" * 70)
    
    # Step 1: Risk Assessment
    print("\nStep 1: Risk Assessment")
    classifier = RiskClassifier()
    
    assessment = classifier.assess_risk(
        model_name="CustomerServiceBot-v1",
        model_type="generation",
        use_case="Automated customer service responses with sentiment analysis",
        impact_scope="group",
        decision_autonomy="human_oversight",
        data_sensitivity="private",
        reversibility="reversible",
        regulatory_requirements="moderate"
    )
    
    print(f"✅ Risk Assessment Complete")
    print(f"   Tier: {assessment.tier.name} (Tier {assessment.tier.value})")
    print(f"   Risk Score: {assessment.score:.3f}")
    print(f"   Requires Voting: {assessment.approval_requirements['voting_required']}")
    print(f"   Quorum Required: {assessment.approval_requirements['quorum']:.0%}")
    
    # Step 2: Register Model
    print("\nStep 2: Model Registration")
    registry = ModelRegistry(db_path="phase1_demo_registry.db")
    
    model = registry.register_model(
        name="CustomerServiceBot",
        model_type=ModelType.GENERATION,
        description="AI-powered customer service chatbot",
        use_case=assessment.reasoning.split('\n')[0],
        owner="Customer-Success-Team",
        initial_version="1.0.0",
        tags=["chatbot", "customer-service", "generation"],
        risk_tier=assessment.tier.value,
        metadata={
            "risk_assessment": {
                "score": assessment.score,
                "tier": assessment.tier.name,
                "factors": assessment.factors
            }
        }
    )
    
    print(f"✅ Model Registered")
    print(f"   Model ID: {model.model_id}")
    print(f"   Risk Tier: {model.risk_tier}")
    
    # Step 3: EPI Validation
    print("\nStep 3: EPI Validation")
    epi_calc = EPICalculator()
    
    # Simulate model performance
    scores = EPIScores(
        profit=0.75,  # Customer satisfaction improvement
        ethics=0.85,  # Respects privacy, fair treatment
        violations=[]  # No violations
    )
    
    epi, epi_valid, epi_trace = epi_calc.compute_epi(scores)
    
    print(f"✅ EPI Calculated")
    print(f"   EPI Score: {epi:.3f}")
    print(f"   Valid (>0.7): {epi_valid}")
    print(f"   Components:")
    print(f"     - Harmonic Mean: {epi_trace['hmean']:.3f}")
    print(f"     - Balance Penalty: {epi_trace['balance_penalty']:.3f}")
    print(f"     - Trust: {epi_trace['trust']:.3f}")
    
    # Step 4: Approval Decision
    print("\nStep 4: Approval Decision")
    
    if epi_valid and assessment.tier.value <= 2:
        print("✅ AUTO-APPROVED")
        print("   Reason: EPI valid and Low/Medium risk tier")
        registry.update_status(model.model_id, ModelStatus.APPROVED)
    elif epi_valid:
        print("⏳ PENDING GOVERNANCE VOTE")
        print(f"   Reason: High risk tier ({assessment.tier.name})")
        print(f"   Requirements:")
        print(f"     - Quorum: {assessment.approval_requirements['quorum']:.0%}")
        print(f"     - Majority: {assessment.approval_requirements['majority']:.0%}")
        print(f"     - Technical Review: {assessment.approval_requirements['technical_review']}")
        print(f"     - Ethics Review: {assessment.approval_requirements['ethics_review']}")
    else:
        print("❌ REJECTED")
        print(f"   Reason: EPI score {epi:.3f} below threshold 0.7")
    
    # Step 5: Record Performance
    print("\nStep 5: Performance Tracking")
    
    registry.record_performance(
        model_id=model.model_id,
        version="1.0.0",
        metrics={
            "epi_score": epi,
            "customer_satisfaction": 0.88,
            "response_accuracy": 0.92,
            "avg_response_time": 2.3
        }
    )
    
    print("✅ Performance Metrics Recorded")
    print("   Metrics:")
    print(f"     - EPI Score: {epi:.3f}")
    print(f"     - Customer Satisfaction: 0.88")
    print(f"     - Response Accuracy: 0.92")
    print(f"     - Avg Response Time: 2.3s")
    
    return model, assessment, epi


def main():
    """Run the Phase 1 integration demo."""
    print("\n" + "=" * 70)
    print("  PHASE 1 INTEGRATION DEMONSTRATION")
    print("  Risk Classification + Model Registry + Database Schema")
    print("=" * 70)
    
    try:
        # Demo 1: Risk Classification
        classifier, assessments = demo_risk_classification()
        
        # Demo 2: Model Registry
        registry, models = demo_model_registry()
        
        # Demo 3: Integrated Workflow
        model, assessment, epi = demo_integration()
        
        # Summary
        print_section("SUMMARY")
        
        print("Phase 1 Features Demonstrated:")
        print("  ✅ Risk-Tiered Classification (4 tiers)")
        print("  ✅ Model Registry (versioning, metadata, tracking)")
        print("  ✅ Database Schema (enterprise-ready)")
        print("  ✅ EPI Integration (ethical constraints)")
        print("  ✅ Approval Workflows (risk-based)")
        print()
        
        print("Key Benefits:")
        print("  • Automated risk assessment for all AI models")
        print("  • Centralized model tracking and versioning")
        print("  • Risk-based approval requirements")
        print("  • EPI validation for ethical compliance")
        print("  • Complete audit trail in database")
        print()
        
        print("Next Steps:")
        print("  1. Deploy to testnet for validation")
        print("  2. Implement Phase 2 (voting mechanisms)")
        print("  3. Add compliance automation (Phase 3)")
        print("  4. Build enterprise dashboard")
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
