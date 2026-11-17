from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

def test_user_cannot_create_request_for_foreign_device():
    """
    Korisnik ne smije otvoriti
    servisni zahtjev za tuđi uređaj.
    """

    login_response = client.post(
        "/auth/login",
        json={
            "username": "customer1",
            "password": "test123",
        },
    )

    token = login_response.json()[
        "access_token"
    ]

    response = client.post(
        "/service-requests",
        headers={
            "Authorization":
            f"Bearer {token}"
        },
        json={
            "device_id": 999999,
            "title": "Test",
            "description": "Test",
        },
    )

    assert response.status_code in [403, 404]