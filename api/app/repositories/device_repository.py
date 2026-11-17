from sqlalchemy.orm import Session

from app.models.device import Device


def get_device_by_id(
    db: Session,
    device_id: int,
) -> Device | None:
    """
    Dohvaća uređaj prema ID-u.
    """

    return (
        db.query(Device)
        .filter(Device.id == device_id)
        .first()
    )

def create_device(
    db: Session,
    device: Device,
) -> Device:
    """
    Sprema novi uređaj u bazu.
    """

    db.add(device)

    db.commit()

    db.refresh(device)

    return device

def get_devices_by_owner(
    db: Session,
    owner_id: int,
    limit: int,
    offset: int,
):
    """
    Dohvaća uređaje korisnika uz straničenje.
    """

    return (
        db.query(Device)
        .filter(Device.owner_id == owner_id)
        .offset(offset)
        .limit(limit)
        .all()
    )