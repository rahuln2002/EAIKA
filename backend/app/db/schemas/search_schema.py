from pydantic import BaseModel

# =========================================================
# SEARCH REQUEST
# =========================================================


class SearchRequest(BaseModel):
    query: str


# =========================================================
# SEARCH RESULT
# =========================================================


class SearchResult(BaseModel):
    chunk_text: str
    score: float
    document_id: int


# =========================================================
# SEARCH RESPONSE
# =========================================================


class SearchResponse(BaseModel):
    results: list[SearchResult]
