from datetime import UTC, datetime, timedelta

import bcrypt
from jose import JWTError, jwt
from jose.exceptions import ExpiredSignatureError

from app.core.config import settings
from app.core.errors import AppError

ALGORITHM = "HS256"


def hash_password(password: str) -> str:
    """
    Stvara bcrypt hash lozinke (salt je dio samog zapisa).
    """

    hashed = bcrypt.hashpw(
        password.encode(),
        bcrypt.gensalt(),
    )

    return hashed.decode()


def verify_password(
    password: str,
    password_hash: str,
) -> bool:
    """
    Provjerava odgovara li lozinka hash vrijednosti.
    """

    try:
        return bcrypt.checkpw(
            password.encode(),
            password_hash.encode(),
        )
    except ValueError:
        # bcrypt 5 odbija lozinke dulje od 72 bajta
        return False


def _create_token(
    subject: str,
    token_type: str,
    expires_delta: timedelta,
) -> str:
    payload = {
        "sub": subject,
        "type": token_type,
        "exp": datetime.now(UTC) + expires_delta,
    }

    return jwt.encode(
        payload,
        settings.JWT_SECRET,
        algorithm=ALGORITHM,
    )


def create_access_token(subject: str) -> str:
    """
    Stvara kratkotrajni JWT access token.
    """

    return _create_token(
        subject,
        "access",
        timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    )


def create_refresh_token(subject: str) -> str:
    """
    Stvara dugotrajni JWT refresh token.
    """

    return _create_token(
        subject,
        "refresh",
        timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
    )


def decode_token(token: str, token_type: str) -> str:
    """
    Dekodira token i vraća `sub` (korisničko ime).

    Odbija istekao token (token_expired), neispravan potpis i token
    krive vrste, npr. refresh token poslan kao access (invalid_credentials).
    """

    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[ALGORITHM],
        )
    except ExpiredSignatureError:
        raise AppError(
            "token_expired",
            "Token je istekao",
            401,
        )
    except JWTError:
        raise AppError(
            "invalid_credentials",
            "Neispravan token",
            401,
        )

    if payload.get("type") != token_type:
        raise AppError(
            "invalid_credentials",
            "Neispravna vrsta tokena",
            401,
        )

    subject = payload.get("sub")

    if not subject:
        raise AppError(
            "invalid_credentials",
            "Neispravan token",
            401,
        )

    return subject
