import os
import time

from dotenv import load_dotenv

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

load_dotenv()
DB_PASSWORD = os.environ.get('DB_PASSWORD')
DB_USER = os.environ.get('DB_USER')
DB_HOST = os.environ.get('DB_HOST')
DB_PORT = os.environ.get('DB_PORT')
DB_DATABASE = os.environ.get('DB_DATABASE')
while os.system("nc -z " + f'{DB_HOST} {DB_PORT}') != 0:
    time.sleep(0.1)
engine = create_engine(f'postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}')
Base.metadata.create_all(bind=engine)
SessionMaker = sessionmaker(autoflush=False, bind=engine)


def db_session_dependency():
    """
    Dependency for getting session object
    :return:
    """
    session = SessionMaker()
    try:
        yield session
    finally:
        session.close()
