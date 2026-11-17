from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.errors import AppError
from app.models.device import Device
from app.models.user import User
from app.repositories.device_repository import (
    create_device,
    get_device_by_id,
    get_devices_by_owner,
)


def create_user_device(
    db: Session,
    owner_id: int,
    manufacturer: str,
    model: str,
    serial_number: str,
) -> Device:
    """
    Kreira uređaj za korisnika. Serijski broj je jedinstven;
    jedinstvenost provodi baza, a njezinu iznimku prevodimo u 409.
    """

    device = Device(
        owner_id=owner_id,
        manufacturer=manufacturer,
        model=model,
        serial_number=serial_number,
    )

    try:
        return create_device(db, device)
    except IntegrityError:
        db.rollback()
        raise AppError(
            "duplicate",
            "Uređaj s tim serijskim brojem već postoji",
            409,
        )


def get_user_devices(
    db: Session,
    owner_id: int,
    limit: int,
    offset: int,
) -> list[Device]:
    """
    Dohvaća uređaje korisnika uz straničenje.
    """

    return get_devices_by_owner(db, owner_id, limit, offset)


def get_user_device(
    db: Session,
    device_id: int,
    user: User,
) -> Device:
    """
    Vraća uređaj samo njegovu vlasniku. Tuđi uređaj izgleda isto kao
    nepostojeći (404), da se ne odaje koji zapisi postoje.
    """

    device = get_device_by_id(db, device_id)

    if not device or device.owner_id != user.id:
        raise AppError(
            "not_found",
            "Uređaj ne postoji",
            404,
        )

    return device
