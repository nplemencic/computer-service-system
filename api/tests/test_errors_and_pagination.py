import pytest


def test_unknown_route_uses_error_format(client):
    response = client.get("/nema-ove-rute")

    assert response.status_code == 404
    assert response.json()["code"] == "not_found"
    assert "message" in response.json()


def test_validation_error_lists_failed_fields(client, headers):
    response = client.post(
        "/devices",
        headers=headers("customer1"),
        json={"manufacturer": "Dell", "model": "Latitude"},
    )

    assert response.status_code == 422

    body = response.json()

    assert body["code"] == "validation_error"
    assert "message" in body
    assert [e["field"] for e in body["errors"]] == ["serial_number"]


def test_empty_and_too_long_values_are_rejected(client, headers):
    empty = client.post(
        "/devices",
        headers=headers("customer1"),
        json={"manufacturer": "  ", "model": "X", "serial_number": "Y"},
    )
    too_long = client.post(
        "/devices",
        headers=headers("customer1"),
        json={
            "manufacturer": "D" * 101,
            "model": "X",
            "serial_number": "Y",
        },
    )

    assert empty.status_code == 422
    assert too_long.status_code == 422


def test_create_device_returns_201(client, headers):
    response = client.post(
        "/devices",
        headers=headers("customer1"),
        json={
            "manufacturer": "Dell",
            "model": "Latitude",
            "serial_number": "SN-NEW",
        },
    )

    assert response.status_code == 201
    assert response.json()["serial_number"] == "SN-NEW"


def test_limit_and_offset_page_through_results(
    client,
    headers,
    make_device,
):
    ids = [make_device("customer1", f"SN-{i}").id for i in range(3)]

    first_page = client.get(
        "/devices?limit=2&offset=0",
        headers=headers("customer1"),
    )
    second_page = client.get(
        "/devices?limit=2&offset=2",
        headers=headers("customer1"),
    )

    assert [d["id"] for d in first_page.json()] == ids[:2]
    assert [d["id"] for d in second_page.json()] == ids[2:]


def test_default_limit_is_20(client, headers, make_device):
    for i in range(21):
        make_device("customer1", f"SN-{i}")

    response = client.get("/devices", headers=headers("customer1"))

    assert response.status_code == 200
    assert len(response.json()) == 20


@pytest.mark.parametrize(
    "query",
    ["limit=0", "limit=101", "limit=-1", "offset=-1"],
)
def test_invalid_pagination_is_rejected(client, headers, query):
    response = client.get(f"/devices?{query}", headers=headers("customer1"))

    assert response.status_code == 422
    assert response.json()["code"] == "validation_error"
