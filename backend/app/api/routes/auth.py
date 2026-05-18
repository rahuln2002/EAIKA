from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.api.dependencies.database import (
    get_db,
)
from app.db.schemas.auth_schema import (
    TokenResponse,
    UserCreate,
    UserLogin,
)
from app.services.auth.auth_service import (
    AuthService,
)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post("/signup")
async def signup(
    user: UserCreate,
    db: Session = Depends(get_db),
):
    """
    Register new user.
    """

    try:
        created_user = AuthService.register_user(
            db,
            user,
        )

        return {
            "message": "User created successfully.",
            "email": created_user.email,
        }

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


@router.post(
    "/login",
    response_model=TokenResponse,
)
async def login(
    user: UserLogin,
    db: Session = Depends(get_db),
):
    """
    Authenticate user.
    """

    try:
        access_token = AuthService.authenticate_user(
            db,
            user,
        )

        return TokenResponse(access_token=access_token)

    except ValueError as e:
        raise HTTPException(
            status_code=401,
            detail=str(e),
        )
