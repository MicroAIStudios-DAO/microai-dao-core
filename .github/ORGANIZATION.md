# MicroAI Studios DAO - GitHub Organization Structure

## Organization: [`MicroAIStudios-DAO`](https://github.com/MicroAIStudios-DAO)

### Recommended Team Structure

| Team | Access | Members | Purpose |
|------|--------|---------|---------|
| **guardians** | Admin | Founders, Legal | Class A stakeholders with veto power (33%) |
| **core-devs** | Write | Engineers | Core monorepo development |
| **community** | Triage | Contributors | Investors/public stakeholders (33%) |
| **execai-ops** | Read | AI Systems | EXECAI service accounts (33%) |

### Repository Structure

```
MicroAIStudios-DAO/
├── microai-core          # Main monorepo (from Gnoscenti/microai-dao)
│   ├── contracts/        # Solana + Ethereum
│   ├── src/              # Python modules (EPI, personas, etc.)
│   ├── api/              # Unified Flask backend
│   ├── microai-dashboard/# React governance UI
│   └── services/         # Live data server
│
├── frontend              # Landing page (from Gnoscenti/microaistudios-frontend)
│
├── mobile                # Mobile app (from Gnoscenti/mobile-execai)
│
└── .github               # Org-wide workflows (future)
    └── workflows/
```

### Governance Voting Power

```
┌────────────────────────────────────────┐
│     BALANCED DAO GOVERNANCE            │
├────────────────────────────────────────┤
│  EXECAI (AI)     │  33%  │ execai-ops │
│  Founders/Team   │  33%  │ guardians  │
│  Investors       │  33%  │ community  │
└────────────────────────────────────────┘
```

### Transfer Instructions

#### Step 1: Transfer Repos to Organization

For each repo, go to **Settings → Danger Zone → Transfer ownership**

| Source | Target | New Name |
|--------|--------|----------|
| `Gnoscenti/microai-dao` | `MicroAIStudios-DAO/microai-core` | microai-core |
| `Gnoscenti/microaistudios-frontend` | `MicroAIStudios-DAO/frontend` | frontend |
| `Gnoscenti/mobile-execai` | `MicroAIStudios-DAO/mobile` | mobile |

#### Step 2: Archive Merged Repos

These are now consolidated into `microai-core`:
- `Gnoscenti/EPI-governance` → Archive
- `Gnoscenti/execai-platform-api` → Archive

#### Step 3: Set Up Teams

1. Go to: https://github.com/orgs/MicroAIStudios-DAO/teams
2. Create teams: `guardians`, `core-devs`, `community`, `execai-ops`
3. Assign permissions per table above

#### Step 4: Configure Branch Protection

For `microai-core` main branch:
- Require pull request reviews
- Require status checks (EPI validation, compliance scan)
- Restrict who can push to matching branches

### CI/CD Workflows

Already configured in `.github/workflows/`:
1. **ci.yml** - Tests, lint, build
2. **epi-validation.yml** - Ethical compliance checks
3. **compliance-scan.yml** - Wyoming DAO LLC validation

### Secrets Required

| Secret | Purpose | Scope |
|--------|---------|-------|
| `SOLANA_PRIVATE_KEY` | Devnet deployments | microai-core |
| `ETHEREUM_PRIVATE_KEY` | Sepolia deployments | microai-core |
| `VERCEL_TOKEN` | Frontend deployments | frontend, mobile |
| `EXECAI_API_KEY` | AI service auth | microai-core |

### Migration Checklist

- [x] Create `MicroAIStudios-DAO` organization
- [ ] Transfer `microai-dao` → `microai-core`
- [ ] Transfer `microaistudios-frontend` → `frontend`
- [ ] Transfer `mobile-execai` → `mobile`
- [ ] Archive `EPI-governance` (merged)
- [ ] Archive `execai-platform-api` (merged)
- [ ] Set up teams and permissions
- [ ] Configure branch protection
- [ ] Add org secrets
