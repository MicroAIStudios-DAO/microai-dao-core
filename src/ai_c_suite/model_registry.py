"""
Model Registry
==============

Centralized registry for all AI models in the system.
Tracks model metadata, versions, performance, and deployment status.

Features:
- Model registration and versioning
- Performance metrics tracking
- Deployment status management
- Integration with Trust Stack for audit trail
- Risk tier assignment
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional, Any
from enum import Enum
import json
import hashlib
import sqlite3
from pathlib import Path


class ModelStatus(Enum):
    """Model deployment status."""
    REGISTERED = "registered"
    TESTING = "testing"
    APPROVED = "approved"
    DEPLOYED = "deployed"
    DEPRECATED = "deprecated"
    RETIRED = "retired"


class ModelType(Enum):
    """Type of AI model."""
    CLASSIFICATION = "classification"
    REGRESSION = "regression"
    GENERATION = "generation"
    RECOMMENDATION = "recommendation"
    REINFORCEMENT = "reinforcement"
    AGENT = "agent"
    OTHER = "other"


@dataclass
class ModelVersion:
    """A specific version of a model."""
    version: str
    model_hash: str
    created_at: datetime
    created_by: str
    changes: str
    performance_metrics: Dict[str, float] = field(default_factory=dict)
    epi_score: Optional[float] = None
    risk_tier: Optional[int] = None
    deployment_date: Optional[datetime] = None
    status: ModelStatus = ModelStatus.REGISTERED


@dataclass
class AIModel:
    """AI Model metadata and tracking."""
    model_id: str
    name: str
    model_type: ModelType
    description: str
    use_case: str
    owner: str
    created_at: datetime
    current_version: str
    versions: List[ModelVersion] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    risk_tier: Optional[int] = None
    status: ModelStatus = ModelStatus.REGISTERED
    metadata: Dict[str, Any] = field(default_factory=dict)


class ModelRegistry:
    """
    Registry for managing AI models.
    
    Provides:
    - Model registration and versioning
    - Performance tracking
    - Deployment management
    - Audit trail integration
    """
    
    def __init__(self, db_path: str = "model_registry.db"):
        """Initialize model registry with database."""
        self.db_path = db_path
        self._init_database()
    
    def _init_database(self):
        """Initialize SQLite database for model registry."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Models table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS models (
                model_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                model_type TEXT NOT NULL,
                description TEXT,
                use_case TEXT,
                owner TEXT,
                created_at TEXT NOT NULL,
                current_version TEXT,
                risk_tier INTEGER,
                status TEXT,
                tags TEXT,
                metadata TEXT
            )
        """)
        
        # Versions table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS model_versions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                model_id TEXT NOT NULL,
                version TEXT NOT NULL,
                model_hash TEXT NOT NULL,
                created_at TEXT NOT NULL,
                created_by TEXT,
                changes TEXT,
                performance_metrics TEXT,
                epi_score REAL,
                risk_tier INTEGER,
                deployment_date TEXT,
                status TEXT,
                FOREIGN KEY (model_id) REFERENCES models(model_id),
                UNIQUE(model_id, version)
            )
        """)
        
        # Performance metrics table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS performance_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                model_id TEXT NOT NULL,
                version TEXT NOT NULL,
                metric_name TEXT NOT NULL,
                metric_value REAL NOT NULL,
                recorded_at TEXT NOT NULL,
                FOREIGN KEY (model_id) REFERENCES models(model_id)
            )
        """)
        
        conn.commit()
        conn.close()
    
    def register_model(
        self,
        name: str,
        model_type: ModelType,
        description: str,
        use_case: str,
        owner: str,
        initial_version: str = "1.0.0",
        model_hash: Optional[str] = None,
        tags: Optional[List[str]] = None,
        risk_tier: Optional[int] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> AIModel:
        """
        Register a new AI model.
        
        Args:
            name: Model name
            model_type: Type of model
            description: Model description
            use_case: Primary use case
            owner: Model owner/creator
            initial_version: Initial version number
            model_hash: Hash of model weights/code
            tags: Tags for categorization
            risk_tier: Risk tier (1-4)
            metadata: Additional metadata
        
        Returns:
            Registered AIModel
        """
        model_id = self._generate_model_id(name, owner)
        
        # Create initial version
        if model_hash is None:
            model_hash = self._calculate_hash(f"{name}:{initial_version}")
        
        initial_version_obj = ModelVersion(
            version=initial_version,
            model_hash=model_hash,
            created_at=datetime.now(),
            created_by=owner,
            changes="Initial version",
            status=ModelStatus.REGISTERED
        )
        
        # Create model
        model = AIModel(
            model_id=model_id,
            name=name,
            model_type=model_type,
            description=description,
            use_case=use_case,
            owner=owner,
            created_at=datetime.now(),
            current_version=initial_version,
            versions=[initial_version_obj],
            tags=tags or [],
            risk_tier=risk_tier,
            status=ModelStatus.REGISTERED,
            metadata=metadata or {}
        )
        
        # Save to database
        self._save_model(model)
        
        return model
    
    def add_version(
        self,
        model_id: str,
        version: str,
        model_hash: str,
        created_by: str,
        changes: str,
        performance_metrics: Optional[Dict[str, float]] = None,
        epi_score: Optional[float] = None
    ) -> ModelVersion:
        """
        Add a new version to an existing model.
        
        Args:
            model_id: Model ID
            version: Version number
            model_hash: Hash of new model
            created_by: Creator of this version
            changes: Description of changes
            performance_metrics: Performance metrics
            epi_score: EPI score for this version
        
        Returns:
            New ModelVersion
        """
        model = self.get_model(model_id)
        if not model:
            raise ValueError(f"Model {model_id} not found")
        
        # Create new version
        new_version = ModelVersion(
            version=version,
            model_hash=model_hash,
            created_at=datetime.now(),
            created_by=created_by,
            changes=changes,
            performance_metrics=performance_metrics or {},
            epi_score=epi_score,
            status=ModelStatus.REGISTERED
        )
        
        # Update model
        model.versions.append(new_version)
        model.current_version = version
        
        # Save to database
        self._save_version(model_id, new_version)
        self._update_model_version(model_id, version)
        
        return new_version
    
    def update_status(
        self,
        model_id: str,
        status: ModelStatus,
        version: Optional[str] = None
    ):
        """
        Update model or version status.
        
        Args:
            model_id: Model ID
            status: New status
            version: Specific version (if None, updates model status)
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if version:
            cursor.execute("""
                UPDATE model_versions
                SET status = ?
                WHERE model_id = ? AND version = ?
            """, (status.value, model_id, version))
        else:
            cursor.execute("""
                UPDATE models
                SET status = ?
                WHERE model_id = ?
            """, (status.value, model_id))
        
        conn.commit()
        conn.close()
    
    def record_performance(
        self,
        model_id: str,
        version: str,
        metrics: Dict[str, float]
    ):
        """
        Record performance metrics for a model version.
        
        Args:
            model_id: Model ID
            version: Version number
            metrics: Performance metrics
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        recorded_at = datetime.now().isoformat()
        
        for metric_name, metric_value in metrics.items():
            cursor.execute("""
                INSERT INTO performance_metrics
                (model_id, version, metric_name, metric_value, recorded_at)
                VALUES (?, ?, ?, ?, ?)
            """, (model_id, version, metric_name, metric_value, recorded_at))
        
        # Update version performance metrics
        cursor.execute("""
            UPDATE model_versions
            SET performance_metrics = ?
            WHERE model_id = ? AND version = ?
        """, (json.dumps(metrics), model_id, version))
        
        conn.commit()
        conn.close()
    
    def get_model(self, model_id: str) -> Optional[AIModel]:
        """Get model by ID."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM models WHERE model_id = ?", (model_id,))
        row = cursor.fetchone()
        
        if not row:
            conn.close()
            return None
        
        # Parse model data
        model = self._parse_model_row(row)
        
        # Get versions
        cursor.execute("""
            SELECT * FROM model_versions
            WHERE model_id = ?
            ORDER BY created_at DESC
        """, (model_id,))
        
        versions = [self._parse_version_row(v) for v in cursor.fetchall()]
        model.versions = versions
        
        conn.close()
        return model
    
    def list_models(
        self,
        model_type: Optional[ModelType] = None,
        status: Optional[ModelStatus] = None,
        risk_tier: Optional[int] = None,
        tags: Optional[List[str]] = None
    ) -> List[AIModel]:
        """
        List models with optional filters.
        
        Args:
            model_type: Filter by model type
            status: Filter by status
            risk_tier: Filter by risk tier
            tags: Filter by tags
        
        Returns:
            List of matching models
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        query = "SELECT * FROM models WHERE 1=1"
        params = []
        
        if model_type:
            query += " AND model_type = ?"
            params.append(model_type.value)
        
        if status:
            query += " AND status = ?"
            params.append(status.value)
        
        if risk_tier:
            query += " AND risk_tier = ?"
            params.append(risk_tier)
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        
        models = [self._parse_model_row(row) for row in rows]
        
        # Filter by tags if provided
        if tags:
            models = [m for m in models if any(tag in m.tags for tag in tags)]
        
        conn.close()
        return models
    
    def get_model_stats(self) -> Dict[str, Any]:
        """Get registry statistics."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Total models
        cursor.execute("SELECT COUNT(*) FROM models")
        total_models = cursor.fetchone()[0]
        
        # Models by status
        cursor.execute("""
            SELECT status, COUNT(*) 
            FROM models 
            GROUP BY status
        """)
        by_status = dict(cursor.fetchall())
        
        # Models by type
        cursor.execute("""
            SELECT model_type, COUNT(*) 
            FROM models 
            GROUP BY model_type
        """)
        by_type = dict(cursor.fetchall())
        
        # Models by risk tier
        cursor.execute("""
            SELECT risk_tier, COUNT(*) 
            FROM models 
            WHERE risk_tier IS NOT NULL
            GROUP BY risk_tier
        """)
        by_risk = dict(cursor.fetchall())
        
        conn.close()
        
        return {
            "total_models": total_models,
            "by_status": by_status,
            "by_type": by_type,
            "by_risk_tier": by_risk
        }
    
    def _generate_model_id(self, name: str, owner: str) -> str:
        """Generate unique model ID."""
        timestamp = datetime.now().isoformat()
        content = f"{name}:{owner}:{timestamp}"
        return hashlib.sha256(content.encode()).hexdigest()[:16]
    
    def _calculate_hash(self, content: str) -> str:
        """Calculate SHA-256 hash."""
        return hashlib.sha256(content.encode()).hexdigest()
    
    def _save_model(self, model: AIModel):
        """Save model to database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT OR REPLACE INTO models
            (model_id, name, model_type, description, use_case, owner,
             created_at, current_version, risk_tier, status, tags, metadata)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            model.model_id,
            model.name,
            model.model_type.value,
            model.description,
            model.use_case,
            model.owner,
            model.created_at.isoformat(),
            model.current_version,
            model.risk_tier,
            model.status.value,
            json.dumps(model.tags),
            json.dumps(model.metadata)
        ))
        
        # Save initial version
        if model.versions:
            self._save_version(model.model_id, model.versions[0])
        
        conn.commit()
        conn.close()
    
    def _save_version(self, model_id: str, version: ModelVersion):
        """Save model version to database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT OR REPLACE INTO model_versions
            (model_id, version, model_hash, created_at, created_by, changes,
             performance_metrics, epi_score, risk_tier, deployment_date, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            model_id,
            version.version,
            version.model_hash,
            version.created_at.isoformat(),
            version.created_by,
            version.changes,
            json.dumps(version.performance_metrics),
            version.epi_score,
            version.risk_tier,
            version.deployment_date.isoformat() if version.deployment_date else None,
            version.status.value
        ))
        
        conn.commit()
        conn.close()
    
    def _update_model_version(self, model_id: str, version: str):
        """Update current version of a model."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE models
            SET current_version = ?
            WHERE model_id = ?
        """, (version, model_id))
        
        conn.commit()
        conn.close()
    
    def _parse_model_row(self, row) -> AIModel:
        """Parse database row into AIModel."""
        return AIModel(
            model_id=row[0],
            name=row[1],
            model_type=ModelType(row[2]),
            description=row[3],
            use_case=row[4],
            owner=row[5],
            created_at=datetime.fromisoformat(row[6]),
            current_version=row[7],
            risk_tier=row[8],
            status=ModelStatus(row[9]),
            tags=json.loads(row[10]) if row[10] else [],
            metadata=json.loads(row[11]) if row[11] else {}
        )
    
    def _parse_version_row(self, row) -> ModelVersion:
        """Parse database row into ModelVersion."""
        return ModelVersion(
            version=row[2],
            model_hash=row[3],
            created_at=datetime.fromisoformat(row[4]),
            created_by=row[5],
            changes=row[6],
            performance_metrics=json.loads(row[7]) if row[7] else {},
            epi_score=row[8],
            risk_tier=row[9],
            deployment_date=datetime.fromisoformat(row[10]) if row[10] else None,
            status=ModelStatus(row[11])
        )


