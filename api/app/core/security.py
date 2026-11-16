import bcrypt

from datetime import datetime, timedelta, UTC

from jose import jwt

from app.core.config import settings

from jose import JWTError


def hash_password(password: str) -> str:
    """
    Stvara bcrypt hash lozinke.
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

    return bcrypt.checkpw(
        password.encode(),
        password_hash.encode(),
    )

def create_access_token(
    subject: str,
) -> str:
    """
    Stvara JWT access token.
    """

    expires_at = datetime.now(UTC) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload = {
        "sub": subject,
        "exp": expires_at,
    }

    return jwt.encode(
        payload,
        settings.JWT_SECRET,
        algorithm="HS256",
    )

def decode_access_token(
    token: str,
) -> str | None:
    """
    Dekodira JWT token.
    """

    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=["HS256"],
        )

        return payload.get

    except JWTError:
        return None