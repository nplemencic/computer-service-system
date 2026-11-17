from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, utc_now

if TYPE_CHECKING:
    from app.models.service_request import ServiceRequest
    from app.models.user import User


class Device(Base):
    """
    Uređaj korisnika koji se može poslati na servis.
    """

    __tablename__ = "devices"

    id: Mapped[int] = mapped_column(primary_key=True)

    # Vlasnik uređaja
    owner_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
    )

    manufacturer: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    model: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    serial_number: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=utc_now,
        nullable=False,
    )

    # Jedan uređaj pripada jednom korisniku
    owner: Mapped["User"] = relationship(
        back_populates="devices",
    )

    # Jedan uređaj može imati više servisnih zahtjeva
    service_requests: Mapped[list["ServiceRequest"]] = relationship(
        back_populates="device",
    )
