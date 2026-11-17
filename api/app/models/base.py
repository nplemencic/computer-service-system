from datetime import UTC, datetime

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """
    Bazna klasa svih SQLAlchemy modela.
    """

    pass


def utc_now() -> datetime:
    """
    Trenutno UTC vrijeme bez oznake zone
    (stupci su DateTime bez vremenske zone).
    """

    return datetime.now(UTC).replace(tzinfo=None)
