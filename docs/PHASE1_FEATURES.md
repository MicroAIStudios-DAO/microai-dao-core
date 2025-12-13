# Phase 1 Enterprise Features

## Overview

Phase 1 integrates enterprise-ready features from the MicroAI DAO Framework into the existing Trust Stack and EPI governance system. These features provide risk-based AI management, centralized model tracking, and comprehensive database infrastructure.

---

## Features

### 1. Risk-Tiered Classification

**Location:** `src/policy_engine/risk_classifier.py`

#### Description
Implements a 4-tier risk classification system for AI models based on multiple factors including impact scope, decision autonomy, data sensitivity, reversibility, and regulatory requirements.

#### Risk Tiers

| Tier | Name | Risk Score | Approval Requirements |
|------|------|------------|----------------------|
| 1 | LOW | 0.00-0.25 | Automated approval, periodic review |
| 2 | MEDIUM | 0.26-0.50 | Technical review + voting (30% quorum, 50% majority) |
| 3 | HIGH | 0.51-0.75 | Multi-stakeholder review + ethics committee (50% quorum, 66% majority) |
| 4 | CRITICAL | 0.76-1.00 | Full DAO vote + external audit (75% quorum, 80% majority) |

#### Usage Example

```python
from src.policy_engine.risk_classifier import RiskClassifier

classifier = RiskClassifier()

assessment = classifier.assess_risk(
    model_name="CreditScorer-v1",
    model_type="classification",
    use_case="Determine creditworthiness for loans",
    impact_scope="individual",
    decision_autonomy="automated",
    data_sensitivity="protected",
    reversibility="difficult",
    regulatory_requirements="high"
)

print(f"Risk Tier: {assessment.tier.name}")
print(f"Risk Score: {assessment.score:.3f}")
print(f"Approval Requirements: {assessment.approval_requirements}")
```

#### Risk Factors

**Impact Scope:**
- `individual` (0.2): Affects single users
- `group` (0.5): Affects groups or teams
- `organization` (0.7): Affects entire organizations
- `society` (1.0): Affects society at large

**Decision Autonomy:**
- `human_in_loop` (0.2): Human makes final decision
- `human_oversight` (0.4): Human monitors AI decisions
- `automated` (0.7): Fully automated with human review option
- `fully_autonomous` (1.0): No human intervention

**Data Sensitivity:**
- `public` (0.1): Publicly available data
- `internal` (0.3): Internal organizational data
- `private` (0.6): Personal data
- `protected` (0.8): Protected health/financial data
- `highly_sensitive` (1.0): Highly sensitive regulated data

**Reversibility:**
- `reversible` (0.1): Easily reversed
- `difficult` (0.5): Difficult to reverse
- `very_difficult` (0.8): Very difficult to reverse
- `permanent` (1.0): Permanent consequences

**Regulatory Requirements:**
- `none` (0.0): No regulatory oversight
- `minimal` (0.2): Minimal requirements
- `moderate` (0.5): Moderate compliance needs
- `high` (0.8): High regulatory scrutiny
- `critical` (1.0): Critical regulated systems

---

### 2. Model Registry

**Location:** `src/ai_c_suite/model_registry.py`

#### Description
Centralized registry for tracking all AI models in the system. Provides model registration, versioning, performance tracking, and deployment management with complete audit trail.

#### Features
- Model registration with metadata
- Version control and tracking
- Performance metrics recording
- Deployment status management
- Risk tier assignment
- Integration with Trust Stack

#### Model Status Lifecycle

```
REGISTERED → TESTING → APPROVED → DEPLOYED → DEPRECATED → RETIRED
```

#### Usage Example

```python
from src.ai_c_suite.model_registry import ModelRegistry, ModelType, ModelStatus

registry = ModelRegistry()

# Register a new model
model = registry.register_model(
    name="CEO-AI",
    model_type=ModelType.AGENT,
    description="Strategic planning agent",
    use_case="Generate proposals with EPI validation",
    owner="MicroAI-DAO",
    initial_version="1.0.0",
    tags=["agent", "strategic", "governance"],
    risk_tier=2,
    metadata={"base_model": "microsoft/Phi-3-mini-4k-instruct"}
)

# Add a new version
new_version = registry.add_version(
    model_id=model.model_id,
    version="1.1.0",
    model_hash="abc123...",
    created_by="MicroAI-DAO",
    changes="Improved proposal generation",
    performance_metrics={"epi_compliance_rate": 0.95},
    epi_score=0.85
)

# Update status
registry.update_status(model.model_id, ModelStatus.DEPLOYED, version="1.1.0")

# Record performance
registry.record_performance(
    model_id=model.model_id,
    version="1.1.0",
    metrics={
        "epi_score": 0.85,
        "accuracy": 0.92,
        "latency_ms": 150
    }
)

# Get registry stats
stats = registry.get_model_stats()
print(f"Total models: {stats['total_models']}")
```