# Example usage
if __name__ == "__main__":
    registry = ModelRegistry()
    
    # Register CEO-AI model
    ceo_model = registry.register_model(
        name="CEO-AI",
        model_type=ModelType.AGENT,
        description="Strategic planning and proposal generation agent",
        use_case="Generate strategic proposals with EPI validation",
        owner="MicroAI-DAO",
        initial_version="1.0.0",
        tags=["agent", "strategic", "governance"],
        risk_tier=2,
        metadata={"base_model": "microsoft/Phi-3-mini-4k-instruct"}
    )
    
    print(f"Registered model: {ceo_model.name} ({ceo_model.model_id})")
    
    # Register CFO-AI model
    cfo_model = registry.register_model(
        name="CFO-AI",
        model_type=ModelType.AGENT,
        description="Financial decision-making agent",
        use_case="Process payments and manage treasury with EPI constraints",
        owner="MicroAI-DAO",
        initial_version="1.0.0",
        tags=["agent", "financial", "governance"],
        risk_tier=3,
        metadata={"base_model": "microsoft/Phi-3-mini-4k-instruct"}
    )
    
    print(f"Registered model: {cfo_model.name} ({cfo_model.model_id})")
    
    # Get stats
    stats = registry.get_model_stats()
    print(f"\nRegistry Stats:")
    print(f"  Total models: {stats['total_models']}")
    print(f"  By type: {stats['by_type']}")
    print(f"  By risk tier: {stats['by_risk_tier']}")
