import bcrypt


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