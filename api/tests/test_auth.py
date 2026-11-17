from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

def test_login_with_invalid_credentials():
    """
    Neispravno korisničko ime ili lozinka
    vraća 401.
    """

    response = client.post(
        "/auth/login",
        json={
            "username": "banana",
            "password": "banana",
        },
    )

    assert response.status_code == 401

def test_login_with_valid_credentials():
    """
    Ispravan login vraća 200.
    """

    response = client.post(
        "/auth/login",
        json={
            "username": "customer1",
            "password": "test123",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert "refresh_token" in data