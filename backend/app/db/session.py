from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config.settings import settings

# =========================================================
# DATABASE ENGINE
# =========================================================

database_url = settings.DATABASE_URL

# ============================================
# FIX RAILWAY POSTGRES URL
# ============================================

if database_url.startswith("postgres://"):
    database_url = database_url.replace(
        "postgres://",
        "postgresql://",
        1,
    )

engine = create_engine(
    database_url,
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
