from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config.settings import settings

# =========================================================
# DATABASE ENGINE
# =========================================================

engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
    echo=settings.DEBUG,
)

# =========================================================
# SESSION FACTORY
# =========================================================

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)
