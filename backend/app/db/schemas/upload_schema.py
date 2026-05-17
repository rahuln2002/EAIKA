from datetime import datetime

from pydantic import BaseModel, ConfigDict

# =========================================================
# DOCUMENT RESPONSE
# =========================================================


class DocumentResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    id: int
    filename: str
    file_type: str
    file_size: int
    status: str
    uploaded_at: datetime
