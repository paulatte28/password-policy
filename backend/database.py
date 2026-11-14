import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# Use SQLite only for local development. A deployed app must never silently
# switch databases if Supabase is unavailable.
if not DATABASE_URL:
    if os.getenv("VERCEL") or os.getenv("RENDER"):
        raise RuntimeError("DATABASE_URL is required for a deployed application")
    DATABASE_URL = "sqlite:///./passwordpolicy.db"
elif DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

try:
    engine = create_engine(DATABASE_URL, connect_args=connect_args, pool_pre_ping=True)
    # Quick connectivity test
    with engine.connect() as conn:
        pass
except Exception as e:
    raise RuntimeError("Could not connect to the configured database") from e

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
