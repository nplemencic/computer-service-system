from sqlalchemy.orm import Session

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
):
    """
    Dohvaća sve servisne zahtjeve.
    """

    return (
        db.query(ServiceRequest)
        .all()
    )

def get_service_requests_by_device_ids(
    db: Session,
    device_ids: list[int],
):
    """
    Dohvaća servisne zahtjeve za zadane uređaje.
    """

    return (
        db.query(ServiceRequest)
        .filter(
            ServiceRequest.device_id.in_(
                device_ids
            )
        )
        .all()
    )

def get_service_request_by_id(
    db: Session,
    request_id: int,
) -> ServiceRequest | None:
    """
    Dohvaća servisni zahtjev po ID-u.
    """

    return (
        db.query(ServiceRequest)
        .filter(
            ServiceRequest.id == request_id
        )
        .first()
    )

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