from sqlalchemy.orm import Session

from app.core.security.jwt_handler import (
    create_access_token,
)
from app.core.security.password_handler import (
    hash_password,
    verify_password,
)
from app.db.models.user import User
from app.db.schemas.auth_schema import (
    UserCreate,
    UserLogin,
)


class AuthService:
    """
    Authentication service layer.
    """

    @staticmethod
    def register_user(
        db: Session,
        user_data: UserCreate,
    ) -> User:
        """
        Register new user.
        """

        existing_user = db.query(User).filter(User.email == user_data.email).first()

        if existing_user:
            raise ValueError("User already exists.")

        hashed_password = hash_password(user_data.password)

        user = User(
            username=user_data.username,
            email=user_data.email,
            hashed_password=hashed_password,
        )

        db.add(user)

        db.commit()

        db.refresh(user)

        return user

    @staticmethod
    def authenticate_user(
        db: Session,
        user_data: UserLogin,
    ) -> str:
        """
        Authenticate user and return JWT.
        """

        user = db.query(User).filter(User.email == user_data.email).first()

        if not user:
            raise ValueError("Invalid credentials.")

        if not verify_password(
            user_data.password,
            user.hashed_password,
        ):
            raise ValueError("Invalid credentials.")

        access_token = create_access_token(
            {
                "sub": user.email,
            }
        )

        return access_token
