from sqlalchemy import create_engine
from sqlalchemy.orm import create_session
from config import DATABASE_URL


engine = create_engine(DATABASE_URL, echo=True)

SessionLocal = create_session(bind=engine, autocommit=False, autoflush=False)


def get_db():
    session = SessionLocal
    try:
        yield session
    finally:
        session.close()


