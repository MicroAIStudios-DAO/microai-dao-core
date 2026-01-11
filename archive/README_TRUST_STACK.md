# MicroAI DAO - Trust Stack Integration

## 🎯 What's New

The **ExecAI Trust Stack** has been fully integrated into MicroAI DAO, creating the world's first **verifiable ethical AI governance system** with cryptographic proof.

### Key Features

✅ **Cryptographic Event Logging** - Every AI decision is signed and tamper-evident  
✅ **Merkle Tree Verification** - Efficient proof generation for any decision  
✅ **EPI Validation** - All decisions constrained by Ethical Profitability Index  
✅ **AI Agents with LLMs** - CEO-AI and CFO-AI using Hugging Face models  
✅ **Trust Dashboard** - Real-time monitoring and verification  
✅ **One-Command Deployment** - Deploy to testnet or production instantly  
✅ **Attestation Bundles** - Machine-verifiable compliance evidence  

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Deploy to Testnet

```bash
./deploy-testnet.sh
```

This single command:
- Sets up Python environment
- Initializes Trust Stack database
- Deploys smart contracts to Sepolia & Devnet
- Starts Flask API (port 5000)
- Launches React dashboard (port 5173)
- Initializes AI agents

### 3. Access the System

- **Dashboard**: http://localhost:5173
- **API**: http://localhost:5000
- **Trust Status**: http://localhost:5000/api/trust/status
- **Health Check**: http://localhost:5000/api/health

### 4. Run the Demo

```bash
python examples/full_stack_demo.py
```

This demonstrates:
- CEO-AI making strategic proposals
- CFO-AI approving payments
- EPI validation
- Trust Stack logging
- Merkle proof generation
- Cryptographic verification

## 📊 Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  MicroAI DAO Core                        │
│                                                          │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐             │
│  │  CEO-AI  │  │  CFO-AI  │  │  EXECAI  │             │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘             │
│       │             │              │                     │
│       └─────────────┼──────────────┘                     │
│                     ▼                                    │
│          ┌──────────────────────┐                       │
│          │  Policy Validator     │                       │
│          │  (EPI + Compliance)   │                       │
│          └──────────┬────────────┘                       │
│                     │                                    │
│                     ▼                                    │
│          ┌──────────────────────┐                       │
│          │  ExecAI Trust Stack   │                       │
│          │  • Event Logger       │                       │
│          │  • Merkle Trees       │                       │
│          │  • Attestations       │                       │
│          │  • Verification       │                       │
│          └──────────┬────────────┘                       │
│                     │                                    │
│                     ▼                                    │
│          ┌──────────────────────┐                       │
│          │  Database (SQLite)    │                       │
│          └───────────────────────┘                       │
└──────────────────────────────────────────────────────────┘
                     │
                     ▼
        ┌────────────────────────┐
        │  Blockchain Anchoring   │
        │  • Ethereum (Sepolia)   │
        │  • Solana (Devnet)      │
        └────────────────────────┘
```

## 🤖 AI Agents

### CEO-AI
Strategic decision-making agent with EPI constraints.

**Capabilities:**
- Strategic planning and vision setting
- Proposal generation with EPI validation
- Market analysis and opportunity assessment
- Risk evaluation and mitigation
- Thought logging with cryptographic verification

**Example:**
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

### CFO-AI
Financial decision-making agent with budget optimization.

**Capabilities:**
- Payment approval workflow
- Budget allocation with EPI validation
- Treasury management
- Financial forecasting
- Compliance checking

**Example:**
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
```

## 🔐 Trust Stack Features

### Event Logging
Every AI decision is automatically logged with:
- Cryptographic signature (HMAC-SHA256)
- Input/output hashes
- EPI score
- Policy evaluations
- Tool calls
- Timestamp

### Merkle Tree Verification
Daily Merkle trees enable:
- Efficient proof generation (O(log n))
- Tamper-evident history
- On-chain anchoring
- Public verifiability

### Attestation Bundles
Machine-verifiable compliance evidence including:
- Model cards
- SBOMs (Software Bill of Materials)
- Evaluation summaries
- Merkle roots
- Multi-signatures

### Trust Badge Levels

| Badge | Requirements |
|-------|-------------|
| **Bronze** | 100+ events, EPI ≥ 0.6, Basic logging |
| **Silver** | 1,000+ events, EPI ≥ 0.7, Daily anchoring |
| **Gold** | 10,000+ events, EPI ≥ 0.8, External audit, SOC2 |

