from datetime import datetime
from app.core.exceptions import ApiException
from fastapi import HTTPException
from app.models.service_request import (
    ServiceRequest,
)

from app.repositories.service_request_repository import (
    create_service_request,
    get_service_requests_by_device_ids,
    get_service_request_by_id,
    update_service_request,
    get_all_service_requests,
)

from app.repositories.device_repository import (
    get_devices_by_owner,
    get_device_by_id,
)

def create_user_service_request(
    db,
    owner_id: int,
    device_id: int,
    title: str,
    description: str,
) -> ServiceRequest:
    """
    Kreira novi servisni zahtjev samo za uređaj
    koji pripada prijavljenom korisniku.
    """

    # Provjeri postoji li uređaj
    device = get_device_by_id(
        db,
        device_id,
    )

    if not device:
        raise ApiException(
            status_code=404,
            code="DEVICE_NOT_FOUND",
            message="Device not found",
        )

    # Ownership provjera
    if device.owner_id != owner_id:
        raise ApiException(
            status_code=403,
            code="ACCESS_DENIED",
            message="Access denied",
        )

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
    owner_id,
    limit,
    offset,
):
    """
    Dohvaća sve servisne zahtjeve korisnika.
    """

    devices = get_devices_by_owner(
        db,
        owner_id,
        1000,
        0,
    )

    device_ids = [
        device.id
        for device in devices
    ]

    return get_service_requests_by_device_ids(
        db,
        device_ids,
        limit,
        offset,
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

    # Dozvoljeni statusi
    allowed_statuses = [
        "OPEN",
        "IN_PROGRESS",
        "COMPLETED",
    ]

    # Validacija poslovnog pravila
    if status not in allowed_statuses:
        raise HTTPException(
            status_code=400,
            detail="Invalid status",
        )

    request.status = status

    # Ažuriramo vrijeme zadnje promjene
    request.updated_at = datetime.utcnow()

    return update_service_request(
        db,
        request,
    )

def get_all_requests(
    db,
    limit: int,
    offset: int,
):
    """
    Dohvaća sve servisne zahtjeve.
    """

    return get_all_service_requests(
        db,
        limit,
        offset,
    )

    

