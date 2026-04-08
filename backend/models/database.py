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
    
    # Try to find the source DB using absolute path
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    source_db = os.path.join(base_dir, "roomiematch.db")
    
    if not os.path.exists(tmp_db_path):
        try:
            if os.path.exists(source_db):
                shutil.copy2(source_db, tmp_db_path)
        except Exception as e:
            print(f"Failed to copy DB: {e}")
            pass
    db_url = f"sqlite:///{tmp_db_path}"

engine = create_engine(
    db_url, 
    connect_args={"check_same_thread": False} if "sqlite" in db_url else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

if "sqlite" in db_url and os.environ.get("VERCEL"):
    try:
        Base.metadata.create_all(bind=engine)
    except Exception:
        pass

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
