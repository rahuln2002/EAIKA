from datetime import datetime

from typing import Optional

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


class FaithfulnessResponse(BaseModel):
    faithfulness_score: float
    matched_terms: int
    total_terms: int


class HallucinationResponse(BaseModel):
    hallucination_score: float
    hallucinated_terms: list[str]


class RelevancyResponse(BaseModel):
    avg_relevancy_score: float


class RetrievalMetricsResponse(BaseModel):
    retrieved_chunks: int
    avg_chunk_length: float


class EvaluationResponse(BaseModel):
    faithfulness: FaithfulnessResponse
    hallucination: HallucinationResponse
    relevancy: RelevancyResponse
    retrieval_metrics: RetrievalMetricsResponse


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
