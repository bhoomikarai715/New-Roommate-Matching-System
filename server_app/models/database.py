from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from server_app.config import settings

import os
import shutil

# Handle Vercel/Heroku style postgres:// URIs
db_url = settings.DATABASE_URL
if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)

# Fix for Vercel Serverless environment (make SQLite writable via memory)
if "sqlite" in db_url and os.environ.get("VERCEL"):
    # Use a pure in-memory SQLite database on Vercel
    db_url = "sqlite:///:memory:"

# SQLAlchemy 2.0+ connect arguments
# check_same_thread False allows multiple threads to share the SQLite connection
connect_args = {"check_same_thread": False} if "sqlite" in db_url else {}

# For in-memory SQLite, we must share a single connection so the db isn't destroyed instantly
from sqlalchemy.pool import StaticPool
if db_url == "sqlite:///:memory:":
    connect_args["check_same_thread"] = False
    
engine = create_engine(
    db_url, 
    connect_args=connect_args,
    poolclass=StaticPool if db_url == "sqlite:///:memory:" else None
)

from server_app.models.base import Base

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """Centralized database initialization, especially for Vercel's in-memory SQLite."""
    if "sqlite" in db_url and os.environ.get("VERCEL"):
        try:
            # Import entities here to avoid circular imports and ensure tables are indexed
            import server_app.models.entities
            Base.metadata.create_all(bind=engine)
            
            # Seed the database dynamically for the in-memory SQLite
            from server_app.services.seeder import seed_database
            with SessionLocal() as db:
                seed_database(db)
        except Exception as e:
            print(f"Table creation or seeding failed: {e}")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
