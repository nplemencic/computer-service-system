from app.models.device import Device
from app.repositories.device_repository import (
    create_device,
    get_devices_by_owner,
)


def create_user_device(
    db,
    owner_id: int,
    manufacturer: str,
    model: str,
    serial_number: str,
) -> Device:
    """
    Kreira uređaj za korisnika.
    """

    device = Device(
        owner_id=owner_id,
        manufacturer=manufacturer,
        model=model,
        serial_number=serial_number,
    )

    return create_device(
        db,
        device,
    )


def get_user_devices(
    db,
    owner_id: int,
):
    """
    Dohvaća sve uređaje korisnika.
    """

    return get_devices_by_owner(
        db,
        owner_id,
    )