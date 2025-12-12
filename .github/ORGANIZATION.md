# MicroAI Studios - GitHub Organization Structure

## Organization: `microai-studios`

### Recommended Team Structure

| Team | Access | Members | Purpose |
|------|--------|---------|---------|
| **guardians** | Admin | Founders, Legal | Class A stakeholders with veto power |
| **core-devs** | Write | Engineers | Core monorepo development |
| **community** | Triage | Contributors | Issue triage, PR reviews |
| **execai-ops** | Read | AI Systems | EXECAI service accounts |

### Repository Structure

```
microai-studios/
├── microai-core          # Main monorepo (this repo)
│   ├── contracts/        # Solana + Ethereum
│   ├── src/              # Python modules (EPI, personas, etc.)
│   ├── api/              # Unified Flask backend
│   ├── dashboard/        # React governance UI
│   └── services/         # Live data server
│
├── frontend              # Landing page (satellite)
│   └── (microaistudios-frontend)
│
├── mobile                # Mobile app (satellite)
│   └── (mobile-execai)
│
├── .github               # Org-wide workflows
│   └── workflows/
│       ├── epi-validation.yml
│       └── compliance-scan.yml
│
└── governance-sdk        # NPM package (future)
    └── @microai/governance
```

### Branch Protection Rules

**For `microai-core`:**
- Require PR reviews from guardians for `contracts/`
- Require EPI validation CI check to pass
- Require compliance scan for Wyoming-related changes

### Governance Voting Power

```
┌────────────────────────────────────────┐
│     BALANCED DAO GOVERNANCE            │
├────────────────────────────────────────┤
│  EXECAI (AI)     │  33%  │ ai-voter   │
│  Founders/Team   │  33%  │ guardians  │
│  Investors       │  33%  │ community  │
└────────────────────────────────────────┘
```

### CI/CD Workflows

1. **EPI Validation** - Runs on all PRs to validate ethical compliance
2. **Compliance Scan** - Checks Wyoming DAO LLC requirements
3. **Contract Audit** - Static analysis on Solana/Ethereum code
4. **Deploy Preview** - Vercel/Railway preview deployments

### Secrets Required

| Secret | Purpose | Scope |
|--------|---------|-------|
| `SOLANA_PRIVATE_KEY` | Devnet deployments | microai-core |
| `ETHEREUM_PRIVATE_KEY` | Sepolia deployments | microai-core |
| `VERCEL_TOKEN` | Frontend deployments | frontend, mobile |
| `EXECAI_API_KEY` | AI service auth | microai-core |

### Migration Checklist

- [ ] Create `microai-studios` organization
- [ ] Transfer `microai-dao` → `microai-core`
- [ ] Transfer `microaistudios-frontend` → `frontend`
- [ ] Transfer `mobile-execai` → `mobile`
- [ ] Archive `EPI-governance` (merged)
- [ ] Archive `execai-platform-api` (merged)
- [ ] Set up teams and permissions
- [ ] Configure branch protection
- [ ] Add org-wide workflows
- [ ] Publish `@microai/governance` SDK
