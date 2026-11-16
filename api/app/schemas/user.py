from datetime import datetime

from pydantic import BaseModel


class UserResponse(BaseModel):
    """
    Podaci o korisniku koje vraćamo klijentu.
    """

    id: int
    username: str
    role: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

class LoginRequest(BaseModel):
    """
    Podaci za prijavu korisnika.
    """

    username: str
    password: str

class TokenResponse(BaseModel):
    """
    JWT token koji vraća API nakon uspješne prijave.
    """

    access_token: str
    token_type: str

class TokenData(BaseModel):
    """
    Podaci iz JWT tokena.
    """

    username: str