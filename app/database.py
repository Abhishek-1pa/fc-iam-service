from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URL_DEV = 'postgresql://postgres:123qwe123qwe@localhost/forgecode'
engine = create_engine(
    SQLALCHEMY_DATABASE_URL_DEV
)

SessionLocal = sessionmaker(autocommit = False, autoflush=False,  bind=engine)

def get_db():
    db = SessionLocal()
    
    try:
        yield db
    finally:
        db.close()