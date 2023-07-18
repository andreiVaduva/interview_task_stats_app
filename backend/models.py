""" This module contains the database ORM models. """
from datetime import datetime
from uuid import uuid4

from sqlalchemy import UUID
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from .database import Base


class Message(Base):
    __tablename__ = 'message'

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    customer_id: Mapped[int]
    message_type: Mapped[str]
    amount: Mapped[float]
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
