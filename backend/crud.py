""" This module contains the database operations. """
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from . import models, schemas


def create_message(db: Session, message: schemas.MessageCreate):
    """ Stores a message inside the database.

    Args:
        db (Session): database session
        message (schemas.MessageCreate): message to be stored

    Returns: The stored message.
    """
    db_message = models.Message(**message.model_dump())
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message


def get_stats(db: Session, stats_params: schemas.StatsParams):
    """ Retrieves the statistics based on the given parameters.

    Args:
        db (Session): database session
        stats_params (schemas.StatsParams): query parameters

    Returns: the required stats
    """

    # Build a select statement that computes both the total_count
    # and total_amount in one query. We build the query based on the
    # given filters (customer_id, message_type, from_date and to_date).
    # NOTE:
    #    The sum function returns None when no records match the query.
    #    To prevent this None value from causing issues at a later
    #    point, we use coalesce function that returns the first non-None
    #    value, in this case, the hardcoded value 0.
    query = select(
        func.count(models.Message.id),
        func.coalesce(
            func.sum(models.Message.amount),
            0,
        ),
    ).where(
        models.Message.customer_id == stats_params.customer_id,
        models.Message.message_type == stats_params.message_type,
    )

    if stats_params.from_date:
        query = query.where(models.Message.created_at >= stats_params.from_date)

    if stats_params.to_date:
        query = query.where(models.Message.created_at <= stats_params.to_date)

    result = db.execute(query).all()
    total_count, total_amount = result[0]

    return schemas.StatsResponse(
        customer_id=stats_params.customer_id,
        message_type=stats_params.message_type,
        from_date=stats_params.from_date,
        to_date=stats_params.to_date,
        total_count=total_count,
        # We use the function round to prevent floating point
        # calculation imprecision like:
        # >>> 0.011 + 0.2 + 0.011
        # 0.22200000000000003
        total_amount=round(total_amount, 3),
    )
