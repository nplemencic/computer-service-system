from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    # Naziv aplikacije
    APP_NAME: str = "Computer Service System API"

    # Okolina rada (dev/prod)
    ENV: str = "dev"

    # Tajni ključ za JWT (u produkciji se mijenja)
    JWT_SECRET: str = "change-me"

    # Trajanje access tokena u minutama
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Trajanje refresh tokena u danima
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Veza prema PostgreSQL bazi
    DATABASE_URL: str


settings = Settings()
