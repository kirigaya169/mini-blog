from main import app
from utils import db_session_dependency
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from models import Base

DB_URL = 'sqlite://'

engine = create_engine(DB_URL,
                       connect_args={'check_same_thread': False},
                       poolclass=StaticPool)

TestingSessionLocal = sessionmaker(autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)


def override_db_dependency():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[db_session_dependency] = override_db_dependency

client = TestClient(app)
