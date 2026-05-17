from fastapi import HTTPException, status


def require_admin(is_admin: bool) -> None:
    """
    Ensure user has admin permissions.
    """

    if not is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required.",
        )
