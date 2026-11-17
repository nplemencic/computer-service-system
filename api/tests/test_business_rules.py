"""
Poslovno pravilo: status zahtjeva mijenja se samo redom
OPEN -> IN_PROGRESS -> COMPLETED. COMPLETED je završno stanje.
"""

import pytest


def change_status(client, headers, request_id, status):
    return client.patch(
        f"/service-requests/{request_id}/status",
        headers=headers("technician"),
        json={"status": status},
    )


@pytest.mark.parametrize(
    "start,target",
    [
        ("OPEN", "IN_PROGRESS"),
        ("IN_PROGRESS", "COMPLETED"),
    ],
)
def test_allowed_transitions_pass(
    client,
    headers,
    make_device,
    make_request,
    start,
    target,
):
    request = make_request(make_device(), start)

    response = change_status(client, headers, request.id, target)

    assert response.status_code == 200
    assert response.json()["status"] == target


@pytest.mark.parametrize(
    "start,target",
    [
        ("OPEN", "COMPLETED"),
        ("OPEN", "OPEN"),
        ("IN_PROGRESS", "OPEN"),
        ("IN_PROGRESS", "IN_PROGRESS"),
        ("COMPLETED", "OPEN"),
        ("COMPLETED", "IN_PROGRESS"),
        ("COMPLETED", "COMPLETED"),
    ],
)
def test_forbidden_transitions_are_rejected(
    client,
    headers,
    make_device,
    make_request,
    start,
    target,
):
    request = make_request(make_device(), start)

    response = change_status(client, headers, request.id, target)

    assert response.status_code == 400
    assert response.json()["code"] == "invalid_status_transition"


def test_rejected_transition_leaves_status_unchanged(
    client,
    headers,
    make_device,
    make_request,
):
    request = make_request(make_device(), "OPEN")

    change_status(client, headers, request.id, "COMPLETED")

    response = client.get(
        f"/service-requests/{request.id}",
        headers=headers("technician"),
    )

    assert response.json()["status"] == "OPEN"


def test_full_lifecycle_in_order(
    client,
    headers,
    make_device,
    make_request,
):
    request = make_request(make_device())

    first = change_status(client, headers, request.id, "IN_PROGRESS")
    second = change_status(client, headers, request.id, "COMPLETED")
    third = change_status(client, headers, request.id, "IN_PROGRESS")

    assert first.status_code == 200
    assert second.status_code == 200
    assert third.status_code == 400
    assert third.json()["code"] == "invalid_status_transition"


def test_unknown_status_is_rejected_by_schema(
    client,
    headers,
    make_device,
    make_request,
):
    request = make_request(make_device())

    response = change_status(client, headers, request.id, "BANANA")

    assert response.status_code == 422
    assert response.json()["code"] == "validation_error"


def test_status_change_of_missing_request_returns_404(client, headers):
    response = change_status(client, headers, 999999, "IN_PROGRESS")

    assert response.status_code == 404
    assert response.json()["code"] == "not_found"


def test_duplicate_serial_number_returns_409(client, headers):
    body = {
        "manufacturer": "HP",
        "model": "ProBook",
        "serial_number": "SN-DUP",
    }

    first = client.post("/devices", headers=headers("customer1"), json=body)
    second = client.post("/devices", headers=headers("customer2"), json=body)

    assert first.status_code == 201
    assert second.status_code == 409
    assert second.json()["code"] == "duplicate"
