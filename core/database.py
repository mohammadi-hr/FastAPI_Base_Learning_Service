from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///./sqlite.db"

# create the engin only once
engine = create_engine(
    DATABASE_URL,
    echo=True,  # prints sql queries (optional)
    # allow using across multiple threads, use only for sqlite
    connect_args={"check_same_thread": False},
    pool_pre_ping=True  # checks connection before using
)

# create a configured Session class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# base class for models
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
