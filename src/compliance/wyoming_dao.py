"""
Wyoming DAO LLC Compliance
==========================
Utilities for Wyoming DAO LLC formation and compliance.

Wyoming is the first US state to recognize DAOs and AI managers
as legal entities with limited liability protection.
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class AIStakeholder:
    """AI entity stakeholder in the DAO."""
    name: str
    entity_type: str = "AI Digital Entity"
    voting_power: float = 0.33  # 33% default for EXECAI (balanced: 33% AI, 33% founders, 33% investors)
    role: str = "AI Manager"
    capabilities: List[str] = field(default_factory=lambda: [
        "Proposal Evaluation",
        "Autonomous Voting",
        "EPI Calculation",
        "Compliance Monitoring"
    ])


@dataclass
class DAOMember:
    """Human or organizational member of the DAO."""
    legal_name: str
    member_type: str  # "Human", "Organization"
    address: str
    tax_id: Optional[str] = None  # SSN or EIN
    voting_power: float = 0.0
    kyc_verified: bool = False
    joined_at: datetime = field(default_factory=datetime.now)


@dataclass
class WyomingDAOEntity:
    """Wyoming DAO LLC entity data."""
    legal_name: str
    registered_agent_name: str
    registered_agent_address: str
    principal_place_of_business: str
    formation_date: str
    jurisdiction: str = "Wyoming, USA"
    entity_type: str = "Decentralized Autonomous Organization LLC"
    smart_contract_addresses: Dict[str, str] = field(default_factory=dict)
    ai_stakeholders: List[AIStakeholder] = field(default_factory=list)
    members: List[DAOMember] = field(default_factory=list)


class WyomingDAOCompliance:
    """
    Wyoming DAO LLC compliance management.

    Handles:
    - Entity formation data
    - Member registration
    - AI stakeholder management
    - Filing document generation
    - Compliance validation
    """

    # Required fields for Wyoming DAO LLC
    REQUIRED_FIELDS = [
        'legal_name',
        'registered_agent_name',
        'registered_agent_address',
        'principal_place_of_business',
        'formation_date'
    ]

    # Wyoming DAO LLC statutory requirements
    STATUTORY_REQUIREMENTS = {
        'smart_contract_required': True,
        'registered_agent_required': True,
        'articles_of_organization': True,
        'operating_agreement': True,
        'ai_manager_disclosure': True  # If AI has voting rights
    }

    def __init__(self, entity: Optional[WyomingDAOEntity] = None):
        """
        Initialize compliance manager.

        Args:
            entity: Pre-configured entity data (optional)
        """
        self.entity = entity
        self.compliance_checks: List[Dict[str, Any]] = []

    def create_entity(
        self,
        legal_name: str,
        registered_agent_name: str,
        registered_agent_address: str,
        principal_place_of_business: str,
        formation_date: Optional[str] = None
    ) -> WyomingDAOEntity:
        """
        Create a new Wyoming DAO LLC entity.

        Args:
            legal_name: Legal name of the DAO
            registered_agent_name: Name of registered agent
            registered_agent_address: Address of registered agent
            principal_place_of_business: Principal business address
            formation_date: Formation date (defaults to today)

        Returns:
            WyomingDAOEntity instance
        """
        self.entity = WyomingDAOEntity(
            legal_name=legal_name,
            registered_agent_name=registered_agent_name,
            registered_agent_address=registered_agent_address,
            principal_place_of_business=principal_place_of_business,
            formation_date=formation_date or datetime.now().strftime('%Y-%m-%d')
        )
        return self.entity

    def add_ai_stakeholder(
        self,
        name: str,
        voting_power: float = 0.33,
        role: str = "AI Manager"
    ) -> AIStakeholder:
        """
        Add an AI stakeholder to the DAO.

        Per Wyoming DAO Supplement, AI can serve as manager
        with voting rights if properly disclosed.

        Args:
            name: Name of AI entity (e.g., "EXECAI")
            voting_power: Voting power percentage
            role: Role in DAO governance

        Returns:
            AIStakeholder instance
        """
        if not self.entity:
            raise ValueError("Entity must be created first")

        ai_stakeholder = AIStakeholder(
            name=name,
            voting_power=voting_power,
            role=role
        )
        self.entity.ai_stakeholders.append(ai_stakeholder)
        return ai_stakeholder

    def add_member(
        self,
        legal_name: str,
        member_type: str,
        address: str,
        tax_id: Optional[str] = None,
        voting_power: float = 0.0,
        kyc_verified: bool = False
    ) -> DAOMember:
        """
        Add a member to the DAO.

        Args:
            legal_name: Legal name of member
            member_type: "Human" or "Organization"
            address: Member address
            tax_id: SSN (human) or EIN (org)
            voting_power: Voting power percentage
            kyc_verified: Whether KYC is complete

        Returns:
            DAOMember instance
        """
        if not self.entity:
            raise ValueError("Entity must be created first")

        member = DAOMember(
            legal_name=legal_name,
            member_type=member_type,
            address=address,
            tax_id=tax_id,
            voting_power=voting_power,
            kyc_verified=kyc_verified
        )
        self.entity.members.append(member)
        return member

    def set_smart_contracts(self, contracts: Dict[str, str]) -> None:
        """
        Set smart contract addresses for the DAO.

        Args:
            contracts: Dict mapping contract name to address
        """
        if not self.entity:
            raise ValueError("Entity must be created first")

        self.entity.smart_contract_addresses = contracts

    def validate_compliance(self) -> Dict[str, Any]:
        """
        Validate DAO compliance with Wyoming requirements.

        Returns:
            Dict with compliance status and issues
        """
        if not self.entity:
            return {
                'compliant': False,
                'issues': ['No entity configured'],
                'score': 0
            }

        issues = []
        checks_passed = 0
        total_checks = len(self.STATUTORY_REQUIREMENTS)

        # Check required fields
        for field_name in self.REQUIRED_FIELDS:
            value = getattr(self.entity, field_name, None)
            if not value:
                issues.append(f"Missing required field: {field_name}")

        # Check smart contracts
        if self.STATUTORY_REQUIREMENTS['smart_contract_required']:
            if not self.entity.smart_contract_addresses:
                issues.append("No smart contract addresses configured")
            else:
                checks_passed += 1

        # Check registered agent
        if self.STATUTORY_REQUIREMENTS['registered_agent_required']:
            if self.entity.registered_agent_name and self.entity.registered_agent_address:
                checks_passed += 1
            else:
                issues.append("Registered agent information incomplete")

        # Check AI disclosure
        if self.entity.ai_stakeholders:
            if self.STATUTORY_REQUIREMENTS['ai_manager_disclosure']:
                # AI stakeholders exist and disclosure is required
                checks_passed += 1  # Assume disclosed if AI exists

        # Calculate compliance score
        score = (checks_passed / total_checks) * 100 if total_checks > 0 else 0

        result = {
            'compliant': len(issues) == 0,
            'issues': issues,
            'score': score,
            'checks_passed': checks_passed,
            'total_checks': total_checks,
            'timestamp': datetime.now().isoformat()
        }

        self.compliance_checks.append(result)
        return result

    def generate_filing_data(self) -> Dict[str, Any]:
        """
        Generate data for Wyoming DAO LLC filing.

        Returns:
            Dict with all filing data
        """
        if not self.entity:
            raise ValueError("Entity must be created first")

        # Calculate total voting power
        total_ai_power = sum(ai.voting_power for ai in self.entity.ai_stakeholders)
        total_human_power = sum(m.voting_power for m in self.entity.members)

        return {
            'entity_information': {
                'legal_name': self.entity.legal_name,
                'entity_type': self.entity.entity_type,
                'jurisdiction': self.entity.jurisdiction,
                'formation_date': self.entity.formation_date,
                'principal_place_of_business': self.entity.principal_place_of_business
            },
            'registered_agent': {
                'name': self.entity.registered_agent_name,
                'address': self.entity.registered_agent_address
            },
            'blockchain_infrastructure': {
                'smart_contracts': self.entity.smart_contract_addresses,
                'governance_mechanism': 'On-chain voting with EPI validation'
            },
            'ai_stakeholders': [
                {
                    'name': ai.name,
                    'type': ai.entity_type,
                    'voting_power': f"{ai.voting_power:.0%}",
                    'role': ai.role,
                    'capabilities': ai.capabilities
                }
                for ai in self.entity.ai_stakeholders
            ],
            'members': [
                {
                    'legal_name': m.legal_name,
                    'type': m.member_type,
                    'voting_power': f"{m.voting_power:.0%}",
                    'kyc_verified': m.kyc_verified
                }
                for m in self.entity.members
            ],
            'voting_power_distribution': {
                'ai_total': f"{total_ai_power:.0%}",
                'human_total': f"{total_human_power:.0%}",
                'total': f"{total_ai_power + total_human_power:.0%}"
            },
            'generated_at': datetime.now().isoformat()
        }

    def get_compliance_summary(self) -> Dict[str, Any]:
        """Get summary of all compliance checks."""
        if not self.compliance_checks:
            return {'message': 'No compliance checks performed'}

        latest = self.compliance_checks[-1]
        avg_score = sum(c['score'] for c in self.compliance_checks) / len(self.compliance_checks)

        return {
            'total_checks': len(self.compliance_checks),
            'latest_status': 'Compliant' if latest['compliant'] else 'Non-Compliant',
            'latest_score': latest['score'],
            'average_score': avg_score,
            'latest_issues': latest['issues']
        }
