""" Tools for populating the database with example messages.
    The function 'run' performs the fill action, and it allows two modes:
      1. pre-defined data (default)
      2. random data
"""
import random
from datetime import datetime

from sqlalchemy import insert
from sqlalchemy.orm import Session

from .database import engine
from .models import Message
from .schemas import MessageType


# This can be tweaked at will.
#
# NOTE:
#    Please be mindful as the messages are generated in memory,
#    and a higher number might cause issues. Tested locally with
#    1_000_000 entries and worked well, but this depends from case
#    to case, based on the local setup and available resources.
_MAX_RANDOM_MESSAGES_NR = 10_000


def _get_random_message() -> dict:
    """ Creates a message with random data.

    Returns (dict): message with random data
    """
    return {
        'customer_id': random.randint(1, 20),
        'message_type': random.choice(MessageType.get_all_values()),
        'amount': round(random.uniform(0, 100), 3),
        'created_at': datetime(
            random.randint(1900, 2022),
            random.randint(1, 12),
            # prevent issues when the number of days
            # exceeds the months actual number of days
            random.randint(1, 28),
            random.randint(0, 23),
            random.randint(0, 59),
            random.randint(0, 59),
        ),
    }


def run(
        use_random_messages: bool = False,
        random_messages_nr: int = _MAX_RANDOM_MESSAGES_NR,
) -> None:
    """ Populates the database with pre-defined or random messages.

    Args:
        use_random_messages (bool):
            If True it populates the db with random messages,
            if False it populates the db with pre-defined messages
            (default: False).
        random_messages_nr (int):
            maximum random messages to be created
    """
    if use_random_messages and isinstance(random_messages_nr, int) and random_messages_nr > 0:
        # NOTE:
        #    Using generators we can make this more memory efficient. This would allow
        #    generating the messages in batches of fixed sizes and storing them batch by batch.
        messages = []

        for _ in range(random_messages_nr):
            messages.append(_get_random_message())
    else:
        messages = [
            # customer_id: 1
            # message_type: 'first'
            {
                'customer_id': 1,
                'message_type': MessageType.FIRST.value,
                'amount': '1.000',
                'created_at': datetime(2000, 1, 1, 0, 0, 0),
            },
            {
                'customer_id': 1,
                'message_type': MessageType.FIRST.value,
                'amount': '2.000',
                'created_at': datetime(2000, 1, 5, 0, 0, 0),
            },
            {
                'customer_id': 1,
                'message_type': MessageType.FIRST.value,
                'amount': '3.000',
                'created_at': datetime(2000, 1, 10, 0, 0, 0),
            },
            {
                'customer_id': 1,
                'message_type': MessageType.FIRST.value,
                'amount': '1.000',
                'created_at': datetime(2000, 1, 15, 0, 0, 0),
            },
            # customer_id: 1
            # message_type: 'second'
            {
                'customer_id': 1,
                'message_type': MessageType.SECOND.value,
                'amount': '2.000',
                'created_at': datetime(2000, 1, 20, 0, 0, 0),
            },
            {
                'customer_id': 1,
                'message_type': MessageType.SECOND.value,
                'amount': '3.000',
                'created_at': datetime(2000, 1, 25, 0, 0, 0),
            },
            # customer_id: 2
            # message_type: 'first'
            {
                'customer_id': 2,
                'message_type': MessageType.FIRST.value,
                'amount': '1.000',
                'created_at': datetime(2000, 1, 15, 0, 0, 0),
            },
            # customer_id: 2
            # message_type: 'third'
            {
                'customer_id': 2,
                'message_type': MessageType.THIRD.value,
                'amount': '2.000',
                'created_at': datetime(2000, 1, 20, 0, 0, 0),
            },
            {
                'customer_id': 2,
                'message_type': MessageType.THIRD.value,
                'amount': '3.000',
                'created_at': datetime(2000, 1, 25, 0, 0, 0),
            },
        ]

    # bulk insert
    # This allows us to store the entries more efficiently,
    # reducing the database overhead and increasing the performance.
    with Session(engine) as session:
        session.execute(insert(Message), messages)
        session.commit()
