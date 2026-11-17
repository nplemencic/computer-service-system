from sqlalchemy.orm import Session

from app.core.errors import AppError
from app.models.service_request import ServiceRequest
from app.models.user import User
from app.repositories.device_repository import get_device_by_id
from app.repositories.service_request_repository import (
    create_service_request,
    get_all_service_requests,
    get_service_request_by_id,
    get_service_requests_by_owner,
    update_service_request,
)

# Poslovno pravilo: dopušteni prijelazi statusa.
# COMPLETED je završno stanje, a povratak unatrag nije moguć.
#
#   iz \ u        OPEN   IN_PROGRESS   COMPLETED
#   OPEN           ne        da           ne
#   IN_PROGRESS    ne        ne           da
#   COMPLETED      ne        ne           ne
ALLOWED_TRANSITIONS: dict[str, set[str]] = {
    "OPEN": {"IN_PROGRESS"},
    "IN_PROGRESS": {"COMPLETED"},
    "COMPLETED": set(),
}


def _request_not_found() -> AppError:
    return AppError(
        "not_found",
        "Servisni zahtjev ne postoji",
        404,
    )


def create_user_service_request(
    db: Session,
    owner_id: int,
    device_id: int,
    title: str,
    description: str,
) -> ServiceRequest:
    """
    Kreira novi servisni zahtjev samo za uređaj
    koji pripada prijavljenom korisniku.
    """

    device = get_device_by_id(db, device_id)

    # Tuđi uređaj izgleda isto kao nepostojeći
    if not device or device.owner_id != owner_id:
        raise AppError(
            "not_found",
            "Uređaj ne postoji",
            404,
        )

    request = ServiceRequest(
        device_id=device_id,
        title=title,
        description=description,
        status="OPEN",
    )

    return create_service_request(db, request)


def get_user_service_requests(
    db: Session,
    owner_id: int,
    limit: int,
    offset: int,
) -> list[ServiceRequest]:
    """
    Dohvaća servisne zahtjeve za uređaje korisnika.
    """

    return get_service_requests_by_owner(
        db,
        owner_id,
        limit,
        offset,
    )


def get_all_requests(
    db: Session,
    limit: int,
    offset: int,
) -> list[ServiceRequest]:
    """
    Dohvaća sve servisne zahtjeve (tehničar).
    """

    return get_all_service_requests(db, limit, offset)


def get_service_request_for_user(
    db: Session,
    request_id: int,
    user: User,
) -> ServiceRequest:
    """
    Tehničar vidi svaki zahtjev, a korisnik samo zahtjeve za svoje
    uređaje. Tuđi zahtjev izgleda isto kao nepostojeći (404).
    """

    request = get_service_request_by_id(db, request_id)

    if not request:
        raise _request_not_found()

    if user.role != "technician" and request.device.owner_id != user.id:
        raise _request_not_found()

    return request


def change_request_status(
    db: Session,
    request_id: int,
    new_status: str,
) -> ServiceRequest:
    """
    Mijenja status zahtjeva ako je prijelaz dopušten.
    """

    request = get_service_request_by_id(db, request_id)

    if not request:
        raise _request_not_found()

    if new_status not in ALLOWED_TRANSITIONS[request.status]:
        raise AppError(
            "invalid_status_transition",
            f"Prijelaz iz {request.status} u {new_status} nije dopušten",
            400,
        )

    request.status = new_status

    return update_service_request(db, request)
