from datetime import datetime

from pydantic import BaseModel


class DeviceCreate(BaseModel):
    """
    Podaci za kreiranje uređaja.
    """

    manufacturer: str
    model: str
    serial_number: str


class DeviceResponse(BaseModel):
    """
    Podaci o uređaju koje vraća API.
    """

    id: int
    owner_id: int

    manufacturer: str
    model: str
    serial_number: str

    created_at: datetime

    class Config:
        from_attributes = True