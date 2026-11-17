def test_customer_cannot_list_all_requests(client, headers):
    response = client.get(
        "/service-requests/all",
        headers=headers("customer1"),
    )

    assert response.status_code == 403
    assert response.json()["code"] == "forbidden"


def test_technician_can_list_all_requests(
    client,
    headers,
    make_device,
    make_request,
):
    make_request(make_device("customer1", "SN-A"))
    make_request(make_device("customer2", "SN-B"))

    response = client.get(
        "/service-requests/all",
        headers=headers("technician"),
    )

    assert response.status_code == 200
    assert len(response.json()) == 2


def test_customer_cannot_change_status(
    client,
    headers,
    make_device,
    make_request,
):
    request = make_request(make_device("customer1"))

    response = client.patch(
        f"/service-requests/{request.id}/status",
        headers=headers("customer1"),
        json={"status": "IN_PROGRESS"},
    )

    assert response.status_code == 403
    assert response.json()["code"] == "forbidden"


def test_technician_can_change_status(
    client,
    headers,
    make_device,
    make_request,
):
    request = make_request(make_device("customer1"))

    response = client.patch(
        f"/service-requests/{request.id}/status",
        headers=headers("technician"),
        json={"status": "IN_PROGRESS"},
    )

    assert response.status_code == 200
    assert response.json()["status"] == "IN_PROGRESS"


def test_requests_without_token_are_rejected(client):
    for method, url in [
        ("get", "/devices"),
        ("post", "/devices"),
        ("get", "/service-requests"),
        ("get", "/service-requests/all"),
        ("patch", "/service-requests/1/status"),
    ]:
        response = getattr(client, method)(url)

        assert response.status_code == 401, f"{method} {url}"
        assert response.json()["code"] == "invalid_credentials"
