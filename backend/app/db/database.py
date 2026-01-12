from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# SQLite database URL
DATABASE_URL = "mysql+pymysql://pikachu:dracaufeu2025@localhost:3306/poke_collect"

# Create engine
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for ORM models
Base = declarative_base()


# Optional: Initialize tables if needed
def init_db():
    Base.metadata.create_all(bind=engine)
