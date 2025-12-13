-- MicroAI DAO Database Schema
-- Version: 2.0 (Enterprise Edition)
-- Supports: Organizations, Stakeholders, Models, Proposals, Votes, Trust Events

-- ============================================================================
-- ORGANIZATIONS
-- ============================================================================

CREATE TABLE IF NOT EXISTS organizations (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    dao_address TEXT UNIQUE,
    governance_token_address TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status TEXT DEFAULT 'active',
    metadata TEXT  -- JSON: settings, configuration
);

CREATE INDEX idx_organizations_status ON organizations(status);
CREATE INDEX idx_organizations_created_at ON organizations(created_at);

-- ============================================================================
-- STAKEHOLDERS
-- ============================================================================

CREATE TABLE IF NOT EXISTS stakeholders (
    id TEXT PRIMARY KEY,
    org_id TEXT REFERENCES organizations(id) ON DELETE CASCADE,
    wallet_address TEXT UNIQUE NOT NULL,
    name TEXT,
    role TEXT,  -- TECHNICAL, BUSINESS, ETHICS, LEGAL
    voting_power REAL DEFAULT 1.0,
    delegation_address TEXT,  -- Address stakeholder delegates to
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status TEXT DEFAULT 'active',
    metadata TEXT  -- JSON: additional info
);

CREATE INDEX idx_stakeholders_org ON stakeholders(org_id);
CREATE INDEX idx_stakeholders_wallet ON stakeholders(wallet_address);
CREATE INDEX idx_stakeholders_role ON stakeholders(role);
CREATE INDEX idx_stakeholders_status ON stakeholders(status);

-- ============================================================================
-- AI MODELS
-- ============================================================================

CREATE TABLE IF NOT EXISTS ai_models (
    id TEXT PRIMARY KEY,
    org_id TEXT REFERENCES organizations(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    model_type TEXT NOT NULL,  -- classification, generation, agent, etc.
    version TEXT NOT NULL,
    description TEXT,
    use_case TEXT,
    owner_id TEXT REFERENCES stakeholders(id),
    risk_tier INTEGER CHECK (risk_tier BETWEEN 1 AND 4),
    deployment_status TEXT DEFAULT 'registered',
    ipfs_hash TEXT,  -- Model weights on IPFS
    model_hash TEXT,  -- SHA-256 hash for verification
    epi_score REAL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deployed_at TIMESTAMP,
    deprecated_at TIMESTAMP,
    metadata TEXT,  -- JSON: performance metrics, tags, etc.
    UNIQUE(org_id, name, version)
);

CREATE INDEX idx_models_org ON ai_models(org_id);
CREATE INDEX idx_models_status ON ai_models(deployment_status);
CREATE INDEX idx_models_risk_tier ON ai_models(risk_tier);
CREATE INDEX idx_models_owner ON ai_models(owner_id);
CREATE INDEX idx_models_created_at ON ai_models(created_at);

-- ============================================================================
-- PROPOSALS
-- ============================================================================

CREATE TABLE IF NOT EXISTS proposals (
    id TEXT PRIMARY KEY,
    org_id TEXT REFERENCES organizations(id) ON DELETE CASCADE,
    proposal_type TEXT NOT NULL,  -- model_deployment, budget_allocation, risk_update, etc.
    title TEXT NOT NULL,
    description TEXT,
    proposer_id TEXT REFERENCES stakeholders(id),
    model_id TEXT REFERENCES ai_models(id),
    status TEXT DEFAULT 'pending',  -- pending, active, passed, rejected, executed, cancelled
    voting_start TIMESTAMP,
    voting_end TIMESTAMP,
    execution_time TIMESTAMP,
    quorum_required REAL DEFAULT 0.30,
    majority_required REAL DEFAULT 0.50,
    votes_for INTEGER DEFAULT 0,
    votes_against INTEGER DEFAULT 0,
    votes_abstain INTEGER DEFAULT 0,
    total_voting_power REAL DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    metadata TEXT  -- JSON: additional proposal data
);

CREATE INDEX idx_proposals_org ON proposals(org_id);
CREATE INDEX idx_proposals_status ON proposals(status);
CREATE INDEX idx_proposals_type ON proposals(proposal_type);
CREATE INDEX idx_proposals_proposer ON proposals(proposer_id);
CREATE INDEX idx_proposals_model ON proposals(model_id);
CREATE INDEX idx_proposals_voting_end ON proposals(voting_end);

-- ============================================================================
-- VOTES
-- ============================================================================

CREATE TABLE IF NOT EXISTS votes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    proposal_id TEXT REFERENCES proposals(id) ON DELETE CASCADE,
    stakeholder_id TEXT REFERENCES stakeholders(id),
    vote_choice TEXT NOT NULL,  -- for, against, abstain
    vote_weight REAL NOT NULL,
    reasoning TEXT,
    signature TEXT,  -- Cryptographic signature
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    metadata TEXT,  -- JSON: additional vote data
    UNIQUE(proposal_id, stakeholder_id)
);

