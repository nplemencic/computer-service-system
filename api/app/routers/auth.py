from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.deps import get_current_user, get_db
from app.models.user import User
from app.schemas.user import (
    LoginRequest,
    RefreshTokenRequest,
    TokenPairResponse,
    UserResponse,
)
from app.services.auth_service import (
    authenticate_user,
    create_tokens,
    refresh_tokens,
)

router = APIRouter()


@router.post("/login", response_model=TokenPairResponse)
def login(
    data: LoginRequest,
    db: Session = Depends(get_db),
):
    """
    Prijava korisnika; vraća access i refresh token.
    """

    user = authenticate_user(db, data.username, data.password)
    access_token, refresh_token = create_tokens(user)

    return TokenPairResponse(
        access_token=access_token,
        refresh_token=refresh_token,
    )


@router.post("/refresh", response_model=TokenPairResponse)
def refresh(
    data: RefreshTokenRequest,
    db: Session = Depends(get_db),
):
    """
    Iz refresh tokena izdaje novi par tokena.
    """

    access_token, refresh_token = refresh_tokens(
        db,
        data.refresh_token,
    )

    return TokenPairResponse(
        access_token=access_token,
        refresh_token=refresh_token,
    )


@router.get("/me", response_model=UserResponse)
def get_me(
    current_user: User = Depends(get_current_user),
):
    """
    Vraća trenutno prijavljenog korisnika.
    """

    return current_user
