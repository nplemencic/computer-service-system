from datetime import datetime
from app.models.service_request import (
    ServiceRequest,
)

from app.repositories.service_request_repository import (
    create_service_request,
    get_service_requests_by_device_ids,
    get_service_request_by_id,
    update_service_request,
)

from app.repositories.device_repository import (
    get_devices_by_owner,
)

def create_user_service_request(
    db,
    device_id: int,
    title: str,
    description: str,
) -> ServiceRequest:
    """
    Kreira novi servisni zahtjev.
    """

    request = ServiceRequest(
        device_id=device_id,
        title=title,
        description=description,
        status="OPEN",
    )

    return create_service_request(
        db,
        request,
    )

def get_user_service_requests(
    db,
    owner_id: int,
):
    """
    Dohvaća sve servisne zahtjeve korisnika.
    """

    devices = get_devices_by_owner(
        db,
        owner_id,
    )

    device_ids = [
        device.id
        for device in devices
    ]

    return get_service_requests_by_device_ids(
        db,
        device_ids,
    )

def change_request_status(
    db,
    request_id: int,
    status: str,
):
    """
    Mijenja status servisnog zahtjeva.
    """

    request = get_service_request_by_id(
        db,
        request_id,
    )

    if not request:
        return None

    request.status = status

    # Ažuriramo vrijeme zadnje promjene
    request.updated_at = datetime.utcnow()

    return update_service_request(
        db,
        request,
    )