## 📱 Dashboard

The React dashboard provides:

### Trust Panel
- Real-time trust status
- Trust badge level
- Live EPI metrics
- Agent activity monitoring
- Merkle root status

### EPI Metrics
- Overall EPI score with visualization
- Component breakdown (profit, ethics, balance, trust)
- Golden ratio analysis
- Optimization suggestions

### Audit Browser
- Event log explorer
- Filter by agent, date, action
- View event details
- Verify cryptographic proofs
- Export audit trails

### Agent Monitoring
- CEO-AI, CFO-AI, EXECAI statistics
- Decision history
- Approval rates
- Recent activity timeline

## 🌐 API Endpoints

### Trust Stack

```
POST   /api/trust/log                    - Log a trust event
GET    /api/trust/event/<id>             - Retrieve event by ID
GET    /api/trust/events/agent/<id>      - Get agent events
GET    /api/trust/events/date/<date>     - Get events by date
GET    /api/trust/prove/<id>             - Generate Merkle proof
POST   /api/trust/verify/event           - Verify event signature
POST   /api/trust/verify/proof           - Verify Merkle proof
POST   /api/trust/anchor/daily/<date>    - Anchor daily root
POST   /api/trust/attestation/generate   - Generate attestation
GET    /api/trust/status                 - Get trust system status
```

### EPI Calculation

```
POST   /api/epi/calculate                - Calculate EPI score
POST   /api/epi/optimize                 - Find optimal parameters
```

### AI Agents

```
GET    /api/personas/strategic-catalyst/profile
POST   /api/personas/strategic-catalyst/respond
GET    /api/personas/execai/profile
POST   /api/personas/execai/evaluate
GET    /api/personas/execai/stats
```

## 🚢 Deployment

### Testnet (Development)

```bash
./deploy-testnet.sh
```

Deploys to:
- Ethereum Sepolia
- Solana Devnet
- Local SQLite database
- Development servers

### Production (Mainnet)

```bash
./deploy-production.sh
```

Deploys to:
- Ethereum Mainnet
- Solana Mainnet
- PostgreSQL database
- Nginx with SSL/TLS
- Systemd services
- Monitoring

**Requirements:**
- PostgreSQL database
- Domain with DNS
- SSL certificates (Let's Encrypt)
- Ethereum private key with ETH
- Solana keypair with SOL

## 📚 Documentation

- **Trust Stack Integration**: [docs/TRUST_STACK_INTEGRATION.md](docs/TRUST_STACK_INTEGRATION.md)
- **EPI Derivation**: [docs/EPI_derivation.md](docs/EPI_derivation.md)
- **Synthetic Trust**: [docs/synthetic_trust.md](docs/synthetic_trust.md)
- **API Reference**: http://localhost:5000/api/info

## 🧪 Testing

Run the full stack demo:

```bash
python examples/full_stack_demo.py
```

Test individual components:

```bash
# Test EPI calculator
python -m pytest src/epi/tests/

# Test Trust Stack
python -m pytest src/trust_stack/tests/

# Test API
curl http://localhost:5000/api/health
curl http://localhost:5000/api/trust/status
```

## 🔒 Security

### Cryptographic Guarantees
- **SHA-256**: Collision-resistant hashing
- **HMAC**: Tamper-evident signatures
- **Merkle Trees**: Efficient verification
- **On-chain Anchoring**: Immutable timestamps

### Privacy Protection
- **PII Redaction**: Automatic removal
- **Hash-based Verification**: No data exposure
- **Selective Disclosure**: Prove without revealing

## 🛣️ Roadmap

### Phase 1 (Current) ✅
- Event logging with signatures
- Merkle tree generation
- Basic attestations
- Dashboard visualization
- AI agents with LLMs

### Phase 2 (Q1 2026)
- On-chain anchoring automation
- Multi-signature attestations
- External audit integration
- Public verification portal

### Phase 3 (Q2 2026)
- Zero-knowledge proofs
- Decentralized storage (IPFS)
- Cross-chain verification
- Automated compliance reporting

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📄 License

MIT License - See [LICENSE](LICENSE) for details.

## 🆘 Support

- **GitHub**: https://github.com/MicroAIStudios-DAO/microai-dao-core
- **Issues**: https://github.com/MicroAIStudios-DAO/microai-dao-core/issues
- **Docs**: https://docs.microai.dao

---

**Built with ethical AI governance in mind** 🤖⚖️
