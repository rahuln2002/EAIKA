from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Analytics(Base):
    __tablename__ = "analytics"

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

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
    )

    # =========================================================
    # METRICS
    # =========================================================

    total_queries: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    documents_uploaded: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    # =========================================================
    # TIMESTAMP
    # =========================================================

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )
