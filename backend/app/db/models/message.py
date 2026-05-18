from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy.orm import relationship

from app.db.base import Base


class Message(Base):
    """
    Chat message model.
    """

    __tablename__ = "messages"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    role = Column(
        String,
        nullable=False,
    )

    content = Column(
        Text,
        nullable=False,
    )

    chat_id = Column(
        Integer,
        ForeignKey("chats.id"),
    )

    # =====================================================
    # RELATIONSHIPS
    # =====================================================

    chat = relationship(
        "Chat",
        back_populates="messages",
    )
