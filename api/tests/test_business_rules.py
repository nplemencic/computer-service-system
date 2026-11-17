from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

def test_invalid_status_is_rejected():
    """
    Nedozvoljeni status mora biti odbijen.
    """

    login_response = client.post(
        "/auth/login",
        json={
            "username": "technician",
            "password": "test123",
        },
    )

    token = login_response.json()[
        "access_token"
    ]

    response = client.patch(
        "/service-requests/1/status",
        headers={
            "Authorization":
            f"Bearer {token}"
        },
        json={
            "status": "BANANA"
        },
    )

    assert response.status_code == 400
