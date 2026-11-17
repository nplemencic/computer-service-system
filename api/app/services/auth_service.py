from sqlalchemy.orm import Session

from app.core.errors import AppError
from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    verify_password,
)
from app.models.user import User
from app.repositories.user_repository import get_user_by_username


def authenticate_user(
    db: Session,
    username: str,
    password: str,
) -> User:
    """
    Provjerava lozinku. Nepostojeći korisnik, kriva lozinka i
    deaktiviran račun daju isti odgovor, da se ne odaje koji računi postoje.
    """

    user = get_user_by_username(db, username)

    if (
        not user
        or not user.is_active
        or not verify_password(password, user.password_hash)
    ):
        raise AppError(
            "invalid_credentials",
            "Neispravno korisničko ime ili lozinka",
            401,
        )

    return user


def create_tokens(user: User) -> tuple[str, str]:
    """
    Izdaje par access i refresh tokena.
    """

    return (
        create_access_token(user.username),
        create_refresh_token(user.username),
    )


def refresh_tokens(
    db: Session,
    refresh_token: str,
) -> tuple[str, str]:
    """
    Iz valjanog refresh tokena izdaje novi par tokena.
    Svaka neuspjela obnova daje isti odgovor, pa klijent zna da se mora
    ponovno prijaviti.
    """

    try:
        username = decode_token(refresh_token, "refresh")
    except AppError:
        raise AppError(
            "invalid_credentials",
            "Refresh token ne vrijedi",
            401,
        )

    user = get_user_by_username(db, username)

    if not user or not user.is_active:
        raise AppError(
            "invalid_credentials",
            "Refresh token ne vrijedi",
            401,
        )

    return create_tokens(user)
