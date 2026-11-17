from datetime import datetime
from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, StringConstraints

RequestStatus = Literal["OPEN", "IN_PROGRESS", "COMPLETED"]

Title = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,
        min_length=1,
        max_length=100,
    ),
]

Description = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,
        min_length=1,
        max_length=2000,
    ),
]


class ServiceRequestCreate(BaseModel):
    """
    Podaci za kreiranje servisnog zahtjeva.
    """

    device_id: int
    title: Title
    description: Description


class ServiceRequestStatusUpdate(BaseModel):
    """
    Promjena statusa servisnog zahtjeva.
    Nepoznat status odbija shema (422); dopušten prijelaz provjerava servis.
    """

    status: RequestStatus


class ServiceRequestResponse(BaseModel):
    """
    Podaci koje API vraća o zahtjevu.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int
    device_id: int

    title: str
    description: str

    status: str

    created_at: datetime
    updated_at: datetime
