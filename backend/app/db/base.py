from app.db.base_class import Base

# =============================================
# IMPORT ALL MODELS
# =============================================

from app.db.models.analytics import Analytics
from app.db.models.chat import Chat
from app.db.models.chunk import Chunk
from app.db.models.document import Document
from app.db.models.message import Message
from app.db.models.user import User

__all__ = [
    "Base",
    "User",
    "Chat",
    "Message",
    "Document",
    "Chunk",
    "Analytics",
]
