# Getting Started with MicroAI DAO

## Complete Step-by-Step Guide

This guide will walk you through everything from cloning the repository to deploying to production.

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Initial Setup](#initial-setup)
3. [Local Development](#local-development)
4. [Running Tests](#running-tests)
5. [Deployment to Staging](#deployment-to-staging)
6. [Security Audit](#security-audit)
7. [Production Deployment](#production-deployment)
8. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Required Software

**On Linux (Ubuntu/Debian):**
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python 3.11
sudo apt install -y python3.11 python3.11-venv python3-pip

# Install Node.js 18+ (for dashboard)
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs

# Install Docker and Docker Compose
sudo apt install -y docker.io docker-compose
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker $USER  # Add yourself to docker group

# Install PostgreSQL client (for database operations)
sudo apt install -y postgresql-client

# Install Git
sudo apt install -y git
```

**On macOS:**
```bash
# Install Homebrew if not already installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install required software
brew install python@3.11 node@18 docker docker-compose postgresql git
```

**On Windows:**
- Install WSL2: https://docs.microsoft.com/en-us/windows/wsl/install
- Then follow Linux instructions inside WSL2

---

## Initial Setup

### Step 1: Clone the Repository

```bash
# Navigate to your projects directory
cd ~

# Clone the repository
git clone https://github.com/MicroAIStudios-DAO/microai-dao-core.git

# Navigate into the project
cd microai-dao-core

# Verify you're on the main branch
git branch
# Should show: * main
```

### Step 2: Set Up Python Environment

```bash
# Create a virtual environment
python3.11 -m venv venv

# Activate the virtual environment
source venv/bin/activate  # On Linux/macOS
# OR
venv\Scripts\activate  # On Windows

# Upgrade pip
pip install --upgrade pip

# Install Python dependencies
pip install -r requirements.txt
pip install -r requirements_security.txt

# Verify installation
python --version  # Should show Python 3.11.x
pip list  # Should show all installed packages
```

### Step 3: Set Up Environment Variables

```bash
# Copy the example environment files
cp .env.example .env
cp .env.security.example .env.security

# Edit the .env file with your actual values
nano .env  # or use your preferred editor

# Required variables to set:
# - JWT_SECRET_KEY (generate with: openssl rand -hex 32)
# - SIGNING_KEY (generate with: openssl rand -hex 32)
# - HMAC_SECRET (generate with: openssl rand -hex 32)
# - DATABASE_URL (use SQLite for local: sqlite:///./microai_dao.db)
# - OPENAI_API_KEY (get from https://platform.openai.com/api-keys)
```

**Generate secure keys:**
```bash
# Generate JWT secret
echo "JWT_SECRET_KEY=$(openssl rand -hex 32)"

# Generate signing key
echo "SIGNING_KEY=$(openssl rand -hex 32)"

# Generate HMAC secret
echo "HMAC_SECRET=$(openssl rand -hex 32)"
```

### Step 4: Initialize the Database

```bash
# Run database initialization
python database/init_db.py

# Verify database was created
ls -lh microai_dao.db  # Should see the database file

# Run migrations (if using PostgreSQL)
alembic upgrade head
```

### Step 5: Install Dashboard Dependencies

```bash
# Navigate to dashboard directory
cd microai-dashboard

# Install Node.js dependencies
npm install

# Return to project root
cd ..
```

---

## Local Development

### Option 1: Run Services Individually

**Terminal 1 - Flask API:**
```bash
# Activate virtual environment
source venv/bin/activate

# Set Flask app
export FLASK_APP=api/app.py
export FLASK_ENV=development

# Run Flask server
python -m flask run --host=0.0.0.0 --port=5000

# API will be available at: http://localhost:5000
```

**Terminal 2 - React Dashboard:**
```bash
# Navigate to dashboard
cd microai-dashboard

# Start development server
npm run dev

# Dashboard will be available at: http://localhost:3000
```

### Option 2: Run with Docker Compose (Recommended)

```bash
# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Services will be available at:
# - API: http://localhost:5000
# - Dashboard: http://localhost:3000
# - PostgreSQL: localhost:5432
# - Redis: localhost:6379

# Stop services
docker-compose down
```

### Verify Everything is Running

```bash
# Test API health endpoint
curl http://localhost:5000/health

# Should return: {"status": "healthy"}

# Test authentication endpoint
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "email": "test@example.com", "password": "testpass123"}'

# Open dashboard in browser
# Navigate to: http://localhost:3000
```

---

## Running Tests

### Run All Tests

```bash
# Activate virtual environment
source venv/bin/activate

# Run all tests with coverage
pytest

# View coverage report
open htmlcov/index.html  # Opens in browser
```

### Run Specific Test Suites

```bash
# Unit tests only
pytest tests/unit/ -v

# Integration tests only
pytest tests/integration/ -v

# End-to-end tests only
pytest tests/e2e/ -v

# Run with specific markers
pytest -m unit  # Only unit tests
pytest -m integration  # Only integration tests
pytest -m e2e  # Only e2e tests
pytest -m security  # Only security tests
```

### Run Tests with Coverage

```bash
# Generate coverage report
pytest --cov=src --cov=api --cov-report=html --cov-report=term

# View HTML coverage report
open htmlcov/index.html
```

### Run Specific Test File

```bash
# Test EPI calculator
pytest tests/unit/test_epi_calculator.py -v

# Test policy validator
pytest tests/unit/test_policy_validator.py -v

# Test API endpoints
pytest tests/integration/test_api_endpoints.py -v
```

---

## Deployment to Staging

### Step 1: Prepare Staging Environment

```bash
# Create staging environment file
cp .env.example .env.staging

# Edit staging configuration
nano .env.staging

# Set staging-specific values:
# - FLASK_ENV=staging
# - DATABASE_URL=postgresql://user:pass@staging-db:5432/microai_dao
# - ETHEREUM_RPC_URL=https://sepolia.infura.io/v3/YOUR-PROJECT-ID
# - SOLANA_RPC_URL=https://api.devnet.solana.com
```

### Step 2: Run Deployment Script

```bash
# Make sure you're in the project root
cd ~/microai-dao-core

# Run staging deployment
./deploy-full.sh staging deploy

# This will:
# 1. Create a backup
# 2. Run tests
# 3. Install dependencies
# 4. Run database migrations
# 5. Build Docker images
# 6. Start services
# 7. Run smoke tests
```

### Step 3: Verify Staging Deployment

```bash
# Check service status
docker-compose ps

# Test API health
curl https://staging.microai-dao.io/health

# View logs
docker-compose logs -f api

# Monitor metrics
docker stats
```

### Step 4: Run Comprehensive Tests on Staging

```bash
# SSH into staging server
ssh user@staging.microai-dao.io

# Navigate to project
cd ~/microai-dao-core

# Run full test suite
pytest

# Run example workflows
python examples/full_stack_demo.py
python examples/synthetic_trust_demo.py
python examples/phase1_demo.py
```

---

## Security Audit

### Step 1: Internal Security Review

```bash
# Run security scanners
pip install bandit safety

# Scan for security issues
bandit -r src/ api/ -f json -o security-report.json

# Check for vulnerable dependencies
safety check

# Review security audit documentation
cat docs/SECURITY_AUDIT.md
```

### Step 2: Fix Critical Issues

**Priority 1: Upgrade Password Hashing**
```python
# In api/middleware/auth.py, replace SHA-256 with bcrypt

# Install bcrypt
pip install bcrypt

# Update password hashing function:
import bcrypt

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt).decode()

def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed.encode())
```

**Priority 2: Persist HMAC Secret**
```bash
# Generate HMAC secret
HMAC_SECRET=$(openssl rand -hex 32)

# Add to .env file
echo "HMAC_SECRET=$HMAC_SECRET" >> .env

# Update code to read from environment
# In src/trust_stack/event_logger.py:
import os
HMAC_SECRET = os.getenv('HMAC_SECRET')
```

### Step 3: Contact Security Audit Firms

**OpenZeppelin (Recommended First)**

Email: security@openzeppelin.com

Subject: Smart Contract Audit Request - MicroAI DAO

Body:
```
Hi OpenZeppelin team,

We're building an AI governance framework with EPI-based decision validation
and would like to request a security audit.

Project: MicroAI DAO Core
Repository: https://github.com/MicroAIStudios-DAO/microai-dao-core

Scope:
- 2 Ethereum contracts (~500 lines Solidity)
- 1 Solana program (~300 lines Rust)
- Flask REST API (~2,000 lines Python)
- Focus: Governance, EPI validation, oracle integration, authentication

Timeline: 3-4 weeks preferred
Budget: $30K-$80K

Documentation:
- Security Audit Doc: docs/SECURITY_AUDIT.md
- Architecture: docs/TRUST_STACK_INTEGRATION.md
- Synthetic Trust: docs/synthetic_trust.md

Can we schedule a call to discuss?

Best regards,
[Your Name]
[Your Title]
[Your Email]
[Your Phone]
```

**Trail of Bits (For Comprehensive Audit)**

Contact: https://www.trailofbits.com/contact

Similar email template, emphasize:
- Cryptographic operations (Merkle trees, HMAC signatures)
- Smart contract security
- API security

**Cure53 (For Web Application Security)**

Contact: https://cure53.de/

Focus on:
- Flask API security
- Authentication and authorization
- Input validation
- CORS and security headers

### Step 4: Launch Bug Bounty Program

**Immunefi Platform**

1. Visit: https://immunefi.com/
2. Click "Submit Project"
3. Fill out application:
   - Project: MicroAI DAO
   - Type: DeFi / Governance
   - Blockchain: Ethereum, Solana
   - Rewards: $50K-$250K

**Reward Structure:**
- Critical: $10,000-$50,000
- High: $5,000-$10,000
- Medium: $1,000-$5,000
- Low: $500-$1,000

---

## Production Deployment

### Step 1: Pre-Production Checklist

```bash
# ✅ Security audit completed
# ✅ All critical issues fixed
# ✅ Staging tests passing
# ✅ Bug bounty program launched
# ✅ Legal review completed (Wyoming DAO LLC)
# ✅ Compliance review (SOC2, GDPR, CCPA)
# ✅ Monitoring and alerting configured
# ✅ Backup and disaster recovery plan
# ✅ Rollback procedure tested
```

### Step 2: Prepare Production Environment

```bash
# Create production environment file
cp .env.example .env.production

# Edit production configuration
nano .env.production

# Set production values:
# - FLASK_ENV=production
# - DEBUG=False
# - DATABASE_URL=postgresql://user:pass@prod-db:5432/microai_dao
# - ETHEREUM_RPC_URL=https://mainnet.infura.io/v3/YOUR-PROJECT-ID
# - SOLANA_RPC_URL=https://api.mainnet-beta.solana.com
# - Enable SSL/TLS
# - Use strong secrets
```

### Step 3: Deploy to Production

```bash
# SSH into production server
ssh user@production.microai-dao.io

# Navigate to project
cd ~/microai-dao-core

# Pull latest code
git pull origin main

# Run production deployment
./deploy-full.sh production deploy

# This will:
# 1. Create backup
# 2. Run tests
# 3. Deploy application
# 4. Deploy smart contracts
# 5. Run smoke tests
# 6. Create deployment tag
```

### Step 4: Post-Deployment Verification

```bash
# Test API health
curl https://api.microai-dao.io/health

# Test authentication
curl -X POST https://api.microai-dao.io/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "your-password"}'

# Test EPI calculation
curl https://api.microai-dao.io/api/epi/calculate \
  -H "Authorization: Bearer YOUR-TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"profit": 0.8, "ethics": 0.7, "violations": []}'

# Monitor logs
docker-compose logs -f

# Check metrics
docker stats
```

### Step 5: Enable Monitoring

```bash
# Set up monitoring (Prometheus + Grafana)
docker-compose -f docker-compose.monitoring.yml up -d

# Access Grafana
# Navigate to: https://grafana.microai-dao.io

# Set up alerts (PagerDuty, Slack, Email)
# Configure in: monitoring/alertmanager.yml
```

---

## Troubleshooting

### Common Issues

**Issue: "Permission denied" when running Docker**
```bash
# Add user to docker group
sudo usermod -aG docker $USER

# Log out and log back in, or run:
newgrp docker
```

**Issue: "Port already in use"**
```bash
# Find process using port 5000
lsof -i :5000

# Kill the process
kill -9 <PID>

# Or use different port
export API_PORT=5001
python -m flask run --port=5001
```

**Issue: "Database connection failed"**
```bash
# Check PostgreSQL is running
docker-compose ps postgres

# Check connection string
echo $DATABASE_URL

# Test connection
psql $DATABASE_URL -c "SELECT 1;"
```

**Issue: "Import errors"**
```bash
# Set PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Or add to .bashrc
echo 'export PYTHONPATH="${PYTHONPATH}:$(pwd)"' >> ~/.bashrc
source ~/.bashrc
```

**Issue: "Tests failing"**
```bash
# Clean test cache
pytest --cache-clear

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Run tests with verbose output
pytest -vv
```

**Issue: "Docker build fails"**
```bash
# Clean Docker cache
docker system prune -a

# Rebuild without cache
docker-compose build --no-cache

# Check disk space
df -h
```

### Getting Help

**Documentation:**
- Security Audit: `docs/SECURITY_AUDIT.md`
- Trust Stack Integration: `docs/TRUST_STACK_INTEGRATION.md`
- Synthetic Trust: `docs/synthetic_trust.md`
- Phase 1 Features: `docs/PHASE1_FEATURES.md`

**Community:**
- GitHub Issues: https://github.com/MicroAIStudios-DAO/microai-dao-core/issues
- Discord: [Your Discord Link]
- Email: support@microai-dao.io

**Emergency:**
- Security Issues: security@microai-dao.io
- Critical Bugs: +1-XXX-XXX-XXXX

---

## Next Steps

### Week 1: Testing
- [ ] Clone repository on Linux machine
- [ ] Run local development environment
- [ ] Run all tests
- [ ] Fix any failing tests
- [ ] Deploy to staging

### Week 2-3: Security
- [ ] Fix critical security issues (password hashing, HMAC persistence)
- [ ] Contact OpenZeppelin for audit
- [ ] Launch bug bounty program
- [ ] Internal security review

### Month 2: Audit & Compliance
- [ ] Complete security audit
- [ ] Fix audit findings
- [ ] SOC2 certification prep
- [ ] Legal review (Wyoming DAO LLC)

### Month 3: Production
- [ ] Production deployment
- [ ] Monitoring and alerting
- [ ] User onboarding
- [ ] Marketing launch

---

## Useful Commands Cheat Sheet

```bash
# Development
source venv/bin/activate          # Activate virtual environment
python -m flask run               # Start Flask API
npm run dev                       # Start React dashboard (in microai-dashboard/)
docker-compose up -d              # Start all services

# Testing
pytest                            # Run all tests
pytest tests/unit/ -v             # Run unit tests
pytest --cov=src --cov=api        # Run with coverage

# Deployment
./deploy-full.sh staging deploy   # Deploy to staging
./deploy-full.sh production deploy # Deploy to production
./deploy-full.sh production rollback # Rollback production

# Database
python database/init_db.py        # Initialize database
alembic upgrade head              # Run migrations
alembic downgrade -1              # Rollback one migration

# Docker
docker-compose ps                 # Check service status
docker-compose logs -f api        # View API logs
docker-compose down               # Stop all services
docker system prune -a            # Clean Docker cache

# Git
git pull origin main              # Pull latest changes
git status                        # Check status
git log --oneline -10             # View recent commits
```

---

**Last Updated**: December 12, 2025  
**Version**: 1.0  
**Author**: MicroAI DAO Team

**Questions?** Open an issue on GitHub or email support@microai-dao.io
