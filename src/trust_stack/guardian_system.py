"""
Guardian Oversight System
=========================

Implements guardian controls from synthetic_trust.md:
- Veto power for Class A stakeholders
- Emergency pause functionality
- Upgrade authority
- Dispute resolution

Guardians provide the human safety net for AI governance.
"""

from typing import List, Optional, Dict
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class GuardianAction(Enum):
    """Types of guardian actions."""
    VETO = "veto"
    APPROVE = "approve"
    PAUSE = "pause"
    RESUME = "resume"
    UPGRADE = "upgrade"
    DISPUTE_RESOLUTION = "dispute_resolution"


class GuardianRole(Enum):
    """Guardian role levels."""
    CLASS_A = "class_a"  # Full authority
    CLASS_B = "class_b"  # Limited authority
    OBSERVER = "observer"  # View only


@dataclass
class Guardian:
    """Guardian stakeholder."""
    guardian_id: str
    name: str
    role: GuardianRole
    public_key: str
    added_date: datetime
    active: bool = True
    veto_count: int = 0
    last_action_date: Optional[datetime] = None


@dataclass
class GuardianAction:
    """Record of guardian action."""
    action_id: str
    guardian_id: str
    action_type: GuardianAction
    target_id: str  # Proposal/decision ID
    reason: str
    timestamp: datetime
    signature: str
    metadata: Dict = field(default_factory=dict)


@dataclass
class SystemState:
    """Current system state."""
    is_paused: bool = False
    pause_reason: Optional[str] = None
    paused_by: Optional[str] = None
    paused_at: Optional[datetime] = None
    total_proposals: int = 0
    total_vetoes: int = 0
    total_approvals: int = 0


