from datetime import datetime

from pydantic import BaseModel


class ServiceRequestCreate(BaseModel):
    """
    Podaci za kreiranje servisnog zahtjeva.
    """

    device_id: int
    title: str
    description: str


class ServiceRequestResponse(BaseModel):
    """
    Podaci koje API vraća o zahtjevu.
    """

    id: int

    device_id: int

    title: str
    description: str

    status: str

    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ServiceRequestStatusUpdate(
    BaseModel
):
    """
    Promjena statusa servisnog zahtjeva.
    """

    status: str