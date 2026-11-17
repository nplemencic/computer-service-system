"""
Domenske pogreške i njihovo prevođenje u odgovor jedinstvenog oblika.

Svaki neuspjeh prema klijentu ima tijelo s poljima `code` i `message`;
odgovor 422 uz to nosi i popis polja koja nisu prošla provjeru (`errors`).
"""

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException


class AppError(Exception):
    """
    Pogreška koju podiže aplikacija (pravilo, prava, nepostojeći zapis).

    `code` je stalan i namijenjen klijentskom kodu, `message` je namijenjen
    čovjeku i smije se mijenjati.
    """

    def __init__(
        self,
        code: str,
        message: str,
        status_code: int = 400,
    ):
        super().__init__(message)
        self.code = code
        self.message = message
        self.status_code = status_code


# Kodovi za pogreške koje podiže sam framework (npr. nepostojeća ruta)
_HTTP_STATUS_CODES = {
    401: "invalid_credentials",
    403: "forbidden",
    404: "not_found",
    405: "method_not_allowed",
}


def _error_body(code: str, message: str) -> dict:
    return {"code": code, "message": message}


async def app_error_handler(
    _request: Request,
    exc: AppError,
) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content=_error_body(exc.code, exc.message),
    )


async def http_error_handler(
    _request: Request,
    exc: StarletteHTTPException,
) -> JSONResponse:
    code = _HTTP_STATUS_CODES.get(exc.status_code, "http_error")

    return JSONResponse(
        status_code=exc.status_code,
        content=_error_body(code, str(exc.detail)),
        headers=exc.headers,
    )


async def validation_error_handler(
    _request: Request,
    exc: RequestValidationError,
) -> JSONResponse:
    errors = [
        {
            # loc[0] je "body", "query" ili "path"; zanima nas ostatak
            "field": ".".join(str(part) for part in err["loc"][1:]),
            "message": err["msg"],
        }
        for err in exc.errors()
    ]

    body = _error_body(
        "validation_error",
        "Neispravni podatci u zahtjevu",
    )
    body["errors"] = errors

    return JSONResponse(status_code=422, content=body)


def register_error_handlers(app: FastAPI) -> None:
    """
    Prijavljuje sva tri rukovatelja na jednom mjestu.
    """
    app.add_exception_handler(AppError, app_error_handler)
    app.add_exception_handler(
        StarletteHTTPException,
        http_error_handler,
    )
    app.add_exception_handler(
        RequestValidationError,
        validation_error_handler,
    )
