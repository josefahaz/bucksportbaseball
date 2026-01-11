"""
Migration script to add ActivityLog table to production database.
Run this on Render shell: python migrate_add_activity_log.py
"""
import os
from sqlmodel import SQLModel, create_engine
from models import ActivityLog  # Import to ensure it's registered

# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///database.db")

# Fix Render's postgres:// to postgresql+psycopg://
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+psycopg://", 1)
elif DATABASE_URL.startswith("postgresql://") and "+psycopg" not in DATABASE_URL:
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+psycopg://", 1)

print("=" * 60)
print("DATABASE MIGRATION: Add ActivityLog Table")
print("=" * 60)
print(f"\nDatabase: {DATABASE_URL.split('@')[0]}@...")

# Create engine
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(DATABASE_URL, echo=True, connect_args={"check_same_thread": False})
else:
    engine = create_engine(DATABASE_URL, echo=True)

print("\nCreating ActivityLog table...")

try:
    # Import all models to ensure they're registered
    import models
    import auth_models
    
    # Create all tables (will only create missing ones)
    SQLModel.metadata.create_all(engine)
    
    print("\n✓ Migration completed successfully!")
    print("✓ ActivityLog table is now available")
    
    # Verify the table exists
    from sqlmodel import Session, select
    with Session(engine) as session:
        # Try to query the table
        statement = select(ActivityLog)
        result = session.exec(statement).all()
        print(f"✓ Verified: ActivityLog table has {len(result)} entries")
    
except Exception as e:
    print(f"\n✗ Migration failed: {e}")
    raise

print("\n" + "=" * 60)
print("Migration complete! Activity logs are now enabled.")
print("=" * 60)