#### Model Types

- `CLASSIFICATION`: Classification models
- `REGRESSION`: Regression models
- `GENERATION`: Generative models (text, image, etc.)
- `RECOMMENDATION`: Recommendation systems
- `REINFORCEMENT`: Reinforcement learning agents
- `AGENT`: Autonomous AI agents
- `OTHER`: Other model types

---

### 3. Database Schema

**Location:** `database/schema.sql`

#### Description
Comprehensive enterprise database schema supporting multi-organization governance, stakeholder management, AI model tracking, proposals, voting, trust events, and compliance.

#### Core Tables

**Organizations**
- Multi-tenant support
- DAO address tracking
- Governance token management

**Stakeholders**
- Role-based classification (Technical, Business, Ethics, Legal)
- Voting power management
- Delegation support

**AI Models**
- Complete model lifecycle tracking
- Version history
- Risk tier assignment
- Performance metrics

**Proposals**
- Governance proposals
- Voting requirements
- Execution tracking

**Votes**
- Stakeholder votes
- Vote weight calculation
- Cryptographic signatures

**Trust Events**
- AI decision logging
- EPI score tracking
- Audit trail

**Merkle Anchors**
- Daily Merkle root anchoring
- On-chain verification
- Blockchain integration

**Attestations**
- Model attestations
- Compliance certificates
- Release bundles

**Guardian Actions**
- Veto tracking
- Emergency actions
- Oversight audit trail

**Compliance Checks**
- GDPR, SOC2, AI Act, HIPAA
- Automated compliance monitoring
- Violation tracking

#### Views

- `active_proposals`: Current active proposals with vote counts
- `model_deployment_status`: Model status with performance metrics
- `stakeholder_voting_summary`: Stakeholder voting history
- `trust_metrics_summary`: Daily trust metrics aggregation

#### Database Initialization

```bash
# Initialize database
python database/init_db.py

# This creates:
# - All tables and indexes
# - Views for common queries
# - Triggers for timestamp updates
# - Default organization
```

---

## Integration with Existing Systems

### EPI Integration

Risk classification works seamlessly with EPI validation:

```python
from src.policy_engine.risk_classifier import RiskClassifier
from src.epi.calculator import EPICalculator, EPIScores

# Assess risk
classifier = RiskClassifier()
assessment = classifier.assess_risk(...)

# Calculate EPI
epi_calc = EPICalculator()
scores = EPIScores(profit=0.85, ethics=0.80, violations=[])
epi, valid, trace = epi_calc.compute_epi(scores)

# Decision logic
if valid and assessment.tier.value <= 2:
    # Auto-approve for low/medium risk with valid EPI
    approve_deployment()
elif valid and assessment.tier.value >= 3:
    # Require governance vote for high/critical risk
    create_proposal()
else:
    # Reject if EPI invalid
    reject_deployment()
```

### Trust Stack Integration

Model registry integrates with Trust Stack event logging:

```python
from src.trust_stack import EventLogger
from src.ai_c_suite.model_registry import ModelRegistry

registry = ModelRegistry()
logger = EventLogger()

# Register model
model = registry.register_model(...)

# Log deployment event
event = logger.log_event(
    agent_id=model.name,
    action_type="model_deployment",
    input_data={"model_id": model.model_id, "version": model.current_version},
    output_data={"status": "deployed", "risk_tier": model.risk_tier},
    epi_score=model.metadata.get("epi_score")
)

# Record in registry
registry.update_status(model.model_id, ModelStatus.DEPLOYED)
```

### Guardian System Integration

Risk tiers determine guardian oversight requirements:

```python
from src.trust_stack import GuardianSystem
from src.policy_engine.risk_classifier import RiskClassifier

classifier = RiskClassifier()
guardian_system = GuardianSystem()

assessment = classifier.assess_risk(...)

if assessment.tier.value >= 3:
    # High/Critical risk requires guardian approval
    if assessment.approval_requirements['ethics_review']:
        # Notify ethics committee
        notify_ethics_committee(assessment)
    
    if assessment.approval_requirements['external_audit']:
        # Require external audit
        require_external_audit(assessment)
```

