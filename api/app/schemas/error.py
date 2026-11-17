from pydantic import BaseModel


class ErrorResponse(BaseModel):
    """
    Standardni format greške.
    """

    code: str
    message: str