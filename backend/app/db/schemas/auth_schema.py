from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field

# =========================================================
# USER CREATE
# =========================================================


class UserCreate(BaseModel):
    username: str = Field(
        min_length=3,
        max_length=50,
    )

    email: EmailStr

    password: str = Field(
        min_length=8,
        max_length=128,
    )


# =========================================================
# USER LOGIN
# =========================================================


class UserLogin(BaseModel):
    email: EmailStr

    password: str


# =========================================================
# TOKEN RESPONSE
# =========================================================


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


# =========================================================
# USER RESPONSE
# =========================================================


class UserResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    id: int
    username: str
    email: str
    is_admin: bool
    is_active: bool
    created_at: datetime
