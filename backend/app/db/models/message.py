from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Message(Base):
    __tablename__ = "messages"

    # =========================================================
    # PRIMARY KEY
    # =========================================================

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    # =========================================================
    # FOREIGN KEY
    # =========================================================

    chat_id: Mapped[int] = mapped_column(
        ForeignKey("chats.id"),
        nullable=False,
    )

    # =========================================================
    # MESSAGE DATA
    # =========================================================

    role: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    content: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    # =========================================================
    # TIMESTAMP
    # =========================================================

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    # =========================================================
    # RELATIONSHIPS
    # =========================================================

    chat = relationship(
        "Chat",
        back_populates="messages",
    )
