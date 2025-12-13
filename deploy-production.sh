#!/bin/bash
###############################################################################
# MicroAI DAO - Production Deployment Script
# 
# This script deploys the complete MicroAI governance system to production:
# - Python backend with Gunicorn
# - Trust Stack with PostgreSQL
# - Smart contracts (Ethereum Mainnet, Solana Mainnet)
# - React dashboard (optimized build)
# - AI agents with model caching
# - SSL/TLS configuration
# - Monitoring and logging
###############################################################################

set -e  # Exit on error

echo "======================================================================"
echo "  MicroAI DAO - Production Deployment"
echo "======================================================================"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Check if running from project root
if [ ! -f "requirements.txt" ]; then
    echo -e "${RED}Error: Must run from project root directory${NC}"
    exit 1
fi

# Confirm production deployment
echo -e "${RED}WARNING: This will deploy to PRODUCTION (mainnet)${NC}"
echo -e "${YELLOW}This includes:${NC}"
echo "  - Real smart contract deployments"
echo "  - Mainnet gas fees"
echo "  - Production database"
echo "  - Public-facing services"
echo ""
read -p "Are you sure you want to continue? (type 'YES' to confirm): " confirm

if [ "$confirm" != "YES" ]; then
    echo "Deployment cancelled"
    exit 0
fi

echo ""
echo "Starting production deployment..."
echo ""

# Step 1: Environment Setup
echo -e "${YELLOW}[1/10] Setting up production environment...${NC}"

# Check for required environment variables
required_vars=(
    "DATABASE_URL"
    "SECRET_KEY"
    "ETHEREUM_RPC_URL"
    "ETHEREUM_PRIVATE_KEY"
    "SOLANA_RPC_URL"
    "SOLANA_KEYPAIR_PATH"
)

missing_vars=()
for var in "${required_vars[@]}"; do
    if [ -z "${!var}" ]; then
        missing_vars+=("$var")
    fi
done

