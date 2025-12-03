import os
from typing import Generator
from sqlmodel import SQLModel, create_engine, Session

# Use PostgreSQL in production (Render), SQLite for local development
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///database.db")

# Render provides DATABASE_URL starting with "postgres://" but SQLAlchemy needs "postgresql+psycopg://"
# for psycopg3 (the modern PostgreSQL driver)
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+psycopg://", 1)
elif DATABASE_URL.startswith("postgresql://") and "+psycopg" not in DATABASE_URL:
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+psycopg://", 1)

# SQLite needs special connect_args, PostgreSQL doesn't
# Configure pool settings for better connection management
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(DATABASE_URL, echo=False, connect_args={"check_same_thread": False})
else:
    # PostgreSQL pool settings - recycle connections and handle overflow better
    engine = create_engine(
        DATABASE_URL, 
        echo=False,
        pool_size=5,
        max_overflow=10,
        pool_timeout=30,
        pool_recycle=1800,  # Recycle connections after 30 minutes
        pool_pre_ping=True,  # Verify connections before using
    )


def init_db() -> None:
    """Create all tables."""
    import models  # noqa: F401  # ensure models are registered
    import auth_models  # noqa: F401  # ensure auth models are registered
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    """Yield a database session and ensure it's closed after use."""
    session = Session(engine)
    try:
        yield session
    finally:
        session.close()
