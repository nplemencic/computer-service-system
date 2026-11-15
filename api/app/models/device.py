from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Device(Base):
    """
    Uređaj korisnika koji se može poslati na servis.
    """

    __tablename__ = "devices"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

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
        default=datetime.utcnow,
        nullable=False,
    )

    # Jedan uređaj pripada jednom korisniku
    owner = relationship(
        "User",
        back_populates="devices",
    )