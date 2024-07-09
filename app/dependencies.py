from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Setting up the SQLAlchemy database URL from environment variables or using a default value
SQLALCHEMY_DATABASE_URL = (
    os.getenv("DATABASE_URL")
    if os.getenv("DATABASE_URL") is not None
    else "postgresql://postgres:password@localhost:5432/mydatabase"
)

# Creating the SQLAlchemy engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Creating a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Creating a base class for the declarative models
Base = declarative_base()


# Dependency to get a database session
def get_db():
    """
    Provides a SQLAlchemy session.

    Yields:
    - Session: A SQLAlchemy session to interact with the database.

    Ensures that the session is closed after use.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
