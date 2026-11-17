from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Naziv aplikacije
    APP_NAME: str = "Computer Service System API"

    # Okolina rada (dev/prod)
    ENV: str = "dev"

    # Tajni ključ za JWT
    JWT_SECRET: str = "change-me"

    # Trajanje access tokena u minutama
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Trajanje refresh tokena
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Veza prema PostgreSQL bazi
    DATABASE_URL: str

    class Config:
        env_file = ".env"


settings = Settings()