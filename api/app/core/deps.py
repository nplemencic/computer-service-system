from app.core.database import AsyncSessionLocal


async def get_db():
    """
    Otvara sesiju za jedan zahtjev.
    Ako sve prođe radi commit,
    a u slučaju greške rollback.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise