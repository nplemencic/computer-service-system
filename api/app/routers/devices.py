from fastapi import APIRouter, Depends

from app.core.deps import require_device_owner

router = APIRouter()


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