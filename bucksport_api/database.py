import os
from sqlmodel import SQLModel, create_engine, Session

# Use PostgreSQL in production (Render), SQLite for local development
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///database.db")

# Render provides DATABASE_URL starting with "postgres://" but SQLAlchemy needs "postgresql://"
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# SQLite needs special connect_args, PostgreSQL doesn't
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(DATABASE_URL, echo=False, connect_args={"check_same_thread": False})
else:
    engine = create_engine(DATABASE_URL, echo=False)


def init_db() -> None:
    """Create all tables."""
    import models  # noqa: F401  # ensure models are registered
    import auth_models  # noqa: F401  # ensure auth models are registered
    SQLModel.metadata.create_all(engine)


def get_session() -> Session:
    """Return a new database session."""
    return Session(engine)
