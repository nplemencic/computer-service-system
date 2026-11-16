from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.deps import get_db
from app.schemas.user import (
    LoginRequest,
    TokenResponse,
    UserResponse,
)
from app.services.auth_service import authenticate_user
from app.core.security import create_access_token
from app.core.deps import get_current_user
from app.models.user import User
from app.core.deps import require_technician

router = APIRouter()


@router.post(
    "/login",
    response_model=TokenResponse,
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

    return {
        "access_token": access_token,
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

