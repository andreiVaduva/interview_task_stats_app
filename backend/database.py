""" This module contains the database configurations and the session maker. """
import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database configurations.
_POSTGRES_USER = os.getenv('POSTGRES_USER')
_POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
_POSTGRES_DB = os.getenv('POSTGRES_DB')
_DB_PORT = '5432'
_HOST_NAME = 'database'
# _HOST_NAME = '0.0.0.0'  # To run the backend outside docker, uncomment this line.
_SQLALCHEMY_DATABASE_URL = \
    f'postgresql://{_POSTGRES_USER}:{_POSTGRES_PASSWORD}@{_HOST_NAME}:{_DB_PORT}/{_POSTGRES_DB}'

engine = create_engine(_SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


def get_db():
    """ yields a database session. """
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
