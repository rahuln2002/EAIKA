from datetime import datetime

from typing import Optional
from typing import Any

from pydantic import (
    BaseModel,
    ConfigDict,
)

# =========================================================
# CHAT CREATE
# =========================================================


class ChatCreate(BaseModel):
    title: str


# =========================================================
# CHAT REQUEST
# =========================================================


class ChatRequest(BaseModel):
    query: str

    chat_id: Optional[int] = None


# =========================================================
# MESSAGE CREATE
# =========================================================


class MessageCreate(BaseModel):
    content: str


# =========================================================
# SOURCE RESPONSE
# =========================================================


class SourceResponse(BaseModel):
    chunk_id: int

    document_id: int

    citation: str

    content: str


# =========================================================
# EVALUATION RESPONSE
# =========================================================


class EvaluationResponse(BaseModel):
    faithfulness: float

    hallucination: float

    relevancy: float

    retrieval_metrics: dict[str, Any]


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


# =========================================================
# CONVERSATIONAL CHAT RESPONSE
# =========================================================


class ConversationalChatResponse(BaseModel):
    chat_id: int

    answer: str

    sources: list[SourceResponse]

    evaluation: EvaluationResponse


# =========================================================
# CHAT HISTORY RESPONSE
# =========================================================


class ChatHistoryResponse(BaseModel):
    chat_id: int

    messages: list[MessageResponse]


# =========================================================
# CHAT LIST RESPONSE
# =========================================================


class ChatListResponse(BaseModel):
    id: int

    title: str

    created_at: datetime
