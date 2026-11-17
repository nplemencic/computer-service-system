from sqlalchemy.orm import Session

from app.models.device import Device
from app.models.service_request import ServiceRequest


def create_service_request(
    db: Session,
    request: ServiceRequest,
) -> ServiceRequest:
    """
    Sprema novi servisni zahtjev.
    """

    db.add(request)
    db.commit()
    db.refresh(request)

    return request


def get_all_service_requests(
    db: Session,
    limit: int,
    offset: int,
) -> list[ServiceRequest]:
    """
    Dohvaća sve zahtjeve uz straničenje.
    """

    return (
        db.query(ServiceRequest)
        .order_by(ServiceRequest.id)
        .offset(offset)
        .limit(limit)
        .all()
    )


def get_service_requests_by_owner(
    db: Session,
    owner_id: int,
    limit: int,
    offset: int,
) -> list[ServiceRequest]:
    """
    Dohvaća zahtjeve za uređaje određenog vlasnika uz straničenje.
    """

    return (
        db.query(ServiceRequest)
        .join(Device, ServiceRequest.device_id == Device.id)
        .filter(Device.owner_id == owner_id)
        .order_by(ServiceRequest.id)
        .offset(offset)
        .limit(limit)
        .all()
    )


def get_service_request_by_id(
    db: Session,
    request_id: int,
) -> ServiceRequest | None:
    """
    Dohvaća servisni zahtjev po ID-u.
    """

    return db.query(ServiceRequest).filter(ServiceRequest.id == request_id).first()


def update_service_request(
    db: Session,
    request: ServiceRequest,
) -> ServiceRequest:
    """
    Sprema promjene servisnog zahtjeva.
    """

    db.commit()
    db.refresh(request)

    return request
