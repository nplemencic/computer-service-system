from app.core.database import SessionLocal


def get_session():
    """
    Vraća SQLAlchemy sesiju za skripte
    koje se pokreću izvan FastAPI-ja.
    """
    return SessionLocal()