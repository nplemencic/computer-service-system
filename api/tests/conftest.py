"""
Zajednički fixtureovi.

Testovi rade nad zasebnom bazom (<ime baze>_test) koja se sama stvara.
Svaki test radi unutar transakcije koja se na kraju poništi, pa se razvojna
baza ne dira i testovi ne ovise jedni o drugima ni o seed skripti.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.engine import make_url
from sqlalchemy.orm import Session

import app.models  # noqa: F401
from app.core.config import settings
from app.core.deps import get_db
from app.core.security import create_access_token, hash_password
from app.main import create_app
from app.models.base import Base
from app.models.device import Device
from app.models.service_request import ServiceRequest
from app.models.user import User

PASSWORD = "test123"

USERS = [
    ("technician", "technician"),
    ("customer1", "customer"),
    ("customer2", "customer"),
]


@pytest.fixture(scope="session")
def engine():
    dev_url = make_url(settings.DATABASE_URL)
    test_url = dev_url.set(database=f"{dev_url.database}_test")

    # Sigurnosna provjera: nikad ne brišemo razvojnu bazu
    assert test_url.database.endswith("_test")

    # Zasebna baza stvara se ako ne postoji
    admin = create_engine(
        dev_url.set(database="postgres"),
        isolation_level="AUTOCOMMIT",
    )
    with admin.connect() as connection:
        exists = connection.execute(
            text("SELECT 1 FROM pg_database WHERE datname = :name"),
            {"name": test_url.database},
        ).scalar()

        if not exists:
            connection.execute(text(f'CREATE DATABASE "{test_url.database}"'))
    admin.dispose()

    test_engine = create_engine(test_url)

    # Svaki pokretanje testova kreće s praznom shemom
    Base.metadata.drop_all(test_engine)
    Base.metadata.create_all(test_engine)

    yield test_engine

    test_engine.dispose()


@pytest.fixture(scope="session")
def seed_users(engine):
    """
    Tri korisnika upisuju se jednom po pokretanju (bcrypt je spor).
    """

    with Session(engine) as session:
        for username, role in USERS:
            session.add(
                User(
                    username=username,
                    password_hash=hash_password(PASSWORD),
                    role=role,
                )
            )
        session.commit()


@pytest.fixture
def db(engine, seed_users):
    """
    Sesija unutar vanjske transakcije koja se poništava nakon testa.
    commit() unutar aplikacije oslobađa samo savepoint.
    """

    connection = engine.connect()
    outer_transaction = connection.begin()
    session = Session(
        bind=connection,
        join_transaction_mode="create_savepoint",
    )

    yield session

    session.close()
    outer_transaction.rollback()
    connection.close()


@pytest.fixture
def client(db):
    app = create_app()

    def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def users(db):
    return {user.username: user for user in db.query(User).all()}


@pytest.fixture
def headers():
    """
    Vraća funkciju koja za korisničko ime daje Authorization zaglavlje.
    Token se izdaje izravno, bez prijave (i bez bcrypta).
    """

    def _headers(username: str) -> dict:
        token = create_access_token(username)
        return {"Authorization": f"Bearer {token}"}

    return _headers


@pytest.fixture
def make_device(db, users):
    def _make(owner: str = "customer1", serial: str = "SN-1") -> Device:
        device = Device(
            owner_id=users[owner].id,
            manufacturer="Dell",
            model="Latitude",
            serial_number=serial,
        )
        db.add(device)
        db.flush()
        return device

    return _make


@pytest.fixture
def make_request(db):
    def _make(device: Device, status: str = "OPEN") -> ServiceRequest:
        request = ServiceRequest(
            device_id=device.id,
            title="Test zahtjev",
            description="Opis kvara",
            status=status,
        )
        db.add(request)
        db.flush()
        return request

    return _make
