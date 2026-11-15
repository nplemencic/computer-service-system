from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

# Engine upravlja vezama prema bazi
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
)

# Tvornica novih sesija
SessionLocal = sessionmaker(
    bind=engine,
)
