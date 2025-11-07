from sqlmodel import SQLModel, create_engine, Session

DATABASE_URL = "sqlite:///database.db"

engine = create_engine(DATABASE_URL, echo=False, connect_args={"check_same_thread": False})


def init_db() -> None:
    """Create all tables."""
    import models  # noqa: F401  # ensure models are registered
    import auth_models  # noqa: F401  # ensure auth models are registered
    SQLModel.metadata.create_all(engine)


def get_session() -> Session:
    """Return a new database session."""
    return Session(engine)
