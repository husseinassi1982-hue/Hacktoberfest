from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)

from app.api.dependencies import (
    get_current_token,
    get_current_user,
)

from app.database.auth import (
    create_session,
    create_user,
    delete_session,
)

from app.models.auth import (
    AccountCredentials,
    AuthResponse,
)


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post(
    "/register",
    response_model=AuthResponse
)
def register(
    credentials: AccountCredentials
) -> AuthResponse:

    try:
        user = create_user(
            credentials.email,
            credentials.password
        )

        token, _ = create_session(
            credentials.email,
            credentials.password
        )

        return AuthResponse(
            token=token,
            user=user
        )

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(error)
        ) from error


@router.post(
    "/login",
    response_model=AuthResponse
)
def login(
    credentials: AccountCredentials
) -> AuthResponse:

    try:
        token, user = create_session(
            credentials.email,
            credentials.password
        )

        return AuthResponse(
            token=token,
            user=user
        )

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(error)
        ) from error


@router.get("/me")
def me(
    user: dict[str, str] = Depends(
        get_current_user
    )
):
    return user


@router.post("/logout")
def logout(
    token: str = Depends(
        get_current_token
    ),
    user: dict[str, str] = Depends(
        get_current_user
    )
):

    delete_session(token)

    return {
        "message": "Logged out successfully."
    }