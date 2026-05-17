from fastapi import APIRouter, HTTPException

from app.core.security.jwt_handler import (
    create_access_token,
)
from app.core.security.password_handler import (
    hash_password,
    verify_password,
)
from app.db.schemas.auth_schema import (
    TokenResponse,
    UserCreate,
    UserLogin,
)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)

# =========================================================
# TEMP USER STORE
# =========================================================

fake_users_db = {}


@router.post(
    "/signup",
)
async def signup(
    user: UserCreate,
):
    """
    Register new user.
    """

    if user.email in fake_users_db:
        raise HTTPException(
            status_code=400,
            detail="User already exists.",
        )

    hashed_password = hash_password(user.password)

    fake_users_db[user.email] = {
        "username": user.username,
        "email": user.email,
        "hashed_password": hashed_password,
    }

    return {
        "message": "User created successfully.",
    }


@router.post(
    "/login",
    response_model=TokenResponse,
)
async def login(
    user: UserLogin,
):
    """
    Authenticate user.
    """

    db_user = fake_users_db.get(user.email)

    if not db_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials.",
        )

    if not verify_password(
        user.password,
        db_user["hashed_password"],
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials.",
        )

    access_token = create_access_token(
        {
            "sub": user.email,
        }
    )

    return TokenResponse(access_token=access_token)
