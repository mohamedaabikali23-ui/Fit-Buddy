"""
FitBuddy - Database Configuration
Configures SQLite database and SQLAlchemy session management.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "sqlite:///./fitbuddy.db"

# connect_args={"check_same_thread": False} is required for SQLite with multi-threaded ASGI apps
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """
    Dependency for FastAPI route handlers that yields a database session
    and ensures it is properly closed after request completion.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
