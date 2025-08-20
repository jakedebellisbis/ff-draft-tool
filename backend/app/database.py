# backend/app/database.py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.engine.url import make_url

# Use DATABASE_URL if provided (Render/Neon), otherwise fall back to local SQLite
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./ffdraft.db")

engine_kwargs = {"pool_pre_ping": True}

# Only apply SQLite-specific connect args when using SQLite
try:
    url = make_url(SQLALCHEMY_DATABASE_URL)
    if url.drivername.startswith("sqlite"):
        engine_kwargs["connect_args"] = {"check_same_thread": False}
except Exception:
    # If parsing fails for any reason, just continue without sqlite tweaks
    pass

engine = create_engine(SQLALCHEMY_DATABASE_URL, **engine_kwargs)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


