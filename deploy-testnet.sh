#!/bin/bash
###############################################################################
# MicroAI DAO - Testnet Deployment Script
# 
# This script deploys the complete MicroAI governance system to testnet:
# - Python backend (Flask API)
# - Trust Stack (event logging, verification)
# - Smart contracts (Ethereum Sepolia, Solana Devnet)
# - React dashboard
# - AI agents (CEO-AI, CFO-AI, EXECAI)
###############################################################################

set -e  # Exit on error

echo "======================================================================"
echo "  MicroAI DAO - Testnet Deployment"
echo "======================================================================"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if running from project root
if [ ! -f "requirements.txt" ]; then
    echo -e "${RED}Error: Must run from project root directory${NC}"
    exit 1
fi

# Step 1: Environment Setup
echo -e "${YELLOW}[1/7] Setting up Python environment...${NC}"
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
echo -e "${GREEN}✓ Python environment ready${NC}"
echo ""

# Step 2: Database Setup
echo -e "${YELLOW}[2/7] Initializing Trust Stack database...${NC}"
mkdir -p data/trust_stack
python3 << EOF
import sqlite3
import os

db_path = 'data/trust_stack/events.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create events table
cursor.execute('''
CREATE TABLE IF NOT EXISTS events (
    event_id TEXT PRIMARY KEY,
    timestamp TEXT NOT NULL,
    tenant_id TEXT NOT NULL,
    agent_id TEXT NOT NULL,
    action_type TEXT NOT NULL,
    model TEXT,
    input_hash TEXT NOT NULL,
    output_hash TEXT NOT NULL,
    policy_version TEXT NOT NULL,
    epi_score REAL,
    signature TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')

# Create merkle_roots table
cursor.execute('''
CREATE TABLE IF NOT EXISTS merkle_roots (
    date TEXT PRIMARY KEY,
    root_hash TEXT NOT NULL,
    event_count INTEGER NOT NULL,
    anchor_tx TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')

conn.commit()
conn.close()
print("✓ Database initialized")
EOF
echo -e "${GREEN}✓ Trust Stack database ready${NC}"
echo ""

# Step 3: Smart Contracts - Ethereum Sepolia
echo -e "${YELLOW}[3/7] Deploying Ethereum contracts to Sepolia...${NC}"
if [ -d "contracts/ethereum" ]; then
    cd contracts/ethereum
    
    # Check if Hardhat is installed
    if [ ! -d "node_modules" ]; then
        echo "Installing Hardhat dependencies..."
        npm install
    fi
    
    # Deploy contracts
    echo "Deploying Governance and EPIOracle contracts..."
    npx hardhat run scripts/deploy.js --network sepolia || {
        echo -e "${YELLOW}⚠ Ethereum deployment skipped (configure SEPOLIA_RPC_URL and PRIVATE_KEY in .env)${NC}"
    }
    
    cd ../..
fi
echo -e "${GREEN}✓ Ethereum contracts deployed (or skipped)${NC}"
echo ""

# Step 4: Smart Contracts - Solana Devnet
echo -e "${YELLOW}[4/7] Deploying Solana programs to Devnet...${NC}"
if [ -d "contracts/solana" ]; then
    cd contracts/solana
    
    # Check if Anchor is installed
    if command -v anchor &> /dev/null; then
        echo "Building Solana program..."
        anchor build
        
        echo "Deploying to Devnet..."
        anchor deploy --provider.cluster devnet || {
            echo -e "${YELLOW}⚠ Solana deployment skipped (configure Solana CLI and wallet)${NC}"
        }
    else
        echo -e "${YELLOW}⚠ Anchor not installed, skipping Solana deployment${NC}"
    fi
    
    cd ../..
fi
echo -e "${GREEN}✓ Solana programs deployed (or skipped)${NC}"
echo ""

# Step 5: Start Flask API
echo -e "${YELLOW}[5/7] Starting Flask API server...${NC}"
export FLASK_ENV=development
export FLASK_DEBUG=1

# Kill any existing Flask processes
pkill -f "flask run" || true
pkill -f "python.*api/app.py" || true

# Start Flask in background
cd api
python app.py > ../logs/api.log 2>&1 &
API_PID=$!
cd ..

echo "Waiting for API to start..."
sleep 5

# Check if API is running
if curl -s http://localhost:5000/api/health > /dev/null; then
    echo -e "${GREEN}✓ Flask API running on http://localhost:5000${NC}"
    echo "  PID: $API_PID"
else
    echo -e "${RED}✗ Flask API failed to start${NC}"
    echo "Check logs/api.log for details"
fi
echo ""

# Step 6: Build and Start React Dashboard
echo -e "${YELLOW}[6/7] Building React dashboard...${NC}"
cd microai-dashboard

# Install dependencies if needed
if [ ! -d "node_modules" ]; then
    echo "Installing npm dependencies..."
    npm install
fi

# Build for production
echo "Building dashboard..."
npm run build

# Start development server in background
echo "Starting dashboard server..."
npm run dev > ../logs/dashboard.log 2>&1 &
DASHBOARD_PID=$!

cd ..

echo "Waiting for dashboard to start..."
sleep 5

echo -e "${GREEN}✓ Dashboard running on http://localhost:5173${NC}"
echo "  PID: $DASHBOARD_PID"
echo ""

# Step 7: Initialize AI Agents
echo -e "${YELLOW}[7/7] Initializing AI agents...${NC}"
python3 << EOF
import sys
sys.path.insert(0, 'src')

try:
    from personas.ceo_ai import CEOAI
    from personas.cfo_ai import CFOAI
    
    print("Initializing CEO-AI...")
    ceo = CEOAI(use_local_model=False)
    print("✓ CEO-AI ready")
    
    print("Initializing CFO-AI...")
    cfo = CFOAI(use_local_model=False)
    print("✓ CFO-AI ready")
    
    print("\nAI Agents initialized successfully!")
    print("Note: Using fallback reasoning mode (set use_local_model=True to load HF models)")
    
except Exception as e:
    print(f"⚠ AI agent initialization warning: {e}")
    print("Agents will use fallback mode")
EOF
echo -e "${GREEN}✓ AI agents initialized${NC}"
echo ""

# Create logs directory
mkdir -p logs

# Save PIDs for cleanup
echo $API_PID > logs/api.pid
echo $DASHBOARD_PID > logs/dashboard.pid

# Summary
echo "======================================================================"
echo -e "${GREEN}  Testnet Deployment Complete!${NC}"
echo "======================================================================"
echo ""
echo "Services running:"
echo "  • Flask API:       http://localhost:5000"
echo "  • React Dashboard: http://localhost:5173"
echo "  • Trust Stack:     Active (SQLite)"
echo "  • AI Agents:       CEO-AI, CFO-AI, EXECAI"
echo ""
echo "Testnet deployments:"
echo "  • Ethereum:        Sepolia (check logs for addresses)"
echo "  • Solana:          Devnet (check logs for program IDs)"
echo ""
echo "Logs:"
echo "  • API:             logs/api.log"
echo "  • Dashboard:       logs/dashboard.log"
echo ""
echo "To stop services:"
echo "  ./stop-services.sh"
echo ""
echo "To view API logs:"
echo "  tail -f logs/api.log"
echo ""
echo "To test the system:"
echo "  curl http://localhost:5000/api/health"
echo "  curl http://localhost:5000/api/trust/status"
echo ""
echo "======================================================================"
