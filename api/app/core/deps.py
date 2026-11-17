from app.core.database import SessionLocal

from app.core.exceptions import ApiException

from fastapi import Depends, HTTPException
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
)

from sqlalchemy.orm import Session
from app.core.security import decode_access_token
from app.repositories.user_repository import get_user_by_username
from app.models.user import User

from app.repositories.device_repository import (
    get_device_by_id,
)


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

def require_technician(
    current_user: User = Depends(
        get_current_user
    ),
):
    """
    Dozvoljava pristup samo tehničarima.
    """

    if current_user.role != "technician":
        raise ApiException(
            status_code=403,
            code="ACCESS_DENIED",
            message="Access denied",
        )

    return current_user

def require_device_owner(
    device_id: int,
    current_user: User = Depends(
        get_current_user
    ),
    db: Session = Depends(get_db),
):
    """
    Provjerava je li korisnik vlasnik uređaja.
    """

    device = get_device_by_id(
        db,
        device_id,
    )

    if not device:
        raise HTTPException(
            status_code=404,
            detail="Device not found",
        )

    if device.owner_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Access denied",
        )

    return device