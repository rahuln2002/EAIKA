from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import Text
from sqlalchemy.orm import relationship

from app.db.base import Base


class Chunk(Base):
    """
    Document chunk model.
    """

    __tablename__ = "chunks"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    content = Column(
        Text,
        nullable=False,
    )

    chunk_index = Column(
        Integer,
        nullable=False,
    )

    document_id = Column(
        Integer,
        ForeignKey("documents.id"),
    )

    # =====================================================
    # RELATIONSHIPS
    # =====================================================

    document = relationship(
        "Document",
        back_populates="chunks",
    )
