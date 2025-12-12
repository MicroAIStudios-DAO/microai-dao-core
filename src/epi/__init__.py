"""
Ethical Profitability Index (EPI) Module
=========================================
Core EPI calculation engine combining:
- Clean mathematical model from EPI-governance
- Rich stakeholder analysis from microai-dao
- Policy validation integration
"""

from .calculator import EPICalculator, EPIScores, EPIResult
from .trust_accumulator import TrustAccumulator

__all__ = ['EPICalculator', 'EPIScores', 'EPIResult', 'TrustAccumulator']
