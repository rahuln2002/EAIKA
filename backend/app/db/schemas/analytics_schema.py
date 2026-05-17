from datetime import datetime

from pydantic import BaseModel, ConfigDict


class AnalyticsResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    total_queries: int
    documents_uploaded: int
    created_at: datetime
