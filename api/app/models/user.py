from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, utc_now

if TYPE_CHECKING:
    from app.models.device import Device


class User(Base):
    """
    Korisnik sustava.
    """

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)

    # Jedinstveno korisničko ime za prijavu
    username: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
    )

    # Sprema se hash lozinke, ne sama lozinka
    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    # customer ili technician
    role: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=utc_now,
        nullable=False,
    )

    # Korisnik može imati više uređaja
    devices: Mapped[list["Device"]] = relationship(
        back_populates="owner",
    )
