from app.db.base import Base
from app.db.models.analytics import Analytics  # noqa: F401
from app.db.models.chat import Chat  # noqa: F401
from app.db.models.chunk import Chunk  # noqa: F401
from app.db.models.document import Document  # noqa: F401
from app.db.models.message import Message  # noqa: F401
from app.db.models.user import User  # noqa: F401
from app.db.session import engine


def init_db() -> None:
    """
    Initialize database tables.
    """

    Base.metadata.create_all(bind=engine)
