
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,DeclarativeBase
from sqlalchemy.ext.declarative import declarative_base


DB_NAME = "dummy_test"
DB_USER = "postgres"
DB_PASSWORD = "g"
DB_HOST = "localhost"

SQLALCHEMY_DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:5432/{DB_NAME}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)

class Base(DeclarativeBase):
    pass

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close

