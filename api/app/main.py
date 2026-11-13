from fastapi import FastAPI

# Kreiranje FastAPI aplikacije
app = FastAPI(
    title="Computer Service System API",
)


@app.get("/health")
def health():
    """
    Jednostavna provjera radi li aplikacija.
    """
    return {"status": "ok"}