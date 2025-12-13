"""
Authentication Middleware
=========================

JWT-based authentication for API endpoints.
Implements role-based access control (RBAC).
"""

from functools import wraps
from flask import request, jsonify
import os
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    get_jwt,
    verify_jwt_in_request
)
from datetime import timedelta
from typing import List, Optional, Dict
import secrets
import bcrypt


# JWT Configuration
# CRITICAL: JWT secret MUST be persistent across restarts
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
if not JWT_SECRET_KEY:
    raise ValueError(
        "JWT_SECRET_KEY environment variable must be set. "
        "Generate with: python -c 'import secrets; print(secrets.token_urlsafe(32))'"
    )
JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)


def init_jwt(app):
    """Initialize JWT manager with Flask app."""
    app.config['JWT_SECRET_KEY'] = JWT_SECRET_KEY
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = JWT_ACCESS_TOKEN_EXPIRES
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = JWT_REFRESH_TOKEN_EXPIRES
    
    jwt = JWTManager(app)
    return jwt


# bcrypt Configuration
BCRYPT_ROUNDS = int(os.getenv('BCRYPT_ROUNDS', '12'))  # 12-14 recommended for production

def hash_password(password: str) -> str:
    """Hash password using bcrypt with configured work factor."""
    salt = bcrypt.gensalt(rounds=BCRYPT_ROUNDS)
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')


def verify_password(password: str, hashed: str) -> bool:
    """Verify password against bcrypt hash."""
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))


def create_tokens(identity: str, additional_claims: dict = None):
    """Create access and refresh tokens."""
    access_token = create_access_token(
        identity=identity,
        additional_claims=additional_claims or {}
    )
    refresh_token = create_refresh_token(identity=identity)
    
    return {
        'access_token': access_token,
        'refresh_token': refresh_token,
        'token_type': 'Bearer',
        'expires_in': JWT_ACCESS_TOKEN_EXPIRES.total_seconds()
    }


def jwt_required_with_role(roles: List[str] = None):
    """
    Decorator to require JWT authentication with optional role check.
    
    Args:
        roles: List of allowed roles (e.g., ['admin', 'guardian'])
    """
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            # Verify JWT token
            verify_jwt_in_request()
            
            # Get user identity and claims
            current_user = get_jwt_identity()
            claims = get_jwt()
            
            # Check role if specified
            if roles:
                user_role = claims.get('role', 'user')
                if user_role not in roles:
                    return jsonify({
                        'error': 'Insufficient permissions',
                        'required_roles': roles,
                        'your_role': user_role
                    }), 403
            
            # Pass user info to endpoint
            kwargs['current_user'] = current_user
            kwargs['user_claims'] = claims
            
            return fn(*args, **kwargs)
        
        return wrapper
    return decorator


# Convenience decorators for common roles
def admin_required(fn):
    """Require admin role."""
    return jwt_required_with_role(['admin'])(fn)


def guardian_required(fn):
    """Require guardian role."""
    return jwt_required_with_role(['admin', 'guardian'])(fn)


def stakeholder_required(fn):
    """Require stakeholder role (any authenticated user)."""
    return jwt_required_with_role()(fn)


# Import database-backed API key manager
from .api_key_manager import get_api_key_manager

class APIKeyManager:
    """Manage API keys for programmatic access (deprecated - use DatabaseAPIKeyManager)."""
    
    def __init__(self):
        # Use database-backed manager instead
        self.db_manager = get_api_key_manager()
    
    d    def generate_key(self, user_id: str, name: str, scopes: List[str] = None, expires_in_days: Optional[int] = None) -> str:
        """Generate a new API key (database-backed)."""
        return self.db_manager.generate_key(user_id, name, scopes, expires_in_days)
    
    def verify_key(self, key: str) -> Optional[dict]:
        """Verify API key and return associated data (database-backed)."""
        return self.db_manager.verify_key(key)
    
    def revoke_key(self, key_prefix: str, user_id: str) -> bool:
        """Revoke an API key (database-backed)."""
        return self.db_manager.revoke_key(key_prefix, user_id)
    
    def list_keys(self, user_id: str) -> List[Dict]:
        """List all API keys for a user (database-backed)."""
        return self.db_manager.list_keys(user_id)

# Global API key manager
api_key_manager = APIKeyManager()


def api_key_required(scopes: List[str] = None):
    """
    Decorator to require API key authentication.
    
    Args:
        scopes: Required scopes (e.g., ['read', 'write'])
    """
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            # Get API key from header
            api_key = request.headers.get('X-API-Key')
            
            if not api_key:
                return jsonify({
                    'error': 'API key required',
                    'message': 'Provide API key in X-API-Key header'
                }), 401
            
            # Verify key
            key_data = api_key_manager.verify_key(api_key)
            
            if not key_data:
                return jsonify({
                    'error': 'Invalid API key',
                    'message': 'API key not found or revoked'
                }), 401
            
            # Check scopes if specified
            if scopes:
                key_scopes = key_data.get('scopes', [])
                if not any(scope in key_scopes for scope in scopes):
                    return jsonify({
                        'error': 'Insufficient scopes',
                        'required': scopes,
                        'available': key_scopes
                    }), 403
            
            # Pass key data to endpoint
            kwargs['api_key_data'] = key_data
            
            return fn(*args, **kwargs)
        
        return wrapper
    return decorator


def optional_auth(fn):
    """
    Decorator for endpoints that work with or without authentication.
    Provides user info if authenticated, otherwise continues.
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            verify_jwt_in_request(optional=True)
            current_user = get_jwt_identity()
            claims = get_jwt()
            
            kwargs['current_user'] = current_user
            kwargs['user_claims'] = claims
        except:
            kwargs['current_user'] = None
            kwargs['user_claims'] = {}
        
        return fn(*args, **kwargs)
    
    return wrapper
