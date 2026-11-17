from fastapi import APIRouter, Depends

from app.core.deps import require_device_owner

from sqlalchemy.orm import Session

from app.core.deps import (
    get_current_user,
    get_db,
)

from app.models.user import User

from app.schemas.device import (
    DeviceCreate,
    DeviceResponse,
)

from app.services.device_service import (
    create_user_device,
    get_user_devices,
)

router = APIRouter()

@router.get(
    "",
    response_model=list[DeviceResponse],
)
def get_devices(
    limit: int = 10,
    offset: int = 0,

    current_user: User = Depends(
        get_current_user
    ),

    db: Session = Depends(
        get_db
    ),
):
    """
    Popis uređaja korisnika uz straničenje.
    """

    return get_user_devices(
        db,
        current_user.id,
        limit,
        offset,
    )


@router.get("/{device_id}")
def get_device(
    device=Depends(
        require_device_owner
    ),
):
    """
    Test ownership provjere.
    """

    return {
        "device_id": device.id,
        "manufacturer": device.manufacturer,
        "model": device.model,
    }

@router.post(
    "",
    response_model=DeviceResponse,
)
def create_device(
    data: DeviceCreate,
    current_user: User = Depends(
        get_current_user
    ),
    db: Session = Depends(
        get_db
    ),
):
    """
    Kreira novi uređaj prijavljenog korisnika.
    """

    return create_user_device(
        db=db,
        owner_id=current_user.id,
        manufacturer=data.manufacturer,
        model=data.model,
        serial_number=data.serial_number,
    )