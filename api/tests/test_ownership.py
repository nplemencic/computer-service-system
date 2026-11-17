"""
Vlasništvo nad zapisom provjerava backend: korisnik ne vidi i ne
koristi tuđe zapise, a tuđi zapis izgleda isto kao nepostojeći (404).
"""


def test_user_cannot_create_request_for_foreign_device(
    client,
    headers,
    make_device,
):
    foreign_device = make_device("customer2", "SN-FOREIGN")

    response = client.post(
        "/service-requests",
        headers=headers("customer1"),
        json={
            "device_id": foreign_device.id,
            "title": "Tuđi uređaj",
            "description": "Pokušaj otvaranja zahtjeva",
        },
    )

    assert response.status_code == 404
    assert response.json()["code"] == "not_found"


def test_user_can_create_request_for_own_device(
    client,
    headers,
    make_device,
):
    own_device = make_device("customer1", "SN-OWN")

    response = client.post(
        "/service-requests",
        headers=headers("customer1"),
        json={
            "device_id": own_device.id,
            "title": "Ne radi ekran",
            "description": "Ekran treperi",
        },
    )

    assert response.status_code == 201
    assert response.json()["status"] == "OPEN"
    assert response.json()["device_id"] == own_device.id


def test_foreign_device_looks_the_same_as_missing_device(
    client,
    headers,
    make_device,
):
    foreign_device = make_device("customer2", "SN-FOREIGN")

    foreign = client.get(
        f"/devices/{foreign_device.id}",
        headers=headers("customer1"),
    )
    missing = client.get("/devices/999999", headers=headers("customer1"))

    assert foreign.status_code == missing.status_code == 404
    assert foreign.json() == missing.json()


def test_user_can_read_own_device(client, headers, make_device):
    own_device = make_device("customer1", "SN-OWN")

    response = client.get(
        f"/devices/{own_device.id}",
        headers=headers("customer1"),
    )

    assert response.status_code == 200
    assert response.json()["serial_number"] == "SN-OWN"


def test_device_list_contains_only_own_devices(
    client,
    headers,
    make_device,
):
    own_device = make_device("customer1", "SN-OWN")
    make_device("customer2", "SN-FOREIGN")

    response = client.get("/devices", headers=headers("customer1"))

    assert response.status_code == 200
    assert [d["id"] for d in response.json()] == [own_device.id]


def test_request_list_contains_only_own_requests(
    client,
    headers,
    make_device,
    make_request,
):
    own_request = make_request(make_device("customer1", "SN-OWN"))
    make_request(make_device("customer2", "SN-FOREIGN"))

    response = client.get(
        "/service-requests",
        headers=headers("customer1"),
    )

    assert response.status_code == 200
    assert [r["id"] for r in response.json()] == [own_request.id]


def test_user_cannot_read_foreign_request(
    client,
    headers,
    make_device,
    make_request,
):
    foreign_request = make_request(make_device("customer2", "SN-FOREIGN"))

    response = client.get(
        f"/service-requests/{foreign_request.id}",
        headers=headers("customer1"),
    )

    assert response.status_code == 404
    assert response.json()["code"] == "not_found"


def test_user_can_read_own_request(
    client,
    headers,
    make_device,
    make_request,
):
    own_request = make_request(make_device("customer1", "SN-OWN"))

    response = client.get(
        f"/service-requests/{own_request.id}",
        headers=headers("customer1"),
    )

    assert response.status_code == 200
    assert response.json()["id"] == own_request.id


def test_technician_can_read_any_request(
    client,
    headers,
    make_device,
    make_request,
):
    request = make_request(make_device("customer2", "SN-FOREIGN"))

    response = client.get(
        f"/service-requests/{request.id}",
        headers=headers("technician"),
    )

    assert response.status_code == 200