CREATE INDEX idx_votes_proposal ON votes(proposal_id);
CREATE INDEX idx_votes_stakeholder ON votes(stakeholder_id);
CREATE INDEX idx_votes_choice ON votes(vote_choice);
CREATE INDEX idx_votes_created_at ON votes(created_at);

-- ============================================================================
-- TRUST EVENTS (from Trust Stack)
-- ============================================================================

CREATE TABLE IF NOT EXISTS trust_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_id TEXT UNIQUE NOT NULL,
    org_id TEXT REFERENCES organizations(id) ON DELETE CASCADE,
    agent_id TEXT NOT NULL,  -- AI agent identifier
    action_type TEXT NOT NULL,
    input_hash TEXT NOT NULL,
    output_hash TEXT NOT NULL,
    epi_score REAL,
    risk_tier INTEGER,
    signature TEXT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    policy_version TEXT,
    metadata TEXT  -- JSON: additional event data
);

CREATE INDEX idx_trust_events_org ON trust_events(org_id);
CREATE INDEX idx_trust_events_agent ON trust_events(agent_id);
CREATE INDEX idx_trust_events_action ON trust_events(action_type);
CREATE INDEX idx_trust_events_timestamp ON trust_events(timestamp);
CREATE INDEX idx_trust_events_event_id ON trust_events(event_id);

-- ============================================================================
-- MERKLE ANCHORS (from Trust Stack)
-- ============================================================================

CREATE TABLE IF NOT EXISTS merkle_anchors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    org_id TEXT REFERENCES organizations(id) ON DELETE CASCADE,
    merkle_root TEXT NOT NULL,
    event_count INTEGER NOT NULL,
    start_timestamp TIMESTAMP NOT NULL,
    end_timestamp TIMESTAMP NOT NULL,
    blockchain TEXT,  -- ethereum, solana, etc.
    tx_hash TEXT,  -- On-chain transaction hash
    block_number INTEGER,
    anchored_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    metadata TEXT  -- JSON: additional anchor data
);

CREATE INDEX idx_merkle_anchors_org ON merkle_anchors(org_id);
CREATE INDEX idx_merkle_anchors_root ON merkle_anchors(merkle_root);
CREATE INDEX idx_merkle_anchors_tx ON merkle_anchors(tx_hash);
CREATE INDEX idx_merkle_anchors_anchored_at ON merkle_anchors(anchored_at);

-- ============================================================================
-- ATTESTATIONS (from Trust Stack)
-- ============================================================================

CREATE TABLE IF NOT EXISTS attestations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    attestation_id TEXT UNIQUE NOT NULL,
    org_id TEXT REFERENCES organizations(id) ON DELETE CASCADE,
    model_id TEXT REFERENCES ai_models(id),
    version TEXT NOT NULL,
    attestation_type TEXT NOT NULL,  -- release, compliance, audit
    issuer TEXT NOT NULL,
    signature TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP,
    metadata TEXT  -- JSON: model card, SBOM, compliance data
);

CREATE INDEX idx_attestations_org ON attestations(org_id);
CREATE INDEX idx_attestations_model ON attestations(model_id);
CREATE INDEX idx_attestations_type ON attestations(attestation_type);
CREATE INDEX idx_attestations_created_at ON attestations(created_at);

-- ============================================================================
-- GUARDIAN ACTIONS (from Synthetic Trust)
-- ============================================================================

CREATE TABLE IF NOT EXISTS guardian_actions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    org_id TEXT REFERENCES organizations(id) ON DELETE CASCADE,
    guardian_id TEXT NOT NULL,
    action_type TEXT NOT NULL,  -- veto, pause, resume, upgrade
    target_id TEXT,  -- Proposal ID or system identifier
    reason TEXT,
    signature TEXT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    metadata TEXT  -- JSON: additional action data
);

CREATE INDEX idx_guardian_actions_org ON guardian_actions(org_id);
CREATE INDEX idx_guardian_actions_guardian ON guardian_actions(guardian_id);
CREATE INDEX idx_guardian_actions_type ON guardian_actions(action_type);
CREATE INDEX idx_guardian_actions_timestamp ON guardian_actions(timestamp);

-- ============================================================================
-- COMPLIANCE CHECKS
-- ============================================================================

CREATE TABLE IF NOT EXISTS compliance_checks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    org_id TEXT REFERENCES organizations(id) ON DELETE CASCADE,
    model_id TEXT REFERENCES ai_models(id),
    check_type TEXT NOT NULL,  -- GDPR, SOC2, AI_Act, HIPAA, etc.
    status TEXT NOT NULL,  -- passed, failed, warning
    details TEXT,
    checked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    checked_by TEXT,
    metadata TEXT  -- JSON: detailed check results
);

