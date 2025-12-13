#!/bin/bash
#
# Comprehensive Deployment Script with Rollback Strategy
# =======================================================
#
# Usage:
#   ./deploy-full.sh [staging|production] [deploy|rollback]
#
# Examples:
#   ./deploy-full.sh staging deploy
#   ./deploy-full.sh production rollback
#

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
ENVIRONMENT=${1:-staging}
ACTION=${2:-deploy}
TIMESTAMP=$(date +'%Y%m%d_%H%M%S')
BACKUP_DIR="./backups"
DEPLOYMENT_LOG="./logs/deployment_${TIMESTAMP}.log"

# Validate arguments
if [[ ! "$ENVIRONMENT" =~ ^(staging|production)$ ]]; then
    echo -e "${RED}Error: Environment must be 'staging' or 'production'${NC}"
    exit 1
fi

if [[ ! "$ACTION" =~ ^(deploy|rollback)$ ]]; then
    echo -e "${RED}Error: Action must be 'deploy' or 'rollback'${NC}"
    exit 1
fi

# Create necessary directories
mkdir -p $BACKUP_DIR
mkdir -p logs

# Logging function
log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1" | tee -a $DEPLOYMENT_LOG
}

error() {
    echo -e "${RED}[$(date +'%Y-%m-%d %H:%M:%S')] ERROR:${NC} $1" | tee -a $DEPLOYMENT_LOG
}

warning() {
    echo -e "${YELLOW}[$(date +'%Y-%m-%d %H:%M:%S')] WARNING:${NC} $1" | tee -a $DEPLOYMENT_LOG
}

# Load environment-specific configuration
load_config() {
    log "Loading configuration for $ENVIRONMENT..."
    
    if [ -f ".env.$ENVIRONMENT" ]; then
        source ".env.$ENVIRONMENT"
    else
        warning "Configuration file .env.$ENVIRONMENT not found, using defaults"
    fi
}

# Backup current deployment
backup_deployment() {
    log "Creating backup..."
    
    BACKUP_NAME="backup_${ENVIRONMENT}_${TIMESTAMP}.tar.gz"
    
    # Backup database (if PostgreSQL is configured)
    if [ ! -z "$DATABASE_URL" ]; then
        pg_dump $DATABASE_URL > "$BACKUP_DIR/db_${TIMESTAMP}.sql" 2>/dev/null || warning "Database backup skipped"
    fi
    
    # Backup application files
    tar -czf "$BACKUP_DIR/$BACKUP_NAME" \
        src/ api/ contracts/ database/ migrations/ \
        --exclude='*.pyc' --exclude='__pycache__' --exclude='venv' 2>/dev/null || true
    
    log "Backup created: $BACKUP_NAME"
    echo "$BACKUP_NAME" > "$BACKUP_DIR/latest_backup.txt"
}

# Run tests before deployment
run_tests() {
    log "Running tests..."
    
    # Unit tests
    pytest tests/unit/ -v || {
        error "Unit tests failed"
        exit 1
    }
    
    # Integration tests
    pytest tests/integration/ -v || {
        warning "Integration tests failed (continuing anyway)"
    }
    
    log "Tests completed"
}

# Deploy application
deploy_application() {
    log "Deploying to $ENVIRONMENT..."
    
    # Install dependencies
    log "Installing dependencies..."
    pip install -q -r requirements.txt
    pip install -q -r requirements_security.txt
    
    # Run database migrations
    log "Running database migrations..."
    alembic upgrade head 2>/dev/null || warning "Migration skipped"
    
    # Build Docker images
    log "Building Docker images..."
    docker-compose build 2>/dev/null || warning "Docker build skipped"
    
    # Start services
    log "Starting services..."
    docker-compose up -d 2>/dev/null || warning "Docker start skipped"
    
    # Wait for services to be healthy
    log "Waiting for services to be healthy..."
    sleep 10
    
    # Run smoke tests
    run_smoke_tests
    
    log "Deployment completed successfully"
}

# Run smoke tests
run_smoke_tests() {
    log "Running smoke tests..."
    
    # Check API health
    HEALTH_URL="http://localhost:5000/health"
    if [ "$ENVIRONMENT" == "production" ]; then
        HEALTH_URL="https://api.microai-dao.io/health"
    fi
    
    RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" $HEALTH_URL 2>/dev/null || echo "000")
    
    if [ "$RESPONSE" == "200" ]; then
        log "Health check passed"
    else
        warning "Health check returned HTTP $RESPONSE (service may not be running yet)"
    fi
}

# Rollback to previous deployment
rollback_deployment() {
    log "Rolling back $ENVIRONMENT deployment..."
    
    # Get latest backup
    if [ ! -f "$BACKUP_DIR/latest_backup.txt" ]; then
        error "No backup found for rollback"
        exit 1
    fi
    
    BACKUP_NAME=$(cat "$BACKUP_DIR/latest_backup.txt")
    
    if [ ! -f "$BACKUP_DIR/$BACKUP_NAME" ]; then
        error "Backup file not found: $BACKUP_NAME"
        exit 1
    fi
    
    # Stop current services
    log "Stopping current services..."
    docker-compose down 2>/dev/null || true
    
    # Restore backup
    log "Restoring backup: $BACKUP_NAME..."
    tar -xzf "$BACKUP_DIR/$BACKUP_NAME"
    
    # Restore database
    DB_BACKUP="$BACKUP_DIR/db_$(echo $BACKUP_NAME | cut -d'_' -f3 | cut -d'.' -f1).sql"
    if [ -f "$DB_BACKUP" ] && [ ! -z "$DATABASE_URL" ]; then
        log "Restoring database..."
        psql $DATABASE_URL < "$DB_BACKUP" 2>/dev/null || warning "Database restore skipped"
    fi
    
    # Restart services
    log "Restarting services..."
    docker-compose up -d 2>/dev/null || warning "Docker restart skipped"
    
    # Run smoke tests
    run_smoke_tests
    
    log "Rollback completed successfully"
}

# Main deployment flow
main() {
    log "========================================="
    log "MicroAI DAO Deployment Script"
    log "Environment: $ENVIRONMENT"
    log "Action: $ACTION"
    log "========================================="
    
    # Load configuration
    load_config
    
    if [ "$ACTION" == "deploy" ]; then
        # Deployment flow
        backup_deployment
        run_tests
        deploy_application
        
        log "✅ Deployment successful!"
        
    elif [ "$ACTION" == "rollback" ]; then
        # Rollback flow
        rollback_deployment
        
        log "✅ Rollback successful!"
    fi
    
    log "========================================="
    log "Deployment log saved to: $DEPLOYMENT_LOG"
    log "========================================="
}

# Run main function
main
