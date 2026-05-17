from datetime import datetime

from pydantic import BaseModel, ConfigDict

# =========================================================
# CHAT CREATE
# =========================================================


class ChatCreate(BaseModel):
    title: str


# =========================================================
# MESSAGE CREATE
# =========================================================


class MessageCreate(BaseModel):
    content: str


# =========================================================
# MESSAGE RESPONSE
# =========================================================


class MessageResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    id: int
    role: str
    content: str
    created_at: datetime


# =========================================================
# CHAT RESPONSE
# =========================================================


class ChatResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    id: int
    title: str
    created_at: datetime
