from app.core.db_init import get_session

from app.models.user import User
from app.models.device import Device
from app.models.service_request import ServiceRequest


def create_users() -> None:
    """
    Stvara početne korisnike ako već ne postoje.
    """

    db = get_session()

    try:
        users = [
            {
                "username": "technician",
                "password_hash": "seed-password",
                "role": "technician",
            },
            {
                "username": "customer1",
                "password_hash": "seed-password",
                "role": "customer",
            },
            {
                "username": "customer2",
                "password_hash": "seed-password",
                "role": "customer",
            },
        ]

        for user_data in users:
            existing_user = (
                db.query(User)
                .filter(User.username == user_data["username"])
                .first()
            )

            if existing_user:
                continue

            db.add(User(**user_data))

        db.commit()

    finally:
        db.close()

def create_devices() -> None:
    """
    Stvara početne uređaje ako već ne postoje.
    """

    db = get_session()

    try:
        customer1 = (
            db.query(User)
            .filter(User.username == "customer1")
            .first()
        )

        customer2 = (
            db.query(User)
            .filter(User.username == "customer2")
            .first()
        )

        devices = [
            {
                "owner_id": customer1.id,
                "manufacturer": "Dell",
                "model": "Latitude 5520",
                "serial_number": "DELL-001",
            },
            {
                "owner_id": customer1.id,
                "manufacturer": "HP",
                "model": "ProBook 450",
                "serial_number": "HP-001",
            },
            {
                "owner_id": customer2.id,
                "manufacturer": "Lenovo",
                "model": "ThinkPad T14",
                "serial_number": "LENOVO-001",
            },
        ]

        for device_data in devices:
            existing_device = (
                db.query(Device)
                .filter(
                    Device.serial_number
                    == device_data["serial_number"]
                )
                .first()
            )

            if existing_device:
                continue

            db.add(Device(**device_data))

        db.commit()

    finally:
        db.close()  

def create_service_requests() -> None:
    """
    Stvara početne servisne zahtjeve.
    """

    db = get_session()

    try:
        dell = (
            db.query(Device)
            .filter(Device.serial_number == "DELL-001")
            .first()
        )

        hp = (
            db.query(Device)
            .filter(Device.serial_number == "HP-001")
            .first()
        )

        lenovo = (
            db.query(Device)
            .filter(Device.serial_number == "LENOVO-001")
            .first()
        )

        requests = [
            {
                "device_id": dell.id,
                "title": "SSD upgrade",
                "description": "Zamjena SSD diska na uređaju.",
                "status": "OPEN",
            },
            {
                "device_id": hp.id,
                "title": "Fan cleaning",
                "description": "Čišćenje ventilatora i uklanjanje prašine.",
                "status": "IN_PROGRESS",
            },
            {
                "device_id": lenovo.id,
                "title": "RAM upgrade",
                "description": "Nadogradnja radne memorije.",
                "status": "COMPLETED",
            },
        ]

        for request_data in requests:
            existing_request = (
                db.query(ServiceRequest)
                .filter(
                    ServiceRequest.title
                    == request_data["title"]
                )
                .filter(
                    ServiceRequest.device_id
                    == request_data["device_id"]
                )
                .first()
            )

            if existing_request:
                continue

            db.add(ServiceRequest(**request_data))

        db.commit()

    finally:
        db.close()


if __name__ == "__main__":
    create_users()
    create_devices()
    create_service_requests()