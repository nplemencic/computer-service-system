from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.deps import get_current_user, get_db
from app.models.user import User
from app.schemas.device import DeviceCreate, DeviceResponse
from app.services.device_service import (
    create_user_device,
    get_user_device,
    get_user_devices,
)

router = APIRouter()


@router.get("", response_model=list[DeviceResponse])
def get_devices(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Popis uređaja prijavljenog korisnika uz straničenje.
    """

    return get_user_devices(db, current_user.id, limit, offset)


@router.get("/{device_id}", response_model=DeviceResponse)
def get_device(
    device_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Podaci o uređaju; dostupno samo vlasniku.
    """

    return get_user_device(db, device_id, current_user)


@router.post(
    "",
    response_model=DeviceResponse,
    status_code=201,
)
def create_device(
    data: DeviceCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
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
