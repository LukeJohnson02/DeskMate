"""Database engine and session setup for the DeskMate backend."""

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./app.db"

# SQLite is used for this project, so `check_same_thread=False` allows FastAPI's
# request handling and tests to reuse sessions safely across worker threads.
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()


def get_db():
    """Yield a SQLAlchemy session for a single request.

    Yields:
        A database session connected to the local SQLite database.

    The `yield` syntax turns this into a FastAPI dependency with teardown
    behavior. FastAPI runs the code before `yield` for the request, passes the
    yielded session into the route, and then always executes `finally` so the
    connection is closed even if a route raises an exception.
    """

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
