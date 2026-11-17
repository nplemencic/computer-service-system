from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.deps import get_db
from app.schemas.user import (
    LoginRequest,
    TokenResponse,
    UserResponse,
    TokenPairResponse,
    RefreshTokenRequest,
)
from app.services.auth_service import authenticate_user

from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_refresh_token,
)

from app.core.deps import get_current_user
from app.models.user import User
from app.core.deps import require_technician

router = APIRouter()


@router.post(
    "/login",
    response_model=TokenPairResponse,
)
def login(
    data: LoginRequest,
    db: Session = Depends(get_db),
):
    """
    Prijava korisnika.
    """

    user = authenticate_user(
        db,
        data.username,
        data.password,
    )

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials",
        )

    access_token = create_access_token(
        user.username,
    )

    refresh_token = create_refresh_token(
    user.username,
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }

@router.get(
    "/me",
    response_model=UserResponse,
)
def get_me(
    current_user: User = Depends(
        get_current_user
    ),
):
    """
    Vraća trenutno prijavljenog korisnika.
    """

    return current_user

@router.get("/technician-only")
def technician_only(
    current_user: User = Depends(
        require_technician
    ),
):
    """
    Test endpoint dostupan samo tehničaru.
    """

    return {
        "message": "Technician access granted"
    }

@router.post(
    "/refresh",
    response_model=TokenResponse,
)
def refresh_token(
    data: RefreshTokenRequest,
):
    """
    Stvara novi access token iz refresh tokena.
    """

    username = decode_refresh_token(
        data.refresh_token,
    )

    if not username:
        raise HTTPException(
            status_code=401,
            detail="Invalid refresh token",
        )

    access_token = create_access_token(
        username,
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }

