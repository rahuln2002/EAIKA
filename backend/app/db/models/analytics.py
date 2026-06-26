from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy.sql import func

from app.db.base import Base


class Analytics(Base):
    """
    Analytics tracking model.
    """

    __tablename__ = "analytics"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    event_type = Column(
        String,
        nullable=False,
        default="chat",
    )

    provider = Column(
        String,
        nullable=True,
    )

    query = Column(
        Text,
        nullable=False,
    )

    latency = Column(
        Float,
        nullable=False,
    )

    retrieval_latency = Column(
        Float,
        nullable=True,
    )

    history_latency = Column(
        Float,
        nullable=True,
    )

    llm_latency = Column(
        Float,
        nullable=True,
    )

    retrieved_chunks = Column(
        Integer,
        nullable=False,
        default=0,
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
