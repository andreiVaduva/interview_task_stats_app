""" This module contains the pydantic models. """
from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, field_validator


class MessageType(str, Enum):
    """ Class that stores the allowed message types. """
    FIRST = 'first'
    SECOND = 'second'
    THIRD = 'third'

    @classmethod
    def get_all_values(cls):
        return [attr.value for attr in cls.__members__.values()]


class MessageBase(BaseModel):
    customer_id: int
    message_type: MessageType


class MessageCreate(MessageBase):
    amount: str

    @field_validator('amount')
    def amount_must_be_a_str_with_3_decimals(cls, v):
        """ Validator that checks the amount field.
            It must be a string representing a float with 3 decimal precision.
        """
        if not isinstance(v, str):
            raise ValueError('must be a string')

        try:
            float(v)
        except ValueError:
            raise ValueError('must be convertable to float')

        try:
            _, decimals = v.split('.')
        except ValueError:
            raise ValueError('must be a string with 3 decimals precision')

        if len(decimals) != 3:
            raise ValueError('must be a string with 3 decimals precision')

        return v


class Message(MessageBase):
    id: UUID
    amount: float
    created_at: datetime


class StatsParams(BaseModel):
    customer_id: int
    message_type: MessageType
    from_date: Optional[datetime] | None = None
    to_date: Optional[datetime] | None = None


class StatsResponse(StatsParams):
    total_count: int
    total_amount: float