class GuardianSystem:
    """
    Guardian oversight system for AI governance.
    
    Provides:
    - Veto power for proposals
    - Emergency pause/resume
    - Upgrade authority
    - Dispute resolution
    """
    
    def __init__(self):
        """Initialize guardian system."""
        self.guardians: Dict[str, Guardian] = {}
        self.actions: List[GuardianAction] = []
        self.state = SystemState()
        self.veto_threshold = 1  # Number of guardians needed to veto
        self.upgrade_threshold = 2  # Number needed for upgrades
    
    def add_guardian(
        self,
        guardian_id: str,
        name: str,
        role: GuardianRole,
        public_key: str
    ) -> Guardian:
        """
        Add a new guardian to the system.
        
        Args:
            guardian_id: Unique guardian identifier
            name: Guardian name
            role: Guardian role level
            public_key: Public key for signature verification
            
        Returns:
            Guardian object
        """
        guardian = Guardian(
            guardian_id=guardian_id,
            name=name,
            role=role,
            public_key=public_key,
            added_date=datetime.now()
        )
        
        self.guardians[guardian_id] = guardian
        return guardian
    
    def veto_proposal(
        self,
        guardian_id: str,
        proposal_id: str,
        reason: str,
        signature: str
    ) -> Dict:
        """
        Veto a proposal.
        
        Args:
            guardian_id: Guardian performing veto
            proposal_id: Proposal to veto
            reason: Reason for veto
            signature: Cryptographic signature
            
        Returns:
            Result dictionary with veto status
        """
        # Verify guardian exists and has authority
        if guardian_id not in self.guardians:
            return {
                'success': False,
                'error': 'Guardian not found'
            }
        
        guardian = self.guardians[guardian_id]
        
        if not guardian.active:
            return {
                'success': False,
                'error': 'Guardian is not active'
            }
        
        if guardian.role == GuardianRole.OBSERVER:
            return {
                'success': False,
                'error': 'Observers cannot veto proposals'
            }
        
        # Check if system is paused
        if self.state.is_paused:
            return {
                'success': False,
                'error': 'System is paused'
            }
        
        # Record veto action
        action = GuardianAction(
            action_id=f"veto_{len(self.actions)}",
            guardian_id=guardian_id,
            action_type=GuardianAction.VETO,
            target_id=proposal_id,
            reason=reason,
            timestamp=datetime.now(),
            signature=signature
        )
        
        self.actions.append(action)
        guardian.veto_count += 1
        guardian.last_action_date = datetime.now()
        self.state.total_vetoes += 1
        
        return {
            'success': True,
            'action_id': action.action_id,
            'guardian': guardian.name,
            'proposal_id': proposal_id,
            'reason': reason,
            'timestamp': action.timestamp.isoformat()
        }
    
    def emergency_pause(
        self,
        guardian_id: str,
        reason: str,
        signature: str
    ) -> Dict:
        """
        Pause the system in case of emergency.
        
        Args:
            guardian_id: Guardian performing pause
            reason: Reason for emergency pause
            signature: Cryptographic signature
            
        Returns:
            Result dictionary with pause status
        """
        # Verify guardian has Class A authority
        if guardian_id not in self.guardians:
            return {
                'success': False,
                'error': 'Guardian not found'
            }
        
        guardian = self.guardians[guardian_id]
        
        if guardian.role != GuardianRole.CLASS_A:
            return {
                'success': False,
                'error': 'Only Class A guardians can pause the system'
            }
        
        if self.state.is_paused:
            return {
                'success': False,
                'error': 'System is already paused'
            }
        
        # Pause the system
        self.state.is_paused = True
        self.state.pause_reason = reason
        self.state.paused_by = guardian_id
        self.state.paused_at = datetime.now()
        
        # Record action
        action = GuardianAction(
            action_id=f"pause_{len(self.actions)}",
            guardian_id=guardian_id,
            action_type=GuardianAction.PAUSE,
            target_id="system",
            reason=reason,
            timestamp=datetime.now(),
            signature=signature
        )
        
        self.actions.append(action)
        guardian.last_action_date = datetime.now()
        
        return {
            'success': True,
            'action_id': action.action_id,
            'guardian': guardian.name,
            'reason': reason,
            'timestamp': action.timestamp.isoformat(),
            'message': 'System paused successfully'
        }
    
    def resume_system(
        self,
        guardian_id: str,
        signature: str
    ) -> Dict:
        """
        Resume the system after emergency pause.
        
        Args:
            guardian_id: Guardian performing resume
            signature: Cryptographic signature
            
        Returns:
            Result dictionary with resume status
        """
        # Verify guardian has Class A authority
        if guardian_id not in self.guardians:
            return {
                'success': False,
                'error': 'Guardian not found'
            }
        
        guardian = self.guardians[guardian_id]
        
        if guardian.role != GuardianRole.CLASS_A:
            return {
                'success': False,
                'error': 'Only Class A guardians can resume the system'
            }
        
        if not self.state.is_paused:
            return {
                'success': False,
                'error': 'System is not paused'
            }
        
        # Resume the system
        pause_duration = (datetime.now() - self.state.paused_at).total_seconds() / 3600
        
        self.state.is_paused = False
        self.state.pause_reason = None
        self.state.paused_by = None
        self.state.paused_at = None
        
        # Record action
        action = GuardianAction(
            action_id=f"resume_{len(self.actions)}",
            guardian_id=guardian_id,
            action_type=GuardianAction.RESUME,
            target_id="system",
            reason="System resumed",
            timestamp=datetime.now(),
            signature=signature,
            metadata={'pause_duration_hours': pause_duration}
        )
        
        self.actions.append(action)
        guardian.last_action_date = datetime.now()
        
        return {
            'success': True,
            'action_id': action.action_id,
            'guardian': guardian.name,
            'pause_duration_hours': pause_duration,
            'timestamp': action.timestamp.isoformat(),
            'message': 'System resumed successfully'
        }
    
    def get_guardian_stats(self, guardian_id: str) -> Optional[Dict]:
        """
        Get statistics for a guardian.
        
        Args:
            guardian_id: Guardian identifier
            
        Returns:
            Dictionary with guardian statistics or None
        """
        if guardian_id not in self.guardians:
            return None
        
        guardian = self.guardians[guardian_id]
        
        # Count actions by type
        guardian_actions = [a for a in self.actions if a.guardian_id == guardian_id]
        action_counts = {}
        for action in guardian_actions:
            action_type = action.action_type.value
            action_counts[action_type] = action_counts.get(action_type, 0) + 1
        
        return {
            'guardian_id': guardian_id,
            'name': guardian.name,
            'role': guardian.role.value,
            'active': guardian.active,
            'added_date': guardian.added_date.isoformat(),
            'veto_count': guardian.veto_count,
            'total_actions': len(guardian_actions),
            'action_breakdown': action_counts,
            'last_action_date': guardian.last_action_date.isoformat() if guardian.last_action_date else None
        }
    
    def get_system_status(self) -> Dict:
        """
        Get current system status.
        
        Returns:
            Dictionary with system status
        """
        active_guardians = sum(1 for g in self.guardians.values() if g.active)
        class_a_guardians = sum(1 for g in self.guardians.values() if g.active and g.role == GuardianRole.CLASS_A)
        
        return {
            'is_paused': self.state.is_paused,
            'pause_reason': self.state.pause_reason,
            'paused_by': self.state.paused_by,
            'paused_at': self.state.paused_at.isoformat() if self.state.paused_at else None,
            'total_guardians': len(self.guardians),
            'active_guardians': active_guardians,
            'class_a_guardians': class_a_guardians,
            'total_proposals': self.state.total_proposals,
            'total_vetoes': self.state.total_vetoes,
            'total_approvals': self.state.total_approvals,
            'veto_rate': self.state.total_vetoes / self.state.total_proposals if self.state.total_proposals > 0 else 0,
            'total_actions': len(self.actions)
        }
    
    def get_recent_actions(self, limit: int = 10) -> List[Dict]:
        """
        Get recent guardian actions.
        
        Args:
            limit: Maximum number of actions to return
            
        Returns:
            List of recent actions
        """
        recent = self.actions[-limit:] if len(self.actions) > limit else self.actions
        
        return [
            {
                'action_id': action.action_id,
                'guardian_id': action.guardian_id,
                'guardian_name': self.guardians[action.guardian_id].name if action.guardian_id in self.guardians else 'Unknown',
                'action_type': action.action_type.value,
                'target_id': action.target_id,
                'reason': action.reason,
                'timestamp': action.timestamp.isoformat()
            }
            for action in reversed(recent)
        ]