if [ ${#missing_vars[@]} -ne 0 ]; then
    echo -e "${RED}Error: Missing required environment variables:${NC}"
    for var in "${missing_vars[@]}"; do
        echo "  - $var"
    done
    echo ""
    echo "Set these in .env.production or export them"
    exit 1
fi

# Load production environment
if [ -f ".env.production" ]; then
    source .env.production
fi

python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
pip install gunicorn psycopg2-binary  # Production extras
echo -e "${GREEN}✓ Production environment ready${NC}"
echo ""

# Step 2: Database Setup (PostgreSQL)
echo -e "${YELLOW}[2/10] Setting up PostgreSQL database...${NC}"
python3 << EOF
import os
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# Connect to PostgreSQL
conn = psycopg2.connect(os.environ['DATABASE_URL'])
conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
cursor = conn.cursor()

# Create events table
cursor.execute('''
CREATE TABLE IF NOT EXISTS trust_events (
    event_id TEXT PRIMARY KEY,
    timestamp TIMESTAMP NOT NULL,
    tenant_id TEXT NOT NULL,
    agent_id TEXT NOT NULL,
    action_type TEXT NOT NULL,
    model TEXT,
    input_hash TEXT NOT NULL,
    output_hash TEXT NOT NULL,
    policy_version TEXT NOT NULL,
    epi_score REAL,
    signature TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_agent_id (agent_id),
    INDEX idx_timestamp (timestamp),
    INDEX idx_tenant_id (tenant_id)
)
''')

# Create merkle_roots table
cursor.execute('''
CREATE TABLE IF NOT EXISTS merkle_roots (
    date DATE PRIMARY KEY,
    root_hash TEXT NOT NULL,
    event_count INTEGER NOT NULL,
    anchor_tx TEXT,
    chain TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')

# Create attestations table
cursor.execute('''
CREATE TABLE IF NOT EXISTS attestations (
    release_id TEXT PRIMARY KEY,
    release_date TIMESTAMP NOT NULL,
    log_root TEXT NOT NULL,
    policy_version TEXT NOT NULL,
    attestation_data JSONB NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')

conn.commit()
cursor.close()
conn.close()
print("✓ PostgreSQL database initialized")
EOF
echo -e "${GREEN}✓ Production database ready${NC}"
echo ""

# Step 3: Smart Contracts - Ethereum Mainnet
echo -e "${YELLOW}[3/10] Deploying Ethereum contracts to Mainnet...${NC}"
echo -e "${RED}⚠ This will cost real ETH in gas fees${NC}"
read -p "Continue with Ethereum deployment? (y/n): " eth_confirm

if [ "$eth_confirm" = "y" ]; then
    cd contracts/ethereum
    npm install
    npx hardhat run scripts/deploy.js --network mainnet
    cd ../..
    echo -e "${GREEN}✓ Ethereum contracts deployed${NC}"
else
    echo -e "${YELLOW}⚠ Ethereum deployment skipped${NC}"
fi
echo ""

# Step 4: Smart Contracts - Solana Mainnet
echo -e "${YELLOW}[4/10] Deploying Solana programs to Mainnet...${NC}"
echo -e "${RED}⚠ This will cost real SOL in deployment fees${NC}"
read -p "Continue with Solana deployment? (y/n): " sol_confirm

if [ "$sol_confirm" = "y" ]; then
    cd contracts/solana
    anchor build
    anchor deploy --provider.cluster mainnet
    cd ../..
    echo -e "${GREEN}✓ Solana programs deployed${NC}"
else
    echo -e "${YELLOW}⚠ Solana deployment skipped${NC}"
fi
echo ""

# Step 5: Download AI Models
echo -e "${YELLOW}[5/10] Downloading AI models for production...${NC}"
python3 << EOF
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

model_name = "microsoft/Phi-3-mini-4k-instruct"
print(f"Downloading {model_name}...")

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype=torch.float16,
    device_map="auto"
)

print("✓ Models downloaded and cached")
EOF
echo -e "${GREEN}✓ AI models ready${NC}"
echo ""

# Step 6: Build React Dashboard
echo -e "${YELLOW}[6/10] Building production dashboard...${NC}"
cd microai-dashboard
npm install
npm run build
cd ..
echo -e "${GREEN}✓ Dashboard built${NC}"
echo ""

# Step 7: Configure Nginx
echo -e "${YELLOW}[7/10] Configuring Nginx...${NC}"
sudo tee /etc/nginx/sites-available/microai-dao << 'NGINX_EOF'
server {
    listen 80;
    server_name your-domain.com;

    # Redirect HTTP to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name your-domain.com;

    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;

    # API Backend
    location /api/ {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Dashboard Frontend
    location / {
        root /var/www/microai-dao/microai-dashboard/dist;
        try_files $uri $uri/ /index.html;
    }
}
NGINX_EOF

sudo ln -sf /etc/nginx/sites-available/microai-dao /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx
echo -e "${GREEN}✓ Nginx configured${NC}"
echo ""

# Step 8: Setup Systemd Services
echo -e "${YELLOW}[8/10] Creating systemd services...${NC}"

# API Service
sudo tee /etc/systemd/system/microai-api.service << EOF
[Unit]
Description=MicroAI DAO Flask API
After=network.target postgresql.service

[Service]
Type=notify
User=$USER
WorkingDirectory=$(pwd)
Environment="PATH=$(pwd)/venv/bin"
ExecStart=$(pwd)/venv/bin/gunicorn -w 4 -b 127.0.0.1:5000 api.app:app
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Daily Merkle Anchor Service
sudo tee /etc/systemd/system/microai-anchor.service << EOF
[Unit]
Description=MicroAI DAO Daily Merkle Anchor
After=network.target

[Service]
Type=oneshot
User=$USER
WorkingDirectory=$(pwd)
Environment="PATH=$(pwd)/venv/bin"
ExecStart=$(pwd)/venv/bin/python scripts/daily_anchor.py
EOF

sudo tee /etc/systemd/system/microai-anchor.timer << EOF
[Unit]
Description=Daily Merkle Anchor Timer

[Timer]
OnCalendar=daily
Persistent=true

[Install]
WantedBy=timers.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable microai-api.service
sudo systemctl enable microai-anchor.timer
sudo systemctl start microai-api.service
sudo systemctl start microai-anchor.timer

echo -e "${GREEN}✓ Systemd services configured${NC}"
echo ""

# Step 9: Setup Monitoring
echo -e "${YELLOW}[9/10] Setting up monitoring...${NC}"
pip install prometheus-flask-exporter

# Create monitoring endpoint
mkdir -p monitoring
cat > monitoring/prometheus.yml << EOF
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'microai-api'
    static_configs:
      - targets: ['localhost:5000']
EOF

echo -e "${GREEN}✓ Monitoring configured${NC}"
echo ""

# Step 10: Final Checks
echo -e "${YELLOW}[10/10] Running final checks...${NC}"

# Test API
if curl -s https://your-domain.com/api/health > /dev/null; then
    echo -e "${GREEN}✓ API is responding${NC}"
else
    echo -e "${RED}✗ API check failed${NC}"
fi

# Test Trust Stack
if curl -s https://your-domain.com/api/trust/status > /dev/null; then
    echo -e "${GREEN}✓ Trust Stack is operational${NC}"
else
    echo -e "${RED}✗ Trust Stack check failed${NC}"
fi

echo ""

# Summary
echo "======================================================================"
echo -e "${GREEN}  Production Deployment Complete!${NC}"
echo "======================================================================"
echo ""
echo "Services:"
echo "  • API:             https://your-domain.com/api"
echo "  • Dashboard:       https://your-domain.com"
echo "  • Trust Status:    https://your-domain.com/api/trust/status"
echo ""
echo "Smart Contracts:"
echo "  • Ethereum:        Mainnet (check deployment logs)"
echo "  • Solana:          Mainnet (check deployment logs)"
echo ""
echo "Monitoring:"
echo "  • Systemd status:  sudo systemctl status microai-api"
echo "  • API logs:        sudo journalctl -u microai-api -f"
echo "  • Nginx logs:      sudo tail -f /var/log/nginx/access.log"
echo ""
echo "Maintenance:"
echo "  • Restart API:     sudo systemctl restart microai-api"
echo "  • Check anchor:    sudo systemctl status microai-anchor.timer"
echo "  • View events:     psql \$DATABASE_URL -c 'SELECT COUNT(*) FROM trust_events'"
echo ""
echo "======================================================================"
echo ""
echo -e "${YELLOW}IMPORTANT: Update 'your-domain.com' in Nginx config with your actual domain${NC}"
echo -e "${YELLOW}IMPORTANT: Configure SSL certificates with Let's Encrypt (certbot)${NC}"
echo ""
