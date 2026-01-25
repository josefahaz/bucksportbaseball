"""
Migration script to add Donation table to the database.
Run this to create the donation table in both local and production databases.
"""
import os
from sqlmodel import SQLModel, create_engine
from models import Donation  # Import to register the table

# Get database URL from environment or use local SQLite
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///database.db")

# Handle Render PostgreSQL URL format
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

print(f"Connecting to database: {DATABASE_URL.split('@')[0] if '@' in DATABASE_URL else DATABASE_URL}")

# Create engine
engine = create_engine(DATABASE_URL, echo=True)

# Create all tables (will only create missing ones)
print("\nCreating Donation table...")
SQLModel.metadata.create_all(engine)

print("\n✅ Migration complete! Donation table created successfully.")
