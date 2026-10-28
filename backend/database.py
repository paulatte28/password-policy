import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# Supabase / PostgreSQL or local SQLite fallback
if not DATABASE_URL:
    DATABASE_URL = "sqlite:///./passwordpolicy.db"
elif DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

try:
    engine = create_engine(DATABASE_URL, connect_args=connect_args)
    # Quick connectivity test
    with engine.connect() as conn:
        pass
except Exception as e:
    print(f"[Warning] Could not connect to primary DATABASE_URL ({e}). Falling back to local SQLite.")
    DATABASE_URL = "sqlite:///./passwordpolicy.db"
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
