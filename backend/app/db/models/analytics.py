from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Float
from sqlalchemy import Integer
from sqlalchemy import String
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

    event_type = Column(
        String,
        nullable=False,
    )

    latency = Column(
        Float,
        nullable=True,
    )

    provider = Column(
        String,
        nullable=True,
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
