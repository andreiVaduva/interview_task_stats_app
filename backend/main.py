""" The main module:
      - creates the database
      - populates the database
      - creates the FastAPI app

    This module also contains the following RestAPI routes:
      - POST /messages - adds a message to the database
      - GET /stats - retrieves the required stats
"""
from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from . import crud, fill_db, models, schemas
from .database import engine, get_db


# Create the database.
#
# NOTE:
#     This approach does not support database migrations. To support
#     this feature, the database must be created with tools like alembic.
models.Base.metadata.create_all(bind=engine)

# Populate the database (default: uses pre-defined messages).
#
# Available options:
#   1. POPULATE DATABASE WITH PRE-DEFINED MESSAGES (default)
#        action: None
#        result: fill the database with pre-defined messages
#   2. KEEP DATABASE EMPTY
#        action: before starting the application comment the line below
#        result: empty database that can be populated at a later point
#   3. POPULATE DATABASE WITH RANDOM MESSAGES
#        action: use the parameters
#               (use_random_messages=True, random_messages_nr=100)
#        result: fill the database with the given number of random messages
#                (100 is the maximum allowed currently - can be changed)
fill_db.run(use_random_messages=False)

# Create the FastAPI app.
app = FastAPI()


@app.post('/messages', response_model=schemas.Message)
def create_message(message: schemas.MessageCreate, db: Session = Depends(get_db)):
    """ Creates a message in the database.

    Args:
        message (schemas.MessageCreate): the message
        db (Session): database session

    Returns (schemas.Message): the new message created
    """
    return crud.create_message(db, message)


@app.get('/stats', response_model=schemas.StatsResponse)
def get_stats(stats_params: schemas.StatsParams = Depends(), db: Session = Depends(get_db)):
    """ Retrieves the required stats.

    Args:
        stats_params (schemas.Stats): query parameters
        db (Session): database session

    Returns (schemas.StatsResponse): the required stats
    """
    return crud.get_stats(db, stats_params)
