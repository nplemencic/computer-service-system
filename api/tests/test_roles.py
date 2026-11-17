from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

def test_customer_cannot_view_all_service_requests():
    """
    Customer ne smije pristupiti
    technician endpointu.
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

    response = client.get(
        "/service-requests/all",
        headers={
            "Authorization":
            f"Bearer {token}"
        },
    )

    assert response.status_code == 403

def test_technician_can_view_all_service_requests():
    """
    Technician smije pristupiti
    popisu svih servisnih zahtjeva.
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

    response = client.get(
        "/service-requests/all",
        headers={
            "Authorization":
            f"Bearer {token}"
        },
    )

    assert response.status_code == 200