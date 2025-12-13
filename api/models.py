"""
SQLAlchemy Models
=================

Database models for users, proposals, votes, and governance.
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, ForeignKey, Enum
from sqlalchemy.orm import relationship
import enum

db = SQLAlchemy()


class UserRole(enum.Enum):
    """User roles for RBAC."""
    USER = "user"
    STAKEHOLDER = "stakeholder"
    GUARDIAN = "guardian"
    ADMIN = "admin"


class ProposalStatus(enum.Enum):
    """Proposal status."""
    PENDING = "pending"
    ACTIVE = "active"
    PASSED = "passed"
    REJECTED = "rejected"
    EXECUTED = "executed"
    CANCELLED = "cancelled"


class VoteChoice(enum.Enum):
    """Vote choices."""
    FOR = "for"
    AGAINST = "against"
    ABSTAIN = "abstain"


class User(db.Model):
    """User model for authentication and authorization."""
    __tablename__ = 'users'
    
    id = Column(String(64), primary_key=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(64), nullable=False)
    wallet_address = Column(String(64), unique=True, nullable=False, index=True)
    name = Column(String(255))
    role = Column(Enum(UserRole), default=UserRole.USER, nullable=False)
    voting_power = Column(Float, default=1.0)
    delegation_address = Column(String(64))
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = Column(DateTime)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    proposals = relationship('Proposal', back_populates='proposer', foreign_keys='Proposal.proposer_id')
    votes = relationship('Vote', back_populates='voter')
    api_keys = relationship('APIKey', back_populates='user')
    
    def __repr__(self):
        return f"<User {self.email}>"
    
    def to_dict(self):
        """Convert to dictionary."""
        return {
            'id': self.id,
            'email': self.email,
            'wallet_address': self.wallet_address,
            'name': self.name,
            'role': self.role.value,
            'voting_power': self.voting_power,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'is_active': self.is_active
        }


class Proposal(db.Model):
    """Governance proposal model."""
    __tablename__ = 'proposals'
    
    id = Column(String(64), primary_key=True)
    title = Column(String(500), nullable=False)
    description = Column(Text)
    proposal_type = Column(String(50), nullable=False)
    
    proposer_id = Column(String(64), ForeignKey('users.id'), nullable=False)
    model_id = Column(String(64))
    
    status = Column(Enum(ProposalStatus), default=ProposalStatus.PENDING, nullable=False)
    
    voting_start = Column(DateTime)
    voting_end = Column(DateTime)
    execution_time = Column(DateTime)
    
    quorum_required = Column(Float, default=0.30)
    majority_required = Column(Float, default=0.50)
    
    votes_for = Column(Integer, default=0)
    votes_against = Column(Integer, default=0)
    votes_abstain = Column(Integer, default=0)
    total_voting_power = Column(Float, default=0.0)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    metadata_json = Column(Text)  # JSON metadata
    
    # Relationships
    proposer = relationship('User', back_populates='proposals', foreign_keys=[proposer_id])
    votes = relationship('Vote', back_populates='proposal')
    
    def __repr__(self):
        return f"<Proposal {self.title}>"
    
    def to_dict(self):
        """Convert to dictionary."""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'proposal_type': self.proposal_type,
            'proposer_id': self.proposer_id,
            'proposer_name': self.proposer.name if self.proposer else None,
            'model_id': self.model_id,
            'status': self.status.value,
            'voting_start': self.voting_start.isoformat() if self.voting_start else None,
            'voting_end': self.voting_end.isoformat() if self.voting_end else None,
            'quorum_required': self.quorum_required,
            'majority_required': self.majority_required,
            'votes_for': self.votes_for,
            'votes_against': self.votes_against,
            'votes_abstain': self.votes_abstain,
            'total_voting_power': self.total_voting_power,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class Vote(db.Model):
    """Vote model."""
    __tablename__ = 'votes'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    proposal_id = Column(String(64), ForeignKey('proposals.id'), nullable=False)
    voter_id = Column(String(64), ForeignKey('users.id'), nullable=False)
    
    vote_choice = Column(Enum(VoteChoice), nullable=False)
    vote_weight = Column(Float, nullable=False)
    reasoning = Column(Text)
    signature = Column(String(256))
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    proposal = relationship('Proposal', back_populates='votes')
    voter = relationship('User', back_populates='votes')
    
    __table_args__ = (
        db.UniqueConstraint('proposal_id', 'voter_id', name='unique_vote_per_proposal'),
    )
    
    def __repr__(self):
        return f"<Vote {self.vote_choice.value} on {self.proposal_id}>"
    
    def to_dict(self):
        """Convert to dictionary."""
        return {
            'id': self.id,
            'proposal_id': self.proposal_id,
            'voter_id': self.voter_id,
            'voter_name': self.voter.name if self.voter else None,
            'vote_choice': self.vote_choice.value,
            'vote_weight': self.vote_weight,
            'reasoning': self.reasoning,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class APIKey(db.Model):
    """API key model for programmatic access."""
    __tablename__ = 'api_keys'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    key_hash = Column(String(64), unique=True, nullable=False, index=True)
    user_id = Column(String(64), ForeignKey('users.id'), nullable=False)
    
    name = Column(String(255), nullable=False)
    scopes = Column(String(500))  # Comma-separated scopes
    
    created_at = Column(DateTime, default=datetime.utcnow)
    last_used = Column(DateTime)
    expires_at = Column(DateTime)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    user = relationship('User', back_populates='api_keys')
    
    def __repr__(self):
        return f"<APIKey {self.name}>"
    
    def to_dict(self):
        """Convert to dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'scopes': self.scopes.split(',') if self.scopes else [],
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_used': self.last_used.isoformat() if self.last_used else None,
            'expires_at': self.expires_at.isoformat() if self.expires_at else None,
            'is_active': self.is_active
        }


def init_db(app):
    """Initialize database with Flask app."""
    db.init_app(app)
    
    with app.app_context():
        db.create_all()
    
    return db
