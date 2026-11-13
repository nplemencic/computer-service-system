from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def health():
    """
    Provjera radi li aplikacija.
    """
    return {"status": "ok"}