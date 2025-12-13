"""
Security Middleware
===================

Rate limiting, security headers, input validation, and CORS configuration.
"""

from flask import request, jsonify
from functools import wraps
from collections import defaultdict
from datetime import datetime, timedelta
import re
from typing import Dict, Any, List


class RateLimiter:
    """
    Token bucket rate limiter.
    
    Limits requests per IP address or API key.
    """
    
    def __init__(self, requests_per_minute: int = 60, requests_per_hour: int = 1000):
        """
        Initialize rate limiter.
        
        Args:
            requests_per_minute: Max requests per minute
            requests_per_hour: Max requests per hour
        """
        self.rpm_limit = requests_per_minute
        self.rph_limit = requests_per_hour
        
        # Store request timestamps per identifier
        self.requests = defaultdict(list)
    
    def is_allowed(self, identifier: str) -> tuple[bool, dict]:
        """
        Check if request is allowed.
        
        Args:
            identifier: IP address or API key
        
        Returns:
            (allowed, info) tuple
        """
        now = datetime.now()
        
        # Get request history for this identifier
        timestamps = self.requests[identifier]
        
        # Remove old timestamps (older than 1 hour)
        cutoff_hour = now - timedelta(hours=1)
        timestamps = [ts for ts in timestamps if ts > cutoff_hour]
        
        # Count recent requests
        cutoff_minute = now - timedelta(minutes=1)
        requests_last_minute = sum(1 for ts in timestamps if ts > cutoff_minute)
        requests_last_hour = len(timestamps)
        
        # Check limits
        if requests_last_minute >= self.rpm_limit:
            return False, {
                'limit': self.rpm_limit,
                'window': '1 minute',
                'retry_after': 60
            }
        
        if requests_last_hour >= self.rph_limit:
            return False, {
                'limit': self.rph_limit,
                'window': '1 hour',
                'retry_after': 3600
            }
        
        # Add current request
        timestamps.append(now)
        self.requests[identifier] = timestamps
        
        return True, {
            'remaining_minute': self.rpm_limit - requests_last_minute - 1,
            'remaining_hour': self.rph_limit - requests_last_hour - 1
        }


# Global rate limiter
rate_limiter = RateLimiter()


def rate_limit(requests_per_minute: int = 60, requests_per_hour: int = 1000):
    """
    Decorator to apply rate limiting to endpoints.
    
    Args:
        requests_per_minute: Max requests per minute
        requests_per_hour: Max requests per hour
    """
    limiter = RateLimiter(requests_per_minute, requests_per_hour)
    
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            # Get identifier (IP or API key)
            identifier = request.headers.get('X-API-Key') or request.remote_addr
            
            # Check rate limit
            allowed, info = limiter.is_allowed(identifier)
            
            if not allowed:
                response = jsonify({
                    'error': 'Rate limit exceeded',
                    'limit': info['limit'],
                    'window': info['window'],
                    'retry_after': info['retry_after']
                })
                response.status_code = 429
                response.headers['Retry-After'] = str(info['retry_after'])
                return response
            
            # Add rate limit headers
            response = fn(*args, **kwargs)
            
            if hasattr(response, 'headers'):
                response.headers['X-RateLimit-Remaining-Minute'] = str(info['remaining_minute'])
                response.headers['X-RateLimit-Remaining-Hour'] = str(info['remaining_hour'])
            
            return response
        
        return wrapper
    return decorator


def add_security_headers(response):
    """Add security headers to response."""
    # Prevent clickjacking
    response.headers['X-Frame-Options'] = 'DENY'
    
    # Prevent MIME sniffing
    response.headers['X-Content-Type-Options'] = 'nosniff'
    
    # Enable XSS protection
    response.headers['X-XSS-Protection'] = '1; mode=block'
    
    # Content Security Policy
    response.headers['Content-Security-Policy'] = (
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline'; "
        "style-src 'self' 'unsafe-inline'; "
        "img-src 'self' data: https:; "
        "font-src 'self' data:; "
        "connect-src 'self'"
    )
    
    # Strict Transport Security (HTTPS only)
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    
    # Referrer Policy
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    
    # Permissions Policy
    response.headers['Permissions-Policy'] = 'geolocation=(), microphone=(), camera=()'
    
    return response


def configure_cors(app):
    """Configure CORS for the Flask app."""
    from flask_cors import CORS
    
    CORS(app, resources={
        r"/api/*": {
            "origins": ["http://localhost:3000", "http://localhost:5173"],  # Frontend URLs
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization", "X-API-Key"],
            "expose_headers": ["X-RateLimit-Remaining-Minute", "X-RateLimit-Remaining-Hour"],
            "supports_credentials": True,
            "max_age": 3600
        }
    })


class InputValidator:
    """Validate and sanitize input data."""
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """Validate email format."""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    @staticmethod
    def validate_wallet_address(address: str, chain: str = 'ethereum') -> bool:
        """Validate blockchain wallet address."""
        if chain == 'ethereum':
            # Ethereum address: 0x followed by 40 hex characters
            pattern = r'^0x[a-fA-F0-9]{40}$'
            return re.match(pattern, address) is not None
        elif chain == 'solana':
            # Solana address: 32-44 base58 characters
            pattern = r'^[1-9A-HJ-NP-Za-km-z]{32,44}$'
            return re.match(pattern, address) is not None
        return False
    
    @staticmethod
    def sanitize_string(text: str, max_length: int = 1000) -> str:
        """Sanitize string input."""
        # Remove null bytes
        text = text.replace('\x00', '')
        
        # Trim to max length
        text = text[:max_length]
        
        # Remove leading/trailing whitespace
        text = text.strip()
        
        return text
    
    @staticmethod
    def validate_json_schema(data: dict, schema: dict) -> tuple[bool, list]:
        """
        Validate JSON data against schema.
        
        Args:
            data: Input data
            schema: Schema definition
        
        Returns:
            (valid, errors) tuple
        """
        errors = []
        
        # Check required fields
        required = schema.get('required', [])
        for field in required:
            if field not in data:
                errors.append(f"Missing required field: {field}")
        
        # Check field types
        properties = schema.get('properties', {})
        for field, value in data.items():
            if field in properties:
                expected_type = properties[field].get('type')
                
                if expected_type == 'string' and not isinstance(value, str):
                    errors.append(f"Field '{field}' must be a string")
                elif expected_type == 'number' and not isinstance(value, (int, float)):
                    errors.append(f"Field '{field}' must be a number")
                elif expected_type == 'boolean' and not isinstance(value, bool):
                    errors.append(f"Field '{field}' must be a boolean")
                elif expected_type == 'array' and not isinstance(value, list):
                    errors.append(f"Field '{field}' must be an array")
                elif expected_type == 'object' and not isinstance(value, dict):
                    errors.append(f"Field '{field}' must be an object")
        
        return len(errors) == 0, errors


def validate_input(schema: dict):
    """
    Decorator to validate request JSON against schema.
    
    Args:
        schema: JSON schema definition
    """
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            # Get JSON data
            data = request.get_json(silent=True)
            
            if data is None:
                return jsonify({
                    'error': 'Invalid JSON',
                    'message': 'Request body must be valid JSON'
                }), 400
            
            # Validate against schema
            validator = InputValidator()
            valid, errors = validator.validate_json_schema(data, schema)
            
            if not valid:
                return jsonify({
                    'error': 'Validation failed',
                    'errors': errors
                }), 400
            
            # Pass validated data to endpoint
            kwargs['validated_data'] = data
            
            return fn(*args, **kwargs)
        
        return wrapper
    return decorator


# Common validation schemas
SCHEMAS = {
    'login': {
        'required': ['email', 'password'],
        'properties': {
            'email': {'type': 'string'},
            'password': {'type': 'string'}
        }
    },
    'register': {
        'required': ['email', 'password', 'wallet_address'],
        'properties': {
            'email': {'type': 'string'},
            'password': {'type': 'string'},
            'wallet_address': {'type': 'string'},
            'name': {'type': 'string'}
        }
    },
    'proposal': {
        'required': ['title', 'description', 'proposal_type'],
        'properties': {
            'title': {'type': 'string'},
            'description': {'type': 'string'},
            'proposal_type': {'type': 'string'},
            'model_id': {'type': 'string'}
        }
    },
    'vote': {
        'required': ['proposal_id', 'vote_choice'],
        'properties': {
            'proposal_id': {'type': 'string'},
            'vote_choice': {'type': 'string'},
            'reasoning': {'type': 'string'}
        }
    },
    'model_register': {
        'required': ['name', 'model_type', 'description', 'use_case'],
        'properties': {
            'name': {'type': 'string'},
            'model_type': {'type': 'string'},
            'description': {'type': 'string'},
            'use_case': {'type': 'string'},
            'risk_tier': {'type': 'number'},
            'tags': {'type': 'array'}
        }
    }
}


def init_security_middleware(app):
    """Initialize all security middleware."""
    # Add security headers to all responses
    @app.after_request
    def apply_security_headers(response):
        return add_security_headers(response)
    
    # Configure CORS
    configure_cors(app)
    
    # Add request logging
    @app.before_request
    def log_request():
        app.logger.info(f"{request.method} {request.path} from {request.remote_addr}")
    
    return app
