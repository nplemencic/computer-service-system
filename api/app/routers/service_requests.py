from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.deps import (
    get_current_user,
    get_db,
    require_technician,
)
from app.models.user import User
from app.schemas.service_request import (
    ServiceRequestCreate,
    ServiceRequestResponse,
    ServiceRequestStatusUpdate,
)
from app.services.service_request_service import (
    change_request_status,
    create_user_service_request,
    get_all_requests,
    get_service_request_for_user,
    get_user_service_requests,
)

router = APIRouter()


@router.post(
    "",
    response_model=ServiceRequestResponse,
    status_code=201,
)
def create_service_request(
    data: ServiceRequestCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Kreira novi servisni zahtjev za vlastiti uređaj.
    """

    return create_user_service_request(
        db=db,
        owner_id=current_user.id,
        device_id=data.device_id,
        title=data.title,
        description=data.description,
    )


@router.get("", response_model=list[ServiceRequestResponse])
def get_service_requests(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Servisni zahtjevi za uređaje prijavljenog korisnika.
    """

    return get_user_service_requests(
        db,
        current_user.id,
        limit,
        offset,
    )


# Mora stajati prije /{request_id}, inače bi "all" bio shvaćen kao oznaka
@router.get("/all", response_model=list[ServiceRequestResponse])
def get_all_service_requests(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    current_user: User = Depends(require_technician),
    db: Session = Depends(get_db),
):
    """
    Prikaz svih servisnih zahtjeva. Dostupno samo tehničaru.
    """

    return get_all_requests(db, limit, offset)


@router.get("/{request_id}", response_model=ServiceRequestResponse)
def get_service_request(
    request_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Jedan servisni zahtjev: tehničar bilo koji, korisnik samo svoj.
    """

    return get_service_request_for_user(db, request_id, current_user)


@router.patch(
    "/{request_id}/status",
    response_model=ServiceRequestResponse,
)
def update_status(
    request_id: int,
    data: ServiceRequestStatusUpdate,
    current_user: User = Depends(require_technician),
    db: Session = Depends(get_db),
):
    """
    Promjena statusa servisnog zahtjeva (OPEN -> IN_PROGRESS -> COMPLETED).
    Dostupno samo tehničaru.
    """

    return change_request_status(db, request_id, data.status)
