import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Fallback to local SQLite if DATABASE_URL not set or points to default postgres
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL or "postgresql://user:password" in DATABASE_URL:
    db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "matrubhasa.db"))
    DATABASE_URL = f"sqlite:///{db_path}"
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    # Standard PostgreSQL support
    engine = create_engine(DATABASE_URL, pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """FastAPI dependency to yield database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
