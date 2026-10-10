from fastapi import (
    Depends,
    HTTPException,
    status,
)

from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
)

from app.database.auth import (
    get_user_from_token,
)


security = HTTPBearer(
    auto_error=False
)


def get_current_token(
    credentials: HTTPAuthorizationCredentials
    | None = Depends(security)
) -> str:

    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required."
        )

    return credentials.credentials


def get_current_user(
    token: str = Depends(
        get_current_token
    )
) -> dict[str, str]:

    user = get_user_from_token(
        token
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired session."
        )

    return user