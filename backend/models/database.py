from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from backend.config import settings

import os
import shutil

# Handle Vercel/Heroku style postgres:// URIs
db_url = settings.DATABASE_URL
if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)

# Fix for Vercel Serverless environment (make SQLite writable)
if "sqlite" in db_url and os.environ.get("VERCEL"):
    tmp_db_path = "/tmp/roomiematch.db"
    if not os.path.exists(tmp_db_path):
        source_db = "roomiematch.db"
        if not os.path.exists(source_db):
            source_db = "./roomiematch.db"
        try:
            shutil.copy2(source_db, tmp_db_path)
        except Exception as e:
            pass
    db_url = f"sqlite:///{tmp_db_path}"

engine = create_engine(
    db_url, 
    connect_args={"check_same_thread": False} if "sqlite" in db_url else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
