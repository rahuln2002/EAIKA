from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Chunk(Base):
    __tablename__ = "chunks"

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

    document_id: Mapped[int] = mapped_column(
        ForeignKey("documents.id"),
        nullable=False,
    )

    # =========================================================
    # CHUNK DATA
    # =========================================================

    chunk_text: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    embedding_id: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    chunk_index: Mapped[int] = mapped_column(
        nullable=False,
    )

    # =========================================================
    # RELATIONSHIPS
    # =========================================================

    document = relationship(
        "Document",
        back_populates="chunks",
    )
