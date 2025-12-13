"""
Database Initialization Script
==============================

Initializes the MicroAI DAO database with enterprise schema.
Creates all tables, indexes, views, and triggers.
"""

import sqlite3
import os
from pathlib import Path


def init_database(db_path: str = "microai_dao.db", schema_path: str = None):
    """
    Initialize database with schema.
    
    Args:
        db_path: Path to SQLite database file
        schema_path: Path to schema.sql file (optional)
    """
    # Get schema path
    if schema_path is None:
        schema_path = Path(__file__).parent / "schema.sql"
    
    # Read schema
    with open(schema_path, 'r') as f:
        schema_sql = f.read()
    
    # Create database
    print(f"Initializing database: {db_path}")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Execute schema
    cursor.executescript(schema_sql)
    
    conn.commit()
    conn.close()
    
    print("✅ Database initialized successfully!")
    print(f"   Location: {os.path.abspath(db_path)}")
    
    # Verify tables
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT name FROM sqlite_master 
        WHERE type='table' 
        ORDER BY name
    """)
    
    tables = [row[0] for row in cursor.fetchall()]
    
    print(f"\n📊 Created {len(tables)} tables:")
    for table in tables:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        print(f"   - {table}: {count} rows")
    
    conn.close()


def create_default_organization(db_path: str = "microai_dao.db"):
    """Create default organization for testing."""
    import hashlib
    from datetime import datetime
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    org_id = hashlib.sha256(b"MicroAI-DAO-Default").hexdigest()[:16]
    
    cursor.execute("""
        INSERT OR IGNORE INTO organizations
        (id, name, status, metadata)
        VALUES (?, ?, ?, ?)
    """, (
        org_id,
        "MicroAI DAO",
        "active",
        '{"description": "Default organization for MicroAI DAO governance"}'
    ))
    
    conn.commit()
    conn.close()
    
    print(f"\n✅ Created default organization: {org_id}")
    return org_id


def main():
    """Main initialization function."""
    print("=" * 70)
    print("  MicroAI DAO Database Initialization")
    print("=" * 70)
    print()
    
    # Initialize database
    init_database()
    
    # Create default organization
    org_id = create_default_organization()
    
    print()
    print("=" * 70)
    print("  Initialization Complete!")
    print("=" * 70)
    print()
    print("Next steps:")
    print("  1. Register stakeholders: python -m src.governance.register_stakeholder")
    print("  2. Register AI models: python -m src.ai_c_suite.model_registry")
    print("  3. Start API server: python api/app.py")
    print()


if __name__ == "__main__":
    main()
