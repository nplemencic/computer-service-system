from fastapi import FastAPI

from app.core.config import settings

# Kreiranje FastAPI aplikacije
app = FastAPI(
    title=settings.APP_NAME,
)


@app.get("/health")
def health():
    """
    Jednostavna provjera radi li aplikacija.
    """
    return {"status": "ok"}