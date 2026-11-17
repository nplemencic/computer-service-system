from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, ConfigDict, StringConstraints

# Duljine odgovaraju stupcima u bazi (String(100))
ShortText = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,
        min_length=1,
        max_length=100,
    ),
]


class DeviceCreate(BaseModel):
    """
    Podaci za kreiranje uređaja.
    """

    manufacturer: ShortText
    model: ShortText
    serial_number: ShortText


class DeviceResponse(BaseModel):
    """
    Podaci o uređaju koje vraća API.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int
    owner_id: int

    manufacturer: str
    model: str
    serial_number: str

    created_at: datetime
