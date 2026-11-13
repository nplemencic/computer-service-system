from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.core.config import settings

# Engine upravlja vezama prema bazi
engine = create_async_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
)

# Tvornica novih sesija
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
)