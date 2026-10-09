from fastapi import APIRouter

from app.database.auth import create_session, create_user
from app.models.auth import AccountCredentials, AuthResponse


router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=AuthResponse)
def register(credentials: AccountCredentials) -> AuthResponse:
    user = create_user(credentials.email, credentials.password)
    token, _ = create_session(credentials.email, credentials.password)
    return AuthResponse(token=token, user=user)


@router.post("/login", response_model=AuthResponse)
def login(credentials: AccountCredentials) -> AuthResponse:
    token, user = create_session(credentials.email, credentials.password)
    return AuthResponse(token=token, user=user)
