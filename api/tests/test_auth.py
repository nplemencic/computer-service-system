from datetime import UTC, datetime, timedelta

from jose import jwt

from app.core.config import settings
from app.core.security import (
    create_access_token,
    create_refresh_token,
)

PASSWORD = "test123"


def login(client, username, password):
    return client.post(
        "/auth/login",
        json={"username": username, "password": password},
    )


def bearer(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}


def test_login_returns_token_pair(client):
    response = login(client, "customer1", PASSWORD)

    assert response.status_code == 200

    data = response.json()

    assert data["access_token"]
    assert data["refresh_token"]
    assert data["token_type"] == "bearer"


def test_wrong_password_and_unknown_user_get_same_response(client):
    wrong_password = login(client, "customer1", "kriva-lozinka")
    unknown_user = login(client, "nepostojeci", "kriva-lozinka")

    assert wrong_password.status_code == 401
    assert unknown_user.status_code == 401
    assert wrong_password.json() == unknown_user.json()
    assert wrong_password.json()["code"] == "invalid_credentials"


def test_inactive_user_cannot_login(client, db, users):
    users["customer2"].is_active = False
    db.flush()

    response = login(client, "customer2", PASSWORD)

    assert response.status_code == 401
    assert response.json()["code"] == "invalid_credentials"


def test_me_returns_current_user_without_password_hash(client, headers):
    response = client.get("/auth/me", headers=headers("customer1"))

    assert response.status_code == 200

    body = response.json()

    assert body["username"] == "customer1"
    assert body["role"] == "customer"
    assert "password_hash" not in body


def test_me_without_token_is_rejected(client):
    response = client.get("/auth/me")

    assert response.status_code == 401
    assert response.json()["code"] == "invalid_credentials"


def test_me_with_garbage_token_is_rejected(client):
    response = client.get("/auth/me", headers=bearer("nije-token"))

    assert response.status_code == 401
    assert response.json()["code"] == "invalid_credentials"


def test_me_with_expired_token_returns_token_expired(client):
    expired = jwt.encode(
        {
            "sub": "customer1",
            "type": "access",
            "exp": datetime.now(UTC) - timedelta(minutes=1),
        },
        settings.JWT_SECRET,
        algorithm="HS256",
    )

    response = client.get("/auth/me", headers=bearer(expired))

    assert response.status_code == 401
    assert response.json()["code"] == "token_expired"


def test_token_signed_with_other_key_is_rejected(client):
    forged = jwt.encode(
        {
            "sub": "technician",
            "type": "access",
            "exp": datetime.now(UTC) + timedelta(minutes=5),
        },
        "tudji-kljuc",
        algorithm="HS256",
    )

    response = client.get("/auth/me", headers=bearer(forged))

    assert response.status_code == 401
    assert response.json()["code"] == "invalid_credentials"


def test_refresh_token_cannot_be_used_as_access_token(client):
    refresh_token = create_refresh_token("customer1")

    response = client.get("/auth/me", headers=bearer(refresh_token))

    assert response.status_code == 401
    assert response.json()["code"] == "invalid_credentials"


def test_refresh_returns_new_working_token_pair(client):
    tokens = login(client, "customer1", PASSWORD).json()

    response = client.post(
        "/auth/refresh",
        json={"refresh_token": tokens["refresh_token"]},
    )

    assert response.status_code == 200

    new_tokens = response.json()
    me = client.get(
        "/auth/me",
        headers=bearer(new_tokens["access_token"]),
    )

    assert me.status_code == 200
    assert me.json()["username"] == "customer1"


def test_refresh_rejects_access_token(client):
    access_token = create_access_token("customer1")

    response = client.post(
        "/auth/refresh",
        json={"refresh_token": access_token},
    )

    assert response.status_code == 401
    assert response.json()["code"] == "invalid_credentials"


def test_refresh_is_rejected_for_inactive_user(client, db, users):
    refresh_token = create_refresh_token("customer1")
    users["customer1"].is_active = False
    db.flush()

    response = client.post(
        "/auth/refresh",
        json={"refresh_token": refresh_token},
    )

    assert response.status_code == 401
    assert response.json()["code"] == "invalid_credentials"


def test_valid_token_of_deactivated_user_loses_access(
    client,
    db,
    users,
    headers,
):
    users["customer1"].is_active = False
    db.flush()

    response = client.get("/auth/me", headers=headers("customer1"))

    assert response.status_code == 401