CREATE INDEX idx_compliance_checks_org ON compliance_checks(org_id);
CREATE INDEX idx_compliance_checks_model ON compliance_checks(model_id);
CREATE INDEX idx_compliance_checks_type ON compliance_checks(check_type);
CREATE INDEX idx_compliance_checks_status ON compliance_checks(status);
CREATE INDEX idx_compliance_checks_checked_at ON compliance_checks(checked_at);

-- ============================================================================
-- PERFORMANCE METRICS
-- ============================================================================

CREATE TABLE IF NOT EXISTS performance_metrics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    model_id TEXT REFERENCES ai_models(id) ON DELETE CASCADE,
    metric_name TEXT NOT NULL,
    metric_value REAL NOT NULL,
    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    metadata TEXT  -- JSON: additional metric context
);

CREATE INDEX idx_performance_metrics_model ON performance_metrics(model_id);
CREATE INDEX idx_performance_metrics_name ON performance_metrics(metric_name);
CREATE INDEX idx_performance_metrics_recorded_at ON performance_metrics(recorded_at);

-- ============================================================================
-- AUDIT LOGS
-- ============================================================================

CREATE TABLE IF NOT EXISTS audit_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    org_id TEXT REFERENCES organizations(id) ON DELETE CASCADE,
    user_id TEXT,
    action TEXT NOT NULL,
    resource_type TEXT,
    resource_id TEXT,
    ip_address TEXT,
    user_agent TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    metadata TEXT  -- JSON: additional audit data
);

CREATE INDEX idx_audit_logs_org ON audit_logs(org_id);
CREATE INDEX idx_audit_logs_user ON audit_logs(user_id);
CREATE INDEX idx_audit_logs_action ON audit_logs(action);
CREATE INDEX idx_audit_logs_resource ON audit_logs(resource_type, resource_id);
CREATE INDEX idx_audit_logs_timestamp ON audit_logs(timestamp);

-- ============================================================================
-- VIEWS FOR COMMON QUERIES
-- ============================================================================

-- Active proposals with vote counts
CREATE VIEW IF NOT EXISTS active_proposals AS
SELECT 
    p.*,
    s.name as proposer_name,
    s.wallet_address as proposer_wallet,
    m.name as model_name,
    m.risk_tier as model_risk_tier
FROM proposals p
LEFT JOIN stakeholders s ON p.proposer_id = s.id
LEFT JOIN ai_models m ON p.model_id = m.id
WHERE p.status = 'active'
AND datetime(p.voting_end) > datetime('now');

-- Model deployment status
CREATE VIEW IF NOT EXISTS model_deployment_status AS
SELECT 
    m.*,
    s.name as owner_name,
    o.name as org_name,
    COUNT(DISTINCT te.id) as event_count,
    AVG(te.epi_score) as avg_epi_score
FROM ai_models m
LEFT JOIN stakeholders s ON m.owner_id = s.id
LEFT JOIN organizations o ON m.org_id = o.id
LEFT JOIN trust_events te ON te.agent_id = m.name
GROUP BY m.id;

-- Stakeholder voting power
CREATE VIEW IF NOT EXISTS stakeholder_voting_summary AS
SELECT 
    s.*,
    o.name as org_name,
    COUNT(DISTINCT v.id) as total_votes,
    SUM(CASE WHEN v.vote_choice = 'for' THEN 1 ELSE 0 END) as votes_for,
    SUM(CASE WHEN v.vote_choice = 'against' THEN 1 ELSE 0 END) as votes_against
FROM stakeholders s
LEFT JOIN organizations o ON s.org_id = o.id
LEFT JOIN votes v ON s.id = v.stakeholder_id
GROUP BY s.id;

-- Trust metrics summary
CREATE VIEW IF NOT EXISTS trust_metrics_summary AS
SELECT 
    org_id,
    COUNT(*) as total_events,
    AVG(epi_score) as avg_epi_score,
    MIN(epi_score) as min_epi_score,
    MAX(epi_score) as max_epi_score,
    COUNT(DISTINCT agent_id) as unique_agents,
    DATE(timestamp) as event_date
FROM trust_events
GROUP BY org_id, DATE(timestamp);

-- ============================================================================
-- TRIGGERS FOR UPDATED_AT
-- ============================================================================

CREATE TRIGGER IF NOT EXISTS update_organizations_timestamp 
AFTER UPDATE ON organizations
BEGIN
    UPDATE organizations SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;

CREATE TRIGGER IF NOT EXISTS update_stakeholders_timestamp 
AFTER UPDATE ON stakeholders
BEGIN
    UPDATE stakeholders SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;

CREATE TRIGGER IF NOT EXISTS update_ai_models_timestamp 
AFTER UPDATE ON ai_models
BEGIN
    UPDATE ai_models SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;

CREATE TRIGGER IF NOT EXISTS update_proposals_timestamp 
AFTER UPDATE ON proposals
BEGIN
    UPDATE proposals SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;
