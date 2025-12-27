# MicroAI DAO Core - Repository Restructuring Plan

## Executive Summary

This document outlines a comprehensive restructuring plan for the MicroAI DAO Core repository to align with enterprise best practices, improve developer experience, and position the project as production-ready infrastructure.

**Current Issues:**
- 30+ files cluttering the root directory
- - Business/legal documents (.docx) mixed with source code
  - - Multiple scattered README files
    - - Inconsistent file naming conventions
      - - Duplicate files (e.g., two Operating Agreement versions)
        - - Documentation spread across root instead of organized in /docs
         
          - ---

          ## Target Directory Structure

          ```
          microai-dao-core/
          ├── .github/                    # GitHub-specific files
          │   ├── ISSUE_TEMPLATE/
          │   ├── PULL_REQUEST_TEMPLATE.md
          │   ├── workflows/              # CI/CD pipelines
          │   └── CODEOWNERS
          │
          ├── contracts/                  # Smart contracts (existing)
          │   ├── solana/
          │   └── ethereum/
          │
          ├── src/                        # Core Python source (existing)
          │   ├── epi/
          │   ├── policy_engine/
          │   ├── trust_stack/
          │   ├── personas/
          │   ├── knowledge/
          │   ├── ai_c_suite/
          │   └── compliance/
          │
          ├── api/                        # Flask API (existing)
          │
          ├── microai-dashboard/          # React frontend (existing)
          │
          ├── database/                   # Database schemas (existing)
          │
          ├── tests/                      # Test suite (existing)
          │   ├── unit/
          │   ├── integration/
          │   └── e2e/
          │
          ├── docs/                       # ALL documentation
          │   ├── technical/              # Technical docs
          │   │   ├── architecture.md
          │   │   ├── api-reference.md
          │   │   ├── deployment.md
          │   │   └── security.md
          │   ├── legal/                  # Legal documents (converted to PDF)
          │   │   ├── executive-summary.pdf
          │   │   ├── business-plan.pdf
          │   │   ├── articles-of-organization.pdf
          │   │   ├── operating-agreement.pdf
          │   │   └── high-level-explainer.pdf
          │   ├── governance/             # DAO governance docs
          │   │   ├── wyoming-compliance.md
          │   │   ├── voting-procedures.md
          │   │   └── stakeholder-guide.md
          │   ├── guides/                 # User guides
          │   │   ├── getting-started.md
          │   │   ├── installation.md
          │   │   └── contributing.md
          │   └── reports/                # Status reports & audits
          │       ├── deployment-status.md
          │       ├── test-reports.md
          │       └── security-audit.md
          │
          ├── scripts/                    # Utility scripts (existing)
          │   ├── setup.sh
          │   ├── deploy.sh
          │   └── test.sh
          │
          ├── docker/                     # Docker configs (existing)
          │
          ├── examples/                   # Example code (existing)
          │
          ├── config/                     # Configuration files (NEW)
          │   ├── .env.example
          │   └── settings.py
          │
          ├── .gitignore
          ├── .env.example
          ├── Dockerfile
          ├── docker-compose.yml
          ├── Makefile
          ├── pyproject.toml              # Modern Python packaging
          ├── requirements.txt
          ├── requirements-dev.txt
          ├── LICENSE
          ├── README.md                   # Single, comprehensive README
          ├── CHANGELOG.md
          ├── CONTRIBUTING.md
          ├── SECURITY.md
          └── CODE_OF_CONDUCT.md
          ```

          ---

          ## Phase 1: Document Organization (Claude Desktop Script)

          ### Step 1.1: Create New Directory Structure

          ```bash
          #!/bin/bash
          # Run from repository root

          # Create documentation subdirectories
          mkdir -p docs/technical
          mkdir -p docs/legal
          mkdir -p docs/governance
          mkdir -p docs/guides
          mkdir -p docs/reports
          mkdir -p config

          echo "Directory structure created"
          ```

          ### Step 1.2: Move Legal Documents

          ```bash
          #!/bin/bash
          # Move .docx files to docs/legal/
          # Note: Recommend converting to PDF for better accessibility

          git mv "01_Executive_Summary.docx" docs/legal/executive-summary.docx
          git mv "02_Business_Plan.docx" docs/legal/business-plan.docx
          git mv "03_Articles_of_Organization.docx" docs/legal/articles-of-organization.docx
          git mv "04_Operating_Agreement.docx" docs/legal/operating-agreement.docx
          git rm "04_Operating_Agreement(1).docx"  # Remove duplicate
          git mv "05_High_Level_Explainer.docx" docs/legal/high-level-explainer.docx

          git commit -m "chore: organize legal documents into docs/legal/"
          ```

          ### Step 1.3: Consolidate Technical Documentation

          ```bash
          #!/bin/bash
          # Move scattered .md files to appropriate docs/ subdirectories

          # Technical docs
          git mv DEPLOYMENT_STATUS.md docs/reports/deployment-status.md
          git mv DEPLOYMENT_TEST_REPORT.md docs/reports/deployment-test-report.md
          git mv TEST_REPORT.md docs/reports/test-report.md
          git mv FINAL_TEST_RESULTS.md docs/reports/final-test-results.md
          git mv TEST_SUMMARY.txt docs/reports/test-summary.txt
          git mv INTEGRATION_SUMMARY.md docs/reports/integration-summary.md

          # Security docs
          git mv SECURITY_AUDIT_FINDINGS.md docs/reports/security-audit-findings.md
          git mv SECURITY_IMPLEMENTATION_COMPLETE.md docs/reports/security-implementation-complete.md
          git mv SECURITY_STATUS_FINAL.md docs/reports/security-status-final.md

          # Phase/Feature docs
          git mv PHASE1_COMPLETE.md docs/technical/phase1-complete.md
          git mv SYNTHETIC_TRUST_COMPLETE.md docs/technical/synthetic-trust-complete.md

          # Guides
          git mv GETTING_STARTED.md docs/guides/getting-started.md
          git mv "Quick Start Guide.md" docs/guides/quick-start.md
          git mv COMPLETE_IMPLEMENTATION_GUIDE.md docs/guides/implementation-guide.md
          git mv "Kubuntu Setup Guide for MicroAI DAO LLC.md" docs/guides/kubuntu-setup.md
          git mv "Step-by-Step Deployment Guide for MicroAI D..." docs/guides/deployment-guide.md
          git mv "Setting Up Your GitHub Repository.md" docs/guides/github-setup.md

          # Governance docs
          git mv "MicroAI DAO LLC.md" docs/governance/dao-overview.md
          git mv "Minimum Requirements for Wyoming DAO LL..." docs/governance/wyoming-requirements.md

          # Technical reference
          git mv "TheEthicalProfitabilityIndex(EPI)_AMathematic..." docs/technical/epi-mathematical-framework.md
          git mv "EXECAIDAOSmartContractImplementationGuid..." docs/technical/smart-contract-guide.md
          git mv "GStyle Output Framework.md" docs/technical/output-framework.md

          git commit -m "chore: consolidate documentation into docs/ subdirectories"
          ```

          ### Step 1.4: Clean Up Redundant README Files

          ```bash
          #!/bin/bash
          # Consolidate multiple READMEs

          # Archive old READMEs into docs for reference
          git mv README_PHASE1.md docs/technical/readme-phase1-archive.md
          git mv README_TRUST_STACK.md docs/technical/readme-trust-stack-archive.md

          # Keep only main README.md (will be updated)

          git commit -m "chore: consolidate README files"
          ```

          ### Step 1.5: Move Miscellaneous Files

          ```bash
          #!/bin/bash
          # Move remaining scattered files

          # Config files
          git mv .env.example config/.env.example
          git mv .env.security.example config/.env.security.example

          # Remove WARP.md if deprecated
          git rm WARP.md  # or move to docs/archived/ if needed

          # Handle any remaining files
          git mv "Updated Commands for gnoscenti.md" docs/guides/cli-commands.md
          git mv "MISSING_FILES_CHECKLIST.md" docs/reports/missing-files-checklist.md

          git commit -m "chore: organize remaining files"
          ```

          ---

          ## Phase 2: File Naming Standardization

          ### Naming Conventions

          | Type | Convention | Example |
          |------|------------|---------|
          | Directories | lowercase, hyphens | `trust-stack/` |
          | Python files | snake_case | `trust_metrics.py` |
          | Markdown docs | lowercase, hyphens | `getting-started.md` |
          | Config files | lowercase, dots | `.env.example` |
          | Legal docs | lowercase, hyphens | `operating-agreement.pdf` |

          ### Rename Script

          ```bash
          #!/bin/bash
          # Standardize file names (run after Phase 1)

          cd docs/

          # Fix any uppercase or space issues
          find . -name "*.md" -exec rename 's/[A-Z]/\L$&/g; s/ /-/g; s/_/-/g' {} \;

          git add -A
          git commit -m "chore: standardize file naming conventions"
          ```

          ---

          ## Phase 3: Update Main README.md

          The main README should be concise and follow this structure:

          ```markdown
          # MicroAI DAO Core

          Production-ready AI governance infrastructure with Wyoming DAO LLC compliance.

          ## Quick Start

          [5-line install command]

          ## Documentation

          - [Getting Started](docs/guides/getting-started.md)
          - [API Reference](docs/technical/api-reference.md)
          - [Deployment Guide](docs/guides/deployment-guide.md)
          - [Security](SECURITY.md)

          ## Architecture

          [Brief diagram or description]

          ## Status

          | Component | Status |
          |-----------|--------|
          | Core | ✅ Production Ready |
          | API | 🔄 In Progress |
          | Contracts | ✅ Devnet Deployed |

          ## Contributing

          See [CONTRIBUTING.md](CONTRIBUTING.md)

          ## License

          MIT - See [LICENSE](LICENSE)
          ```

          ---

          ## Phase 4: Add Enterprise Standard Files

          ### 4.1 Create CONTRIBUTING.md

          ```bash
          cat > CONTRIBUTING.md << 'EOF'
          # Contributing to MicroAI DAO Core

          ## Development Setup

          1. Fork the repository
          2. Clone your fork
          3. Install dependencies: `pip install -r requirements-dev.txt`
          4. Create a branch: `git checkout -b feature/your-feature`

          ## Code Standards

          - Python: Follow PEP 8, use Black formatter
          - TypeScript: Follow ESLint configuration
          - Commits: Use conventional commits (feat:, fix:, docs:, chore:)

          ## Pull Request Process

          1. Update documentation for any API changes
          2. Add tests for new functionality
          3. Ensure all tests pass: `pytest tests/`
          4. Request review from maintainers

          ## Code of Conduct

          See [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)
          EOF

          git add CONTRIBUTING.md
          git commit -m "docs: add CONTRIBUTING.md"
          ```

          ### 4.2 Create SECURITY.md

          ```bash
          cat > SECURITY.md << 'EOF'
          # Security Policy

          ## Supported Versions

          | Version | Supported          |
          | ------- | ------------------ |
          | 0.1.x   | :white_check_mark: |

          ## Reporting a Vulnerability

          Please report security vulnerabilities to: security@microaistudios.io

          Do NOT create public GitHub issues for security vulnerabilities.

          ## Security Measures

          - All commits are signed
          - Dependencies are audited regularly
          - Smart contracts pending OpenZeppelin audit
          EOF

          git add SECURITY.md
          git commit -m "docs: add SECURITY.md"
          ```

          ### 4.3 Create CHANGELOG.md

          ```bash
          cat > CHANGELOG.md << 'EOF'
          # Changelog

          All notable changes to this project will be documented in this file.

          The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

          ## [Unreleased]

          ### Added
          - Synthetic Trust Framework integration
          - Phase 1 Enterprise Features
          - Security implementation

          ### Changed
          - AI voting power from 51% to 33% for balanced governance

          ### Fixed
          - EventLogger API mismatch
          - ValidationStatus export

          ## [0.1.0] - 2024-12-13

          ### Added
          - Initial release
          - EPI Calculator
          - EXECAI Voter
          - Wyoming DAO compliance module
          - Solana smart contracts (Devnet)
          EOF

          git add CHANGELOG.md
          git commit -m "docs: add CHANGELOG.md"
          ```

          ---

          ## Phase 5: Python Project Modernization

          ### 5.1 Create pyproject.toml

          ```toml
          [build-system]
          requires = ["setuptools>=61.0", "wheel"]
          build-backend = "setuptools.build_meta"

          [project]
          name = "microai-dao-core"
          version = "0.1.0"
          description = "AI-governed DAO infrastructure with Wyoming LLC compliance"
          readme = "README.md"
          license = {text = "MIT"}
          requires-python = ">=3.11"
          authors = [
              {name = "MicroAI Studios DAO", email = "dev@microaistudios.io"}
          ]
          classifiers = [
              "Development Status :: 3 - Alpha",
              "Intended Audience :: Developers",
              "License :: OSI Approved :: MIT License",
              "Programming Language :: Python :: 3.11",
          ]

          dependencies = [
              "flask>=2.0.0",
              "python-dotenv>=1.0.0",
              "bcrypt>=4.0.0",
              "PyJWT>=2.0.0",
          ]

          [project.optional-dependencies]
          dev = [
              "pytest>=7.0.0",
              "pytest-cov>=4.0.0",
              "black>=23.0.0",
              "flake8>=6.0.0",
              "mypy>=1.0.0",
          ]

          [tool.black]
          line-length = 88
          target-version = ['py311']

          [tool.pytest.ini_options]
          testpaths = ["tests"]
          python_files = ["test_*.py"]
          ```

          ---

          ## Phase 6: CI/CD Setup

          ### 6.1 Create GitHub Actions Workflow

          ```yaml
          # .github/workflows/ci.yml
          name: CI

          on:
            push:
              branches: [main]
            pull_request:
              branches: [main]

          jobs:
            test:
              runs-on: ubuntu-latest
              steps:
                - uses: actions/checkout@v4
                - uses: actions/setup-python@v5
                  with:
                    python-version: '3.11'
                - name: Install dependencies
                  run: |
                    pip install -r requirements.txt
                    pip install -r requirements-dev.txt
                - name: Run tests
                  run: pytest tests/unit/ -v --cov=src
                - name: Lint
                  run: |
                    black --check src/
                    flake8 src/
          ```

          ---

          ## Complete Restructuring Script

          Save this as `scripts/restructure.sh` and run with Claude Desktop:

          ```bash
          #!/bin/bash
          set -e

          echo "=== MicroAI DAO Core Restructuring ==="
          echo "This script will reorganize the repository structure."
          echo ""

          # Phase 1: Create directories
          echo "Phase 1: Creating directory structure..."
          mkdir -p docs/{technical,legal,governance,guides,reports}
          mkdir -p config
          mkdir -p .github/workflows

          # Phase 2: Move legal documents
          echo "Phase 2: Moving legal documents..."
          git mv "01_Executive_Summary.docx" docs/legal/executive-summary.docx 2>/dev/null || true
          git mv "02_Business_Plan.docx" docs/legal/business-plan.docx 2>/dev/null || true
          git mv "03_Articles_of_Organization.docx" docs/legal/articles-of-organization.docx 2>/dev/null || true
          git mv "04_Operating_Agreement.docx" docs/legal/operating-agreement.docx 2>/dev/null || true
          git rm "04_Operating_Agreement(1).docx" 2>/dev/null || true
          git mv "05_High_Level_Explainer.docx" docs/legal/high-level-explainer.docx 2>/dev/null || true

          # Phase 3: Move technical docs
          echo "Phase 3: Moving technical documentation..."
          git mv DEPLOYMENT_STATUS.md docs/reports/ 2>/dev/null || true
          git mv DEPLOYMENT_TEST_REPORT.md docs/reports/ 2>/dev/null || true
          git mv TEST_REPORT.md docs/reports/ 2>/dev/null || true
          git mv FINAL_TEST_RESULTS.md docs/reports/ 2>/dev/null || true
          git mv INTEGRATION_SUMMARY.md docs/reports/ 2>/dev/null || true
          git mv SECURITY_AUDIT_FINDINGS.md docs/reports/ 2>/dev/null || true
          git mv SECURITY_IMPLEMENTATION_COMPLETE.md docs/reports/ 2>/dev/null || true
          git mv SECURITY_STATUS_FINAL.md docs/reports/ 2>/dev/null || true
          git mv PHASE1_COMPLETE.md docs/technical/ 2>/dev/null || true
          git mv SYNTHETIC_TRUST_COMPLETE.md docs/technical/ 2>/dev/null || true
          git mv GETTING_STARTED.md docs/guides/ 2>/dev/null || true
          git mv COMPLETE_IMPLEMENTATION_GUIDE.md docs/guides/ 2>/dev/null || true

          # Phase 4: Clean up redundant files
          echo "Phase 4: Cleaning up..."
          git mv README_PHASE1.md docs/technical/ 2>/dev/null || true
          git mv README_TRUST_STACK.md docs/technical/ 2>/dev/null || true

          # Phase 5: Commit
          echo "Phase 5: Committing changes..."
          git add -A
          git commit -m "chore: restructure repository for enterprise standards

          - Organize legal documents into docs/legal/
          - Consolidate technical docs into docs/technical/
          - Move guides to docs/guides/
          - Move reports to docs/reports/
          - Remove duplicate files
          - Clean up root directory"

          echo ""
          echo "=== Restructuring Complete ==="
          echo "Next steps:"
          echo "1. Update README.md with new documentation links"
          echo "2. Add CONTRIBUTING.md, SECURITY.md, CHANGELOG.md"
          echo "3. Create pyproject.toml for modern Python packaging"
          echo "4. Set up GitHub Actions CI/CD"
          ```

          ---

          ## Post-Restructuring: Updated README Quick Start

          After restructuring, update the main README.md with:

          ```bash
          # Quick Start

          git clone https://github.com/MicroAIStudios-DAO/microai-dao-core.git
          cd microai-dao-core
          pip install -r requirements.txt
          python database/init_db.py
          pytest tests/unit/ -v
          ```

          This command sequence remains unchanged as the core directory structure (src/, database/, tests/) is preserved.

          ---

          ## Verification Checklist

          After running the restructuring script:

          - [ ] All .docx files moved to `docs/legal/`
          - [ ] - [ ] All .md documentation in appropriate `docs/` subdirectory
          - [ ] - [ ] Root directory contains only essential files
          - [ ] - [ ] No duplicate files remain
          - [ ] - [ ] `pytest tests/unit/ -v` passes
          - [ ] - [ ] `python database/init_db.py` works
          - [ ] - [ ] Import paths still function (no changes to src/)
         
          - [ ] ---
         
          - [ ] ## Timeline Estimate
         
          - [ ] | Phase | Duration | Description |
          - [ ] |-------|----------|-------------|
          - [ ] | 1 | 30 min | Run restructure script |
          - [ ] | 2 | 15 min | Verify and fix any issues |
          - [ ] | 3 | 30 min | Update README and add standard files |
          - [ ] | 4 | 30 min | Set up CI/CD |
          - [ ] | 5 | 15 min | Final testing |
         
          - [ ] **Total: ~2 hours**
         
          - [ ] ---
         
          - [ ] *Document created: December 26, 2025*
          - [ ] *For use with Claude Desktop local development environment*