---

## API Endpoints (To Be Added)

### Risk Classification

```
POST /api/risk/assess
GET  /api/risk/tiers
GET  /api/risk/assessment/:id
```

### Model Registry

```
POST /api/models/register
GET  /api/models/list
GET  /api/models/:id
POST /api/models/:id/version
PUT  /api/models/:id/status
POST /api/models/:id/metrics
GET  /api/models/stats
```

### Database

```
GET  /api/db/organizations
GET  /api/db/stakeholders
GET  /api/db/proposals
GET  /api/db/votes
GET  /api/db/stats
```

---

## Testing

### Run Phase 1 Demo

```bash
# Run comprehensive demo
python examples/phase1_demo.py
```

This demonstrates:
1. Risk classification for 3 different AI models
2. Model registry with versioning
3. Integrated workflow: risk → register → EPI → approve

### Expected Output

```
======================================================================
  PHASE 1 INTEGRATION DEMONSTRATION
======================================================================

1. RISK-TIERED CLASSIFICATION
  Example 1: Content Recommendation
    Tier: LOW (Tier 1)
    Risk Score: 0.240
    Automated approval enabled

  Example 2: Credit Scoring
    Tier: HIGH (Tier 3)
    Risk Score: 0.680
    Multi-stakeholder review required

  Example 3: Autonomous Vehicle
    Tier: CRITICAL (Tier 4)
    Risk Score: 0.920
    Full DAO vote + external audit required

2. MODEL REGISTRY
  ✅ Registered: CEO-AI (model_id: abc123...)
  ✅ Registered: CFO-AI (model_id: def456...)
  ✅ Added version: 1.1.0
  
  Registry Statistics:
    Total Models: 2
    By Type: agent: 2
    By Risk Tier: 2: 1, 3: 1

3. INTEGRATED WORKFLOW
  Step 1: Risk Assessment ✅
  Step 2: Model Registration ✅
  Step 3: EPI Validation ✅
  Step 4: Approval Decision ✅
  Step 5: Performance Tracking ✅
```

---

## Benefits

### For AI Teams
- ✅ Automated risk assessment
- ✅ Centralized model tracking
- ✅ Clear approval workflows
- ✅ Version control and history
- ✅ Performance monitoring

### For Compliance Officers
- ✅ Risk-based oversight
- ✅ Complete audit trail
- ✅ Regulatory alignment
- ✅ Automated compliance checks
- ✅ Evidence collection

### For Executives
- ✅ Transparent governance
- ✅ Risk visibility
- ✅ Performance metrics
- ✅ Stakeholder accountability
- ✅ Regulatory readiness

---

## Next Steps

### Phase 2: Governance (2-3 days)
- Multi-stakeholder voting system
- Quadratic voting
- Delegation mechanisms
- GovernanceToken contract

### Phase 3: Compliance (2-3 days)
- Compliance automation engine
- Regulatory requirement database
- Automated reporting
- Alert system

### Phase 4: API & Dashboard (3-4 days)
- REST API endpoints
- GraphQL integration
- Enhanced dashboard
- Real-time monitoring

---

## Configuration

### Risk Classifier Configuration

Edit `src/policy_engine/risk_classifier.py` to customize:
- Risk factor weights
- Tier thresholds
- Approval requirements
- Recommendation templates

### Model Registry Configuration

Edit `src/ai_c_suite/model_registry.py` to customize:
- Database path
- Model types
- Status lifecycle
- Performance metrics

### Database Configuration

Edit `database/schema.sql` to customize:
- Table structures
- Indexes
- Views
- Triggers

---

## Troubleshooting

### Issue: Database not initialized
```bash
# Solution: Run initialization script
python database/init_db.py
```

### Issue: Module not found
```bash
# Solution: Set PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

### Issue: Risk assessment returning unexpected tier
```bash
# Solution: Check risk factor values
# Each factor should be between 0-1
# Overall score is weighted average
```

---

## References

- [Risk Classification Documentation](./risk_classification.md)
- [Model Registry API](./model_registry_api.md)
- [Database Schema Guide](./database_schema.md)
- [Integration Examples](../examples/phase1_demo.py)

---

**Last Updated:** December 12, 2025  
**Version:** 1.0.0  
**Status:** Production Ready
