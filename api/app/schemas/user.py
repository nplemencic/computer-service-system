from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class UserResponse(BaseModel):
    """
    Podaci o korisniku koje vraćamo klijentu (bez hasha lozinke).
    """

    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    role: str
    is_active: bool
    created_at: datetime


class LoginRequest(BaseModel):
    """
    Podaci za prijavu korisnika.
    """

    username: str = Field(min_length=1)
    password: str = Field(min_length=1)


class RefreshTokenRequest(BaseModel):
    """
    Refresh token poslan na obnovu.
    """

    refresh_token: str = Field(min_length=1)


class TokenPairResponse(BaseModel):
    """
    Access i refresh token.
    """

    access_token: str
    refresh_token: str
    token_type: str = "bearer"
