from app.core.database import SessionLocal

from fastapi import Depends, HTTPException
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
)

from sqlalchemy.orm import Session

from app.core.security import decode_access_token

from app.repositories.user_repository import get_user_by_username


# Bearer token autentikacija
bearer_scheme = HTTPBearer()

def get_db():
    """
    Otvara sesiju baze za jedan HTTP zahtjev.
    """
    db = SessionLocal()

    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(
        bearer_scheme
    ),
    db: Session = Depends(get_db),
):
    """
    Dohvaća trenutno prijavljenog korisnika
    iz JWT tokena.
    """
    # JWT token iz Authorization headera
    token = credentials.credentials

    # Izvuci username iz tokena
    username = decode_access_token(token)

    if not username:
        raise HTTPException(
            status_code=401,
            detail="Invalid token",
        )

    # Potraži korisnika u bazi
    user = get_user_by_username(
        db,
        username,
    )

    if not user:
        raise HTTPException(
            status_code=401,
            detail="User not found",
        )

    return user