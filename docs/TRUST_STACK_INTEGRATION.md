# ExecAI Trust Stack Integration Guide

## Overview

The ExecAI Trust Stack has been fully integrated with the MicroAI DAO governance framework, creating a unified system for **verifiable ethical AI governance**. This document explains the integration architecture, components, and usage.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    MicroAI DAO Core                          │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   CEO-AI     │  │   CFO-AI     │  │   EXECAI     │     │
│  │   Agent      │  │   Agent      │  │   Voter      │     │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘     │
│         │                  │                  │              │
│         └──────────────────┼──────────────────┘              │
│                            ▼                                 │
│                  ┌───────────────────┐                      │
│                  │  Policy Validator  │                      │
│                  │  (EPI + Compliance)│                      │
│                  └─────────┬──────────┘                      │
│                            │                                 │
│                            ▼                                 │
│         ┌──────────────────────────────────┐                │
│         │      ExecAI Trust Stack          │                │
│         │                                  │                │
│         │  • Event Logger                  │                │
│         │  • Merkle Tree Builder           │                │
│         │  • Attestation Generator         │                │
│         │  • Proof Verifier                │                │
│         └──────────┬───────────────────────┘                │
│                    │                                         │
│                    ▼                                         │
│         ┌──────────────────────┐                            │
│         │   Database (SQLite)   │                            │
│         │   • Events            │                            │
│         │   • Merkle Roots      │                            │
│         │   • Attestations      │                            │
│         └───────────────────────┘                            │
└──────────────────────────────────────────────────────────────┘
                            │
                            ▼
              ┌─────────────────────────┐
              │   Blockchain Anchoring   │
              │   • Ethereum (Sepolia)   │
              │   • Solana (Devnet)      │
              └─────────────────────────┘
```

## Components

### 1. Trust Stack Backend (`src/trust_stack/`)

#### Event Logger (`event_logger.py`)
- Logs every AI decision with cryptographic signature
- Generates SHA-256 hashes of inputs/outputs
- Creates HMAC signatures for tamper-evidence
- Stores events in database with full audit trail

**Key Features:**
- Automatic redaction of PII
- Policy evaluation tracking
- Tool call logging
- EPI score recording

#### Merkle Tree (`merkle_tree.py`)
- Builds Merkle trees from daily event hashes
- Generates cryptographic proofs for individual events
- Enables efficient verification without revealing all events

#### Attestation Generator (`attestation.py`)
- Creates machine-verifiable attestation bundles
- Includes model cards, SBOMs, evaluation summaries
- Generates multi-signature attestations
- Supports compliance frameworks (SOC2, ISO27001, HIPAA)

#### Proof Verifier (`verifier.py`)
- Verifies event signatures
- Validates Merkle proofs
- Checks on-chain anchors
- Provides verification reports

### 2. AI Agents with Trust Integration

#### CEO-AI (`src/personas/ceo_ai.py`)
- Strategic decision-making with Hugging Face LLMs
- EPI validation for all proposals
- Automatic trust logging
- Fallback reasoning when LLM unavailable

**Example Usage:**
```python
from personas.ceo_ai import CEOAI

ceo = CEOAI(use_local_model=False)

proposal = ceo.generate_proposal(
    title="Healthcare AI Investment",
    description="AI diagnostic tools for underserved communities",
    expected_profit=0.75,
    ethical_factors={
        'patient_outcomes': 0.9,
        'data_privacy': 0.85,
        'accessibility': 0.95
    },
    budget=500000,
    timeline="18 months"
)

print(f"EPI Score: {proposal.epi_score}")
print(f"Approved: {proposal.approved}")
```

#### CFO-AI (`src/personas/cfo_ai.py`)
- Financial decision-making with EPI constraints
- Payment approval workflow
- Budget allocation optimization
- Treasury management

**Example Usage:**
```python
from personas.cfo_ai import CFOAI

cfo = CFOAI(use_local_model=False)

payment = cfo.approve_payment(
    recipient="Healthcare AI Vendor",
    amount=50000,
    purpose="AI diagnostic system license",
    category="operational",
    ethical_factors={
        'patient_benefit': 0.9,
        'data_privacy': 0.85
    }
)

print(f"Approved: {payment.approved}")
print(f"EPI Score: {payment.epi_score}")
```

### 3. Flask API Integration (`api/app.py`)

New Trust Stack endpoints:

```
POST   /api/trust/log              - Log a trust event
GET    /api/trust/event/<id>       - Retrieve event by ID
GET    /api/trust/events/agent/<id> - Get agent events
GET    /api/trust/events/date/<date> - Get events by date
GET    /api/trust/prove/<id>       - Generate Merkle proof
POST   /api/trust/verify/event     - Verify event signature
POST   /api/trust/verify/proof     - Verify Merkle proof
POST   /api/trust/anchor/daily/<date> - Anchor daily root
POST   /api/trust/attestation/generate - Generate attestation
GET    /api/trust/status           - Get trust system status
```

### 4. React Dashboard (`microai-dashboard/`)

#### TrustPanel Component
- Real-time trust status display
- Trust badge level (Bronze/Silver/Gold)
- Live EPI metrics
- Agent activity monitoring
- Merkle root anchoring status

#### EPIMetrics Component
- Detailed EPI score breakdown
- Component visualization (profit, ethics, balance, trust)
- Optimization suggestions
- Golden ratio analysis

#### AuditBrowser Component
- Event log explorer
- Filter by agent, date, action type
- View event details
- Verify cryptographic proofs
- Export audit trails

#### TrustDashboard Page
- Unified trust monitoring interface
- Tabbed navigation (Overview, EPI, Audit, Agents)
- System health indicators
- Agent statistics
- Recent activity timeline

## Deployment

### Testnet Deployment (One Command)

```bash
./deploy-testnet.sh
```

This script:
1. Sets up Python environment
2. Initializes SQLite database
3. Deploys contracts to Sepolia (Ethereum) and Devnet (Solana)
4. Starts Flask API on port 5000
5. Builds and starts React dashboard on port 5173
6. Initializes AI agents

**Services:**
- API: http://localhost:5000
- Dashboard: http://localhost:5173
- Trust Status: http://localhost:5000/api/trust/status

### Production Deployment

```bash
./deploy-production.sh
```

This script:
1. Confirms production deployment (requires "YES")
2. Sets up production environment with PostgreSQL
3. Deploys contracts to Ethereum Mainnet and Solana Mainnet
4. Downloads and caches AI models
5. Builds optimized React dashboard
6. Configures Nginx with SSL/TLS
7. Sets up systemd services
8. Configures monitoring

**Requirements:**
- PostgreSQL database
- Domain name with DNS configured
- SSL certificates (Let's Encrypt)
- Ethereum private key with ETH for gas
- Solana keypair with SOL for deployment

## Trust Badge Levels

### Bronze Badge
- **Requirements:**
  - Basic event logging enabled
  - At least 100 logged events
  - EPI calculator operational
  - Average EPI score ≥ 0.6

### Silver Badge
- **Requirements:**
  - Daily Merkle root anchoring
  - On-chain verification available
  - At least 1,000 logged events
  - Average EPI score ≥ 0.7
  - Compliance framework implemented

### Gold Badge
- **Requirements:**
  - Multi-signature attestations
  - External audit completed
  - At least 10,000 logged events
  - Average EPI score ≥ 0.8
  - SOC2/ISO27001 compliance
  - Public transparency portal

## Verification Workflow

### 1. Event Logging
Every AI decision is automatically logged:

```python
event = event_logger.log_event(
    tenant_id="microai-dao",
    agent_id="CEO-AI",
    action_type="strategic_proposal",
    input_data="Healthcare AI Investment proposal",
    output_data="Approved with EPI 0.847",
    policy_version="v1.0.0",
    epi_score=0.847,
    evaluations=[...]
)
```

### 2. Daily Merkle Anchoring
At end of day, all event hashes are combined into Merkle tree:

```python
event_hashes = event_logger.get_daily_hashes("2025-12-12")
root = merkle_anchor.generate_daily_root("2025-12-12", event_hashes)
anchor_tx = merkle_anchor.prepare_anchor_transaction("2025-12-12", root)
```

### 3. Proof Generation
For any event, generate cryptographic proof:

```python
proof = proof_verifier.generate_proof(event_id)
# Returns: Merkle proof + on-chain anchor
```

### 4. Verification
Anyone can verify an event:

```python
result = proof_verifier.verify_event_signature(event)
# Returns: VerificationResult with validity status
```

## API Examples

### Log a Decision

```bash
curl -X POST http://localhost:5000/api/trust/log \
  -H "Content-Type: application/json" \
  -d '{
    "tenant_id": "microai-dao",
    "agent_id": "CEO-AI",
    "action_type": "proposal",
    "input_data": "Strategic proposal for healthcare AI",
    "output_data": "Approved with EPI 0.85",
    "policy_version": "v1.0.0",
    "epi_score": 0.85
  }'
```

### Get Trust Status

```bash
curl http://localhost:5000/api/trust/status
```

### Verify an Event

```bash
curl -X POST http://localhost:5000/api/trust/verify/event \
  -H "Content-Type: application/json" \
  -d '{
    "event": {
      "event_id": "...",
      "timestamp": "...",
      "signature": "..."
    }
  }'
```

## Security Considerations

### Cryptographic Guarantees
- **SHA-256 hashing**: Collision-resistant event fingerprinting
- **HMAC signatures**: Tamper-evident event logging
- **Merkle trees**: Efficient proof generation with logarithmic complexity
- **On-chain anchoring**: Immutable timestamp and verification

### Privacy Protection
- **PII redaction**: Automatic removal of sensitive data
- **Hash-based verification**: Verify without revealing content
- **Selective disclosure**: Prove properties without exposing data

### Compliance Support
- **Audit trails**: Complete decision history
- **Attestation bundles**: Machine-verifiable compliance evidence
- **Transparency**: Public verification without exposing secrets

## Future Enhancements

### Phase 1 (Current)
- ✅ Event logging with signatures
- ✅ Merkle tree generation
- ✅ Basic attestations
- ✅ Dashboard visualization

### Phase 2 (Q1 2026)
- [ ] On-chain anchoring automation
- [ ] Multi-signature attestations
- [ ] External audit integration
- [ ] Public verification portal

### Phase 3 (Q2 2026)
- [ ] Zero-knowledge proofs
- [ ] Decentralized storage (IPFS)
- [ ] Cross-chain verification
- [ ] Automated compliance reporting

## Support

For questions or issues:
- GitHub: https://github.com/MicroAIStudios-DAO/microai-dao-core
- Documentation: /docs
- API Reference: http://localhost:5000/api/info

## License

MIT License - See LICENSE file for details
