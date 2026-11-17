from fastapi import Depends
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
)
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.core.errors import AppError
from app.core.security import decode_token
from app.models.user import User
from app.repositories.user_repository import get_user_by_username

# auto_error=False: zaglavlje koje nedostaje obrađujemo sami,
# da odgovor ima isti oblik kao sve ostale pogreške
bearer_scheme = HTTPBearer(auto_error=False)


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
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> User:
    """
    Dohvaća prijavljenog korisnika iz access tokena.
    Zapis se čita iz baze pa deaktiviran račun gubi pristup odmah.
    """

    if credentials is None:
        raise AppError(
            "invalid_credentials",
            "Prijava je obavezna",
            401,
        )

    username = decode_token(credentials.credentials, "access")

    user = get_user_by_username(db, username)

    if not user or not user.is_active:
        raise AppError(
            "invalid_credentials",
            "Korisnik ne postoji ili nije aktivan",
            401,
        )

    return user


def require_technician(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    Dozvoljava pristup samo tehničarima.
    """

    if current_user.role != "technician":
        raise AppError(
            "forbidden",
            "Nemate ovlasti za ovu radnju",
            403,
        )

    return current_user
