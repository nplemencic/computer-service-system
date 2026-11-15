from app.core.database import SessionLocal


def get_db():
    """
    Otvara sesiju baze za jedan HTTP zahtjev.
    """
    db = SessionLocal()

    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()