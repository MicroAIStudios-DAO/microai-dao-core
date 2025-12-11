"""
Policy Engine Module
====================
Compliance and validation logic for governance decisions.

Features:
- Sanctions screening
- Risk assessment
- EPI threshold enforcement
- Regulatory compliance checks
"""

from .validator import PolicyValidator, ValidationResult

__all__ = ['PolicyValidator', 'ValidationResult']
