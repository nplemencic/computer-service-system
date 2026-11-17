from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.core.security import hash_password
from app.models.device import Device
from app.models.service_request import ServiceRequest
from app.models.user import User


def get_or_create_user(
    db: Session,
    username: str,
    password: str,
    role: str,
) -> User:
    user = db.query(User).filter(User.username == username).first()

    if user:
        return user

    user = User(
        username=username,
        password_hash=hash_password(password),
        role=role,
    )
    db.add(user)
    db.flush()

    return user


def get_or_create_device(
    db: Session,
    owner: User,
    manufacturer: str,
    model: str,
    serial_number: str,
) -> Device:
    device = db.query(Device).filter(Device.serial_number == serial_number).first()

    if device:
        return device

    device = Device(
        owner_id=owner.id,
        manufacturer=manufacturer,
        model=model,
        serial_number=serial_number,
    )
    db.add(device)
    db.flush()

    return device


def get_or_create_request(
    db: Session,
    device: Device,
    title: str,
    description: str,
    status: str,
) -> ServiceRequest:
    request = (
        db.query(ServiceRequest)
        .filter(ServiceRequest.device_id == device.id)
        .filter(ServiceRequest.title == title)
        .first()
    )

    if request:
        return request

    request = ServiceRequest(
        device_id=device.id,
        title=title,
        description=description,
        status=status,
    )
    db.add(request)
    db.flush()

    return request


def seed() -> None:
    """
    Upisuje početne podatke. Smije se pokrenuti više puta:
    ono što već postoji ne stvara se ponovno.
    """

    with SessionLocal() as db:
        get_or_create_user(db, "technician", "test123", "technician")
        customer1 = get_or_create_user(db, "customer1", "test123", "customer")
        customer2 = get_or_create_user(db, "customer2", "test123", "customer")

        dell = get_or_create_device(db, customer1, "Dell", "Latitude 5520", "DELL-001")
        hp = get_or_create_device(db, customer1, "HP", "ProBook 450", "HP-001")
        lenovo = get_or_create_device(
            db, customer2, "Lenovo", "ThinkPad T14", "LENOVO-001"
        )

        get_or_create_request(
            db,
            dell,
            "SSD upgrade",
            "Zamjena SSD diska na uređaju.",
            "OPEN",
        )
        get_or_create_request(
            db,
            hp,
            "Fan cleaning",
            "Čišćenje ventilatora i uklanjanje prašine.",
            "IN_PROGRESS",
        )
        get_or_create_request(
            db,
            lenovo,
            "RAM upgrade",
            "Nadogradnja radne memorije.",
            "COMPLETED",
        )

        db.commit()


if __name__ == "__main__":
    seed()
