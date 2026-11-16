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