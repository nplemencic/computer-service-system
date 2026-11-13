from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Naziv aplikacije
    APP_NAME: str = "Computer Service System API"

    # Okolina rada (dev/prod)
    ENV: str = "dev"

    # Tajni ključ za JWT
    JWT_SECRET: str = "change-me"


settings = Settings()