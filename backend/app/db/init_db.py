from app.db.base import Base
from app.db.session import engine

# IMPORTANT:
# Import models here later
# Example:
# from app.db.models.user import User


def init_db() -> None:
    """
    Initialize database tables.
    """

    Base.metadata.create_all(bind=engine)
