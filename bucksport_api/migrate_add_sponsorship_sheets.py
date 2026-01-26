import os

from sqlmodel import SQLModel, create_engine

from models import SponsorshipSheetMeta, SponsorshipSheetRow


def main() -> None:
    database_url = os.getenv("DATABASE_URL", "sqlite:///database.db")
    if database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql+psycopg://", 1)
    elif database_url.startswith("postgresql://") and "+psycopg" not in database_url:
        database_url = database_url.replace("postgresql://", "postgresql+psycopg://", 1)

    print(f"Connecting to database: {database_url.split('@')[0] if '@' in database_url else database_url}")
    engine = create_engine(database_url, echo=True)

    SQLModel.metadata.create_all(engine)
    print("✅ Sponsorship sheet tables created (if they did not already exist)")


if __name__ == "__main__":
    main()
