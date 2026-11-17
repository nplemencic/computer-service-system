from fastapi import APIRouter, Depends

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
    create_user_service_request,
    get_user_service_requests,
    change_request_status,
    get_all_requests,
)

router = APIRouter()

@router.post(
    "",
    response_model=ServiceRequestResponse,
)
def create_service_request(
    data: ServiceRequestCreate,
    current_user: User = Depends(
        get_current_user
    ),
    db: Session = Depends(
        get_db
    ),
):
    """
    Kreira novi servisni zahtjev.
    """

    return create_user_service_request(
        db=db,
        owner_id=current_user.id,
        device_id=data.device_id,
        title=data.title,
        description=data.description,
    )

@router.get(
    "",
    response_model=list[ServiceRequestResponse],
)
def get_service_requests(
    current_user: User = Depends(
        get_current_user
    ),
    db: Session = Depends(
        get_db
    ),
):
    """
    Vraća servisne zahtjeve prijavljenog korisnika.
    """

    return get_user_service_requests(
        db,
        current_user.id,
    )

@router.patch(
    "/{request_id}/status",
    response_model=ServiceRequestResponse,
)
def update_status(
    request_id: int,
    data: ServiceRequestStatusUpdate,

    current_user: User = Depends(
        require_technician
    ),

    db: Session = Depends(
        get_db
    ),
):
    """
    Promjena statusa servisnog zahtjeva.
    Dostupno samo tehničaru.
    """

    request = change_request_status(
        db,
        request_id,
        data.status,
    )

    return request

@router.get(
    "/all",
    response_model=list[ServiceRequestResponse],
)
def get_all_service_requests(
    current_user: User = Depends(
        require_technician
    ),
    db: Session = Depends(
        get_db
    ),
):
    """
    Prikaz svih servisnih zahtjeva.
    Dostupno samo tehničaru.
    """

    return get_all_requests(
        db,
    )