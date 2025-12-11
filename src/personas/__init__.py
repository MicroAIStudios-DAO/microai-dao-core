"""
AI Personas Module
==================
Executive AI agents for governance and mentorship.

Personas:
- StrategicCatalyst: Executive mentor for founders
- ExecAIVoter: Autonomous voting agent (51% stake)
- (Future) CEOAgent, CFOAgent, CTOAgent
"""

from .strategic_catalyst import StrategicCatalyst
from .execai_voter import ExecAIVoter

__all__ = ['StrategicCatalyst', 'ExecAIVoter']
