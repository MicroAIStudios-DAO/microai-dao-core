# MicroAI DAO - Unified AI-Governed DAO Platform

> **A production-ready, AI-governed Decentralized Autonomous Organization with Wyoming LLC compliance, multi-chain support, and ethical profitability enforcement.**

[![Solana](https://img.shields.io/badge/Solana-Devnet-blue)](https://solana.com)
[![Ethereum](https://img.shields.io/badge/Ethereum-Sepolia-purple)](https://ethereum.org)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

## Overview

MicroAI DAO is a unified monorepo consolidating multiple repositories into a single, deployable system for AI-governed decentralized organizations. It features:

- **EXECAI**: AI stakeholder with 51% voting power
- **EPI Framework**: Ethical Profitability Index for balanced decision-making
- **Multi-Chain**: Solana (governance) + Ethereum (treasury/oracles)
- **Wyoming DAO LLC**: Legal compliance for US jurisdictions
- **Strategic Catalyst**: AI executive mentor for founders

## Repository Structure

```
microai-dao/
├── contracts/                 # Smart Contracts
│   ├── solana/               # Anchor programs (deployed)
│   │   ├── governance/       # Voting, proposals, DAO state
│   │   └── membership/       # Member registry, KYC fields
│   └── ethereum/             # Solidity contracts
│       ├── Governance.sol    # EPI-enforced governance
│       └── EPIOracle.sol     # On-chain EPI scores
│
├── src/                       # Core Python Modules
│   ├── epi/                  # EPI Calculator
│   │   ├── calculator.py     # Harmonic mean, golden ratio balance
│   │   └── trust_accumulator.py # Geometric trust decay
│   ├── policy_engine/        # Compliance validation
│   │   └── validator.py      # Sanctions, risk, EPI checks
│   ├── knowledge/            # Knowledge base
│   │   └── enhanced_kb.py    # TF-IDF semantic search
│   ├── personas/             # AI Agents
│   │   ├── strategic_catalyst.py  # Executive mentor
│   │   └── execai_voter.py   # Autonomous voting agent
│   └── compliance/           # Wyoming DAO LLC
│       └── wyoming_dao.py    # Legal compliance utilities
│
├── api/                       # Unified Flask Backend
│   └── app.py                # REST API endpoints
│
├── microai-dashboard/         # React Dashboard
│   └── src/                  # Governance UI, charts, compliance
│
├── services/
│   └── live-data-server/     # Solana account parser
│
├── automation/               # Revenue systems
├── docker/                   # Docker configs
├── scripts/                  # Deployment scripts
└── docs/                     # Documentation
```

## Quick Start

### Prerequisites

- Node.js 18+
- Python 3.11+
- Rust (for Solana development)
- Solana CLI
- Docker (optional)

### Installation

```bash
# Clone the repository
git clone https://github.com/Gnoscenti/microai-dao.git
cd microai-dao

# Install dependencies
make install

# Or manually:
pip install -r requirements.txt
cd microai-dashboard && npm install
```

### Running Services

```bash
# Start all services (recommended)
make dev-all

# Or individually:
make api         # Flask API (port 5000)
make live-data   # Solana data server (port 8787)
make dev         # React dashboard (port 5173)
```

### Docker Deployment

```bash
make docker-build
make docker-up

# View logs
make docker-logs

# Stop services
make docker-down
```

## Core Components

### 1. EPI Calculator

The Ethical Profitability Index ensures balanced decision-making:

```python
from src.epi import EPICalculator, EPIScores

calculator = EPICalculator(threshold=0.7)
scores = EPIScores(profit=0.8, ethics=0.75, violations=[])
result = calculator.compute_epi(scores)

print(f"EPI Score: {result.epi_score}")
print(f"Recommendation: {result.recommendation}")
```

**Formula**: `EPI = H(P, E) × B(P, E) × T(V)`
- H: Harmonic mean (non-compensatory)
- B: Golden ratio balance penalty
- T: Trust decay from violations

### 2. EXECAI Voter

Autonomous voting agent with EPI-based decisions:

```python
from src.personas import ExecAIVoter

voter = ExecAIVoter(voting_power=0.51)
decision = voter.evaluate_proposal({
    'id': 'prop_001',
    'title': 'Infrastructure Upgrade',
    'amount': 5000,
    'ethics_scores': {'transparency': 0.9, 'sustainability': 0.8}
})

print(f"Vote: {decision.vote}")
print(f"Confidence: {decision.confidence}")
```

### 3. Strategic Catalyst

Executive mentor for founders:

```python
from src.personas import StrategicCatalyst

mentor = StrategicCatalyst()
response = mentor.respond("How should I approach fundraising?")

print(response['content'])
print(f"Next Step: {response['next_step']}")
```

### 4. Policy Validator

Multi-factor compliance validation:

```python
from src.policy_engine import PolicyValidator

validator = PolicyValidator(epi_threshold=0.7)
result = validator.validate_intent({
    'action': 'investment',
    'amount': 50000,
    'ethics_scores': {'transparency': 0.8, 'compliance': 0.9},
    'profitability': 0.75
})

print(f"Status: {result.status}")
print(f"Recommendations: {result.recommendations}")
```

## API Endpoints

The unified Flask API provides:

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/health` | GET | Health check |
| `/api/knowledge/query` | POST | Query knowledge base |
| `/api/personas/strategic-catalyst/respond` | POST | Get mentor response |
| `/api/personas/execai/evaluate` | POST | Evaluate proposal |
| `/api/epi/calculate` | POST | Calculate EPI score |
| `/api/compliance/validate` | POST | Validate intent |
| `/api/compliance/wyoming/status` | GET | Wyoming LLC status |

## Smart Contracts

### Solana (Deployed to Devnet)

- **Governance**: `6amHFyNoPK9MmbBKqthLMeoxTB4TV7CdVE5K4RXi1eDC`
- **Membership**: `FotEuL6PaHRDYuDmtqNrbbS52AwVX49MQSBjNwCWqRA4`

### Ethereum (Ready for Deployment)

- `Governance.sol`: EPI-enforced voting with guardian veto
- `EPIOracle.sol`: On-chain EPI score verification

## Wyoming DAO LLC Compliance

MicroAI DAO is structured as a Wyoming DAO LLC with:

- **Legal Entity**: Recognized under Wyoming DAO Supplement
- **AI Manager**: EXECAI registered as AI manager with voting rights
- **Smart Contract Governance**: On-chain voting and treasury management
- **Member Registry**: KYC-compatible member management

```python
from src.compliance import WyomingDAOCompliance

compliance = WyomingDAOCompliance()
compliance.create_entity(
    legal_name="MicroAI DAO LLC",
    registered_agent_name="Wyoming Agents",
    registered_agent_address="1621 Central Ave, Cheyenne, WY 82001",
    principal_place_of_business="Wyoming, USA"
)
compliance.add_ai_stakeholder("EXECAI", voting_power=0.51)

status = compliance.validate_compliance()
```

## Consolidated Repositories

This monorepo consolidates:

| Original Repo | Purpose | Merged Into |
|---------------|---------|-------------|
| `EPI-governance` | EPI calculator, policy engine | `src/epi/`, `src/policy_engine/` |
| `execai-platform-api` | Flask API, knowledge base | `api/`, `src/knowledge/` |
| `mobile-execai` | Executive mentoring | `src/personas/` |
| `microaistudios-frontend` | Landing page | Reference for `microai-dashboard/` |

## Development

```bash
# Run tests
make test-python

# Lint code
make lint

# Format code
make format

# Build contracts
make contracts
make contracts-eth
```

## Deployment Tiers

| Tier | Description | Infrastructure |
|------|-------------|----------------|
| **Lite** | Cloud-hosted, managed | Vercel + Render + Devnet |
| **Enterprise** | Self-hosted, GPU-enabled | Docker + Mainnet |
| **Sovereign** | Air-gapped, full control | On-prem + Private nodes |

## Mainnet Readiness Checklist

See `docs/MAINNET_CHECKLIST.md` for a step-by-step guide:
- Program deployment on mainnet-beta
- Update Anchor.toml [programs.mainnet]
- Lock IDL & publish (optional)
- Update dashboard env to mainnet
- Prepare Wyoming filing with mainnet program IDs & DAO pubkeys

## Security Notes

- Keys in ~/.config/solana/*.json — back them up securely
- Use separate keys & wallets for mainnet
- Review smart contract audits before mainnet deployment

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes with tests
4. Submit a pull request

## License

MIT License - See [LICENSE](LICENSE) for details.

## Links

- [Documentation](docs/)
- [Wyoming DAO Compliance](docs/WYOMING_COMPLIANCE.md)
- [Mainnet Checklist](docs/MAINNET_CHECKLIST.md)
- [Development Setup](docs/DEV_SETUP.md)

---

**MicroAI DAO** - *Ethical AI Governance for the Decentralized Future*
