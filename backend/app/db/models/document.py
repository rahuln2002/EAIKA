from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import Base


class Document(Base):
    """
    Uploaded document model.
    """

    __tablename__ = "documents"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    filename = Column(
        String,
        nullable=False,
    )

    file_path = Column(
        String,
        nullable=False,
    )

    owner_id = Column(
        Integer,
        ForeignKey("users.id"),
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    # =====================================================
    # RELATIONSHIPS
    # =====================================================

    owner = relationship(
        "User",
        back_populates="documents",
    )

    chunks = relationship(
        "Chunk",
        back_populates="document",
        cascade="all, delete-orphan",
    )