# Example usage
if __name__ == "__main__":
    # Initialize guardian system
    system = GuardianSystem()
    
    # Add guardians
    guardian1 = system.add_guardian(
        guardian_id="guardian_001",
        name="Alice (Founder)",
        role=GuardianRole.CLASS_A,
        public_key="0x1234..."
    )
    
    guardian2 = system.add_guardian(
        guardian_id="guardian_002",
        name="Bob (Advisor)",
        role=GuardianRole.CLASS_B,
        public_key="0x5678..."
    )
    
    print("Guardians added:")
    print(f"  {guardian1.name} - {guardian1.role.value}")
    print(f"  {guardian2.name} - {guardian2.role.value}")
    print()
    
    # Veto a proposal
    result = system.veto_proposal(
        guardian_id="guardian_001",
        proposal_id="prop_123",
        reason="EPI score too low, ethical concerns",
        signature="sig_abc"
    )
    
    print("Veto result:")
    print(f"  Success: {result['success']}")
    if result['success']:
        print(f"  Guardian: {result['guardian']}")
        print(f"  Reason: {result['reason']}")
    print()
    
    # Get system status
    status = system.get_system_status()
    print("System status:")
    print(f"  Paused: {status['is_paused']}")
    print(f"  Active guardians: {status['active_guardians']}")
    print(f"  Total vetoes: {status['total_vetoes']}")
    print(f"  Veto rate: {status['veto_rate']:.1%}")
