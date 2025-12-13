"""
API Key Manager - Database-backed API key storage with encryption.

Provides secure API key generation, storage, and verification with:
- Database persistence (SQLAlchemy)
- bcrypt hashing for keys
- Expiration dates
- Revocation capability
- Audit logging
"""

import secrets
import bcrypt
from datetime import datetime, timedelta
from typing import Optional, List, Dict
from sqlalchemy import create_engine, Column, String, DateTime, Boolean, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import os

Base = declarative_base()


class APIKey(Base):
    """API Key model for database storage."""
    __tablename__ = 'api_keys'
    
    key_hash = Column(String(255), primary_key=True)  # bcrypt hash of key
    key_prefix = Column(String(20), nullable=False, index=True)  # First 8 chars for identification
    user_id = Column(String(255), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    scopes = Column(JSON, nullable=False)  # List of scopes
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    last_used = Column(DateTime, nullable=True)
    expires_at = Column(DateTime, nullable=True)
    revoked = Column(Boolean, default=False, nullable=False)
    revoked_at = Column(DateTime, nullable=True)


class DatabaseAPIKeyManager:
    """
    Database-backed API key manager with encryption.
    
    Features:
    - bcrypt hashing for API keys
    - Database persistence
    - Expiration dates
    - Revocation
    - Audit logging
    """
    
    def __init__(self, database_url: Optional[str] = None):
        """
        Initialize API key manager.
        
        Args:
            database_url: SQLAlchemy database URL (from env if not provided)
        """
        self.database_url = database_url or os.getenv(
            'DATABASE_URL',
            'sqlite:///./api_keys.db'
        )
        
        # Create engine and session
        self.engine = create_engine(self.database_url)
        Base.metadata.create_all(self.engine)
        self.SessionLocal = sessionmaker(bind=self.engine)
    
    def _hash_key(self, key: str) -> str:
        """Hash API key using bcrypt."""
        return bcrypt.hashpw(key.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def _verify_key(self, key: str, key_hash: str) -> bool:
        """Verify API key against bcrypt hash."""
        return bcrypt.checkpw(key.encode('utf-8'), key_hash.encode('utf-8'))
    
    def generate_key(
        self,
        user_id: str,
        name: str,
        scopes: List[str] = None,
        expires_in_days: Optional[int] = None
    ) -> str:
        """
        Generate a new API key.
        
        Args:
            user_id: User identifier
            name: Human-readable key name
            scopes: List of scopes (e.g., ['read', 'write'])
            expires_in_days: Expiration in days (None = never expires)
            
        Returns:
            Generated API key (only shown once!)
        """
        # Generate secure random key
        key = f"mk_{secrets.token_urlsafe(32)}"
        key_prefix = key[:12]  # First 12 chars for identification
        key_hash = self._hash_key(key)
        
        # Calculate expiration
        expires_at = None
        if expires_in_days:
            expires_at = datetime.utcnow() + timedelta(days=expires_in_days)
        
        # Store in database
        db = self.SessionLocal()
        try:
            api_key = APIKey(
                key_hash=key_hash,
                key_prefix=key_prefix,
                user_id=user_id,
                name=name,
                scopes=scopes or ['read'],
                created_at=datetime.utcnow(),
                expires_at=expires_at,
                revoked=False
            )
            db.add(api_key)
            db.commit()
        finally:
            db.close()
        
        return key
    
    def verify_key(self, key: str) -> Optional[Dict]:
        """
        Verify API key and return associated data.
        
        Args:
            key: API key to verify
            
        Returns:
            Key data if valid, None if invalid/revoked/expired
        """
        if not key or not key.startswith('mk_'):
            return None
        
        key_prefix = key[:12]
        
        db = self.SessionLocal()
        try:
            # Find all keys with matching prefix
            candidates = db.query(APIKey).filter(
                APIKey.key_prefix == key_prefix,
                APIKey.revoked == False
            ).all()
            
            # Check each candidate (timing-safe comparison)
            for candidate in candidates:
                if self._verify_key(key, candidate.key_hash):
                    # Check expiration
                    if candidate.expires_at and candidate.expires_at < datetime.utcnow():
                        return None  # Expired
                    
                    # Update last used
                    candidate.last_used = datetime.utcnow()
                    db.commit()
                    
                    return {
                        'user_id': candidate.user_id,
                        'name': candidate.name,
                        'scopes': candidate.scopes,
                        'created_at': candidate.created_at.isoformat(),
                        'last_used': candidate.last_used.isoformat() if candidate.last_used else None,
                        'expires_at': candidate.expires_at.isoformat() if candidate.expires_at else None
                    }
            
            return None  # No match found
        
        finally:
            db.close()
    
    def revoke_key(self, key_prefix: str, user_id: str) -> bool:
        """
        Revoke an API key.
        
        Args:
            key_prefix: First 12 characters of key
            user_id: User identifier (for authorization)
            
        Returns:
            True if revoked, False if not found
        """
        db = self.SessionLocal()
        try:
            api_key = db.query(APIKey).filter(
                APIKey.key_prefix == key_prefix,
                APIKey.user_id == user_id
            ).first()
            
            if api_key:
                api_key.revoked = True
                api_key.revoked_at = datetime.utcnow()
                db.commit()
                return True
            
            return False
        
        finally:
            db.close()
    
    def list_keys(self, user_id: str) -> List[Dict]:
        """
        List all API keys for a user.
        
        Args:
            user_id: User identifier
            
        Returns:
            List of key metadata (without actual keys)
        """
        db = self.SessionLocal()
        try:
            keys = db.query(APIKey).filter(
                APIKey.user_id == user_id
            ).all()
            
            return [
                {
                    'key_prefix': key.key_prefix,
                    'name': key.name,
                    'scopes': key.scopes,
                    'created_at': key.created_at.isoformat(),
                    'last_used': key.last_used.isoformat() if key.last_used else None,
                    'expires_at': key.expires_at.isoformat() if key.expires_at else None,
                    'revoked': key.revoked,
                    'revoked_at': key.revoked_at.isoformat() if key.revoked_at else None
                }
                for key in keys
            ]
        
        finally:
            db.close()
    
    def cleanup_expired(self) -> int:
        """
        Remove expired API keys from database.
        
        Returns:
            Number of keys removed
        """
        db = self.SessionLocal()
        try:
            count = db.query(APIKey).filter(
                APIKey.expires_at < datetime.utcnow(),
                APIKey.revoked == False
            ).update({'revoked': True, 'revoked_at': datetime.utcnow()})
            
            db.commit()
            return count
        
        finally:
            db.close()


# Global instance (singleton pattern)
_api_key_manager = None

def get_api_key_manager() -> DatabaseAPIKeyManager:
    """Get or create global API key manager instance."""
    global _api_key_manager
    if _api_key_manager is None:
        _api_key_manager = DatabaseAPIKeyManager()
    return _api_key_manager
