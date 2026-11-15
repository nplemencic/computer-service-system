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


if __name__ == "__main__":
    create_users()