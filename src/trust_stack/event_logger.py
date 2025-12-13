"""
Event Logger - Cryptographic event logging for AI decisions.

Provides tamper-evident, append-only logging with HMAC signatures
and SHA-256 hashing for all AI agent decisions and governance actions.
"""

import hashlib
import hmac
import json
import uuid
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from pathlib import Path
import os


@dataclass
class Evaluation:
    """Single evaluation result from a policy evaluator."""
    evaluator: str
    category: str  # PII, Safety, Bias, Copyright, Jailbreak
    result: str  # pass, fail, redacted
    confidence: float  # 0.0 to 1.0
    signed_at: str
    signature: str


@dataclass
class TrustEvent:
    """Tamper-evident event log entry."""
    event_id: str
    timestamp: str
    tenant_id: str
    agent_id: str  # CEO-AI, CFO-AI, EXECAI, etc.
    action_type: str  # proposal, payment, vote, decision
    model: Optional[str]
    input_hash: str
    output_hash: str
    policy_version: str
    epi_score: Optional[float]
    tools_called: List[str]
    redactions: List[str]
    evaluations: List[Dict[str, Any]]
    signature: str
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization."""
        return asdict(self)
    
    def to_json(self) -> str:
        """Convert to JSON string."""
        return json.dumps(self.to_dict(), indent=2)


class EventLogger:
    """
    Cryptographic event logger for AI governance decisions.
    
    Features:
    - SHA-256 hashing of inputs/outputs
    - HMAC-SHA256 signing with secret key
    - Append-only event storage
    - Policy evaluation integration
    - EPI score tracking
    """
    
    def __init__(self, signing_key: Optional[str] = None, storage_path: Optional[str] = None):
        """
        Initialize the event logger.
        
        Args:
            signing_key: Secret key for HMAC signing (from env if not provided)
            storage_path: Path to store event logs (default: ./logs/trust_events/)
        """
        # CRITICAL: Signing key MUST be provided - no defaults allowed
        self.signing_key = signing_key or os.getenv('TRUST_SIGNING_KEY')
        if not self.signing_key:
            raise ValueError(
                "TRUST_SIGNING_KEY must be set - no default allowed. "
                "Generate with: python -c 'import secrets; print(secrets.token_urlsafe(32))'"
            )
        if self.signing_key == 'default-dev-key-change-in-prod':
            raise ValueError("Default signing key detected - must use secure key")
        self.storage_path = Path(storage_path or './logs/trust_events')
        self.storage_path.mkdir(parents=True, exist_ok=True)
    
    def hash_data(self, data: str) -> str:
        """
        Generate SHA-256 hash of data.
        
        Args:
            data: String data to hash
            
        Returns:
            Hex-encoded SHA-256 hash
        """
        return hashlib.sha256(data.encode('utf-8')).hexdigest()
    
    def sign_data(self, data: str) -> str:
        """
        Generate HMAC-SHA256 signature of data.
        
        Args:
            data: String data to sign
            
        Returns:
            Hex-encoded HMAC signature
        """
        return hmac.new(
            self.signing_key.encode('utf-8'),
            data.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
    
    def create_evaluation(
        self,
        evaluator: str,
        category: str,
        result: str,
        confidence: float
    ) -> Dict[str, Any]:
        """
        Create a signed evaluation record.
        
        Args:
            evaluator: Name of the evaluator (e.g., 'pii-scanner', 'safety-check')
            category: Category of evaluation
            result: Evaluation result
            confidence: Confidence score 0.0-1.0
            
        Returns:
            Signed evaluation dictionary
        """
        signed_at = datetime.utcnow().isoformat() + 'Z'
        eval_data = f"{evaluator}:{category}:{result}:{confidence}:{signed_at}"
        signature = self.sign_data(eval_data)
        
        return {
            'evaluator': evaluator,
            'category': category,
            'result': result,
            'confidence': confidence,
            'signed_at': signed_at,
            'signature': signature
        }
    
    def log_event(
        self,
        tenant_id: str,
        agent_id: str,
        action_type: str,
        input_data: str,
        output_data: str,
        policy_version: str,
        epi_score: Optional[float] = None,
        model: Optional[str] = None,
        tools_called: Optional[List[str]] = None,
        redactions: Optional[List[str]] = None,
        evaluations: Optional[List[Dict[str, Any]]] = None
    ) -> TrustEvent:
        """
        Log an AI governance event with cryptographic signature.
        
        Args:
            tenant_id: Tenant/organization identifier
            agent_id: AI agent identifier (CEO-AI, CFO-AI, etc.)
            action_type: Type of action (proposal, payment, vote, etc.)
            input_data: Input data (will be hashed)
            output_data: Output data (will be hashed)
            policy_version: Version of policy applied
            epi_score: Ethical Profitability Index score
            model: Model used (if applicable)
            tools_called: List of tools/functions called
            redactions: List of redacted fields
            evaluations: List of evaluation results
            
        Returns:
            Signed TrustEvent
        """
        # Generate unique event ID
        event_id = str(uuid.uuid4())
        timestamp = datetime.utcnow().isoformat() + 'Z'
        
        # Hash inputs and outputs
        input_hash = self.hash_data(input_data)
        output_hash = self.hash_data(output_data)
        
        # Prepare event data for signing
        event_data = {
            'event_id': event_id,
            'timestamp': timestamp,
            'tenant_id': tenant_id,
            'agent_id': agent_id,
            'action_type': action_type,
            'input_hash': input_hash,
            'output_hash': output_hash,
            'policy_version': policy_version,
            'epi_score': epi_score,
            'tools_called': tools_called or [],
            'redactions': redactions or [],
            'evaluations': evaluations or []
        }
        
        # Sign the event
        sign_payload = json.dumps(event_data, sort_keys=True)
        signature = self.sign_data(sign_payload)
        
        # Create TrustEvent
        event = TrustEvent(
            event_id=event_id,
            timestamp=timestamp,
            tenant_id=tenant_id,
            agent_id=agent_id,
            action_type=action_type,
            model=model,
            input_hash=input_hash,
            output_hash=output_hash,
            policy_version=policy_version,
            epi_score=epi_score,
            tools_called=tools_called or [],
            redactions=redactions or [],
            evaluations=evaluations or [],
            signature=signature
        )
        
        # Store event
        self._store_event(event)
        
        return event
    
    def _store_event(self, event: TrustEvent) -> None:
        """
        Store event to disk (append-only).
        
        Args:
            event: TrustEvent to store
        """
        # Store by date for easy retrieval
        date_str = event.timestamp[:10]  # YYYY-MM-DD
        date_dir = self.storage_path / date_str
        date_dir.mkdir(exist_ok=True)
        
        # Store individual event file
        event_file = date_dir / f"{event.event_id}.json"
        with open(event_file, 'w') as f:
            f.write(event.to_json())
        
        # Append to daily log
        daily_log = date_dir / 'events.jsonl'
        with open(daily_log, 'a') as f:
            f.write(event.to_json() + '\n')
    
    def get_event(self, event_id: str) -> Optional[TrustEvent]:
        """
        Retrieve an event by ID.
        
        Args:
            event_id: Event UUID
            
        Returns:
            TrustEvent if found, None otherwise
        """
        # Search through date directories
        for date_dir in self.storage_path.iterdir():
            if not date_dir.is_dir():
                continue
            
            event_file = date_dir / f"{event_id}.json"
            if event_file.exists():
                with open(event_file, 'r') as f:
                    data = json.load(f)
                    return TrustEvent(**data)
        
        return None
    
    def get_events_by_date(self, date: str) -> List[TrustEvent]:
        """
        Retrieve all events for a specific date.
        
        Args:
            date: Date string (YYYY-MM-DD)
            
        Returns:
            List of TrustEvents
        """
        events = []
        date_dir = self.storage_path / date
        
        if not date_dir.exists():
            return events
        
        daily_log = date_dir / 'events.jsonl'
        if daily_log.exists():
            with open(daily_log, 'r') as f:
                for line in f:
                    if line.strip():
                        data = json.loads(line)
                        events.append(TrustEvent(**data))
        
        return events
    
    def get_events_by_agent(self, agent_id: str, limit: int = 100) -> List[TrustEvent]:
        """
        Retrieve recent events for a specific agent.
        
        Args:
            agent_id: Agent identifier
            limit: Maximum number of events to return
            
        Returns:
            List of TrustEvents
        """
        events = []
        
        # Search through date directories (newest first)
        date_dirs = sorted(self.storage_path.iterdir(), reverse=True)
        
        for date_dir in date_dirs:
            if not date_dir.is_dir():
                continue
            
            daily_log = date_dir / 'events.jsonl'
            if daily_log.exists():
                with open(daily_log, 'r') as f:
                    for line in f:
                        if line.strip():
                            data = json.loads(line)
                            if data['agent_id'] == agent_id:
                                events.append(TrustEvent(**data))
                                
                                if len(events) >= limit:
                                    return events
        
        return events
    
    def verify_event(self, event: TrustEvent) -> bool:
        """
        Verify the cryptographic signature of an event.
        
        Args:
            event: TrustEvent to verify
            
        Returns:
            True if signature is valid, False otherwise
        """
        # Reconstruct signing payload
        event_data = {
            'event_id': event.event_id,
            'timestamp': event.timestamp,
            'tenant_id': event.tenant_id,
            'agent_id': event.agent_id,
            'action_type': event.action_type,
            'input_hash': event.input_hash,
            'output_hash': event.output_hash,
            'policy_version': event.policy_version,
            'epi_score': event.epi_score,
            'tools_called': event.tools_called,
            'redactions': event.redactions,
            'evaluations': event.evaluations
        }
        
        sign_payload = json.dumps(event_data, sort_keys=True)
        expected_signature = self.sign_data(sign_payload)
        
        return hmac.compare_digest(expected_signature, event.signature)
    
    def get_daily_hashes(self, date: str) -> List[str]:
        """
        Get all event hashes for a specific date (for Merkle tree).
        
        Args:
            date: Date string (YYYY-MM-DD)
            
        Returns:
            List of event hashes (input_hash + output_hash combined)
        """
        events = self.get_events_by_date(date)
        return [self.hash_data(e.input_hash + e.output_hash) for e in events]


# Example usage
if __name__ == "__main__":
    logger = EventLogger()
    
    # Log a CEO-AI strategic proposal
    event = logger.log_event(
        tenant_id="microai-dao",
        agent_id="CEO-AI",
        action_type="strategic_proposal",
        input_data="Propose investment in healthcare AI sector",
        output_data="Investment approved: $500,000 in healthcare AI with 18-month timeline",
        policy_version="v1.0.0",
        epi_score=0.85,
        model="gpt-4",
        tools_called=["epi_calculator", "market_analyzer"],
        evaluations=[
            logger.create_evaluation("epi-validator", "Ethics", "pass", 0.92),
            logger.create_evaluation("compliance-check", "Safety", "pass", 0.95)
        ]
    )
    
    print("Event logged:")
    print(event.to_json())
    
    # Verify event
    is_valid = logger.verify_event(event)
    print(f"\nEvent signature valid: {is_valid}")
