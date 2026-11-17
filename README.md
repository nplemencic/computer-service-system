# Computer Service System

Backend web aplikacija za upravljanje servisnim zahtjevima računalne opreme.

Projekt je razvijen u sklopu kolegija Programiranje za web.

## Korištene tehnologije

- FastAPI
- SQLAlchemy 2.0
- PostgreSQL
- Alembic
- Pydantic
- JWT Authentication
- bcrypt
- Pytest

## Funkcionalnosti

### Autentikacija

- Prijava korisnika
- JWT access token
- JWT refresh token
- Dohvat trenutno prijavljenog korisnika

### Autorizacija

- Role-based authorization
- Customer uloga
- Technician uloga

### Upravljanje uređajima

- Kreiranje uređaja
- Dohvat uređaja prijavljenog korisnika
- Pagination (limit, offset)

### Servisni zahtjevi

- Kreiranje servisnog zahtjeva
- Dohvat vlastitih servisnih zahtjeva
- Dohvat svih servisnih zahtjeva (technician)
- Promjena statusa servisnog zahtjeva
- Pagination (limit, offset)

### Poslovna pravila

- Korisnik može kreirati servisni zahtjev samo za vlastiti uređaj
- Technician može mijenjati status servisnog zahtjeva
- Dozvoljeni statusi:
  - OPEN
  - IN_PROGRESS
  - COMPLETED

### Sigurnost

- Lozinke se spremaju kao bcrypt hash
- Ownership provjera na backendu
- JWT autentikacija
- Refresh token mehanizam

## Struktura projekta

```text
api/
├── alembic/
├── app/
│   ├── core/
│   ├── models/
│   ├── repositories/
│   ├── routers/
│   ├── schemas/
│   ├── services/
│   ├── main.py
│   └── seed.py
├── tests/
├── requirements.txt
├── .env.example
└── README.md
```

## Pokretanje projekta

### 1. Kloniranje repozitorija

```bash
git clone https://github.com/nplemencic/computer-service-system.git
cd computer-service-system/api
```

### 2. Kreiranje virtualnog okruženja

```bash
python -m venv .venv
```

### 3. Aktivacija virtualnog okruženja

Windows:

```bash
.venv\Scripts\activate
```

Linux / macOS:

```bash
source .venv/bin/activate
```

### 4. Instalacija paketa

```bash
pip install -r requirements.txt
```

### 5. Konfiguracija okruženja

Kopirati:

```bash
.env.example
```

u:

```bash
.env
```

i po potrebi prilagoditi vrijednosti.

Primjer:

```env
APP_NAME=Computer Service System API
ENV=dev

JWT_SECRET=change-me

DATABASE_URL=postgresql+psycopg2://service_user:service_pass@localhost:5432/computer_service

ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
```

## Baza podataka

### Primjena migracija

```bash
alembic upgrade head
```

### Učitavanje početnih podataka

```bash
python -m app.seed
```

## Pokretanje aplikacije

```bash
uvicorn app.main:app --reload
```

Swagger dokumentacija:

```text
http://127.0.0.1:8000/docs
```

## Testiranje

Pokretanje svih testova:

```bash
pytest
```

## API Endpointi

### Auth

| Metoda | Endpoint | Opis |
|---------|----------|------|
| POST | /auth/login | Prijava |
| POST | /auth/refresh | Obnavljanje access tokena |
| GET | /auth/me | Trenutni korisnik |

### Devices

| Metoda | Endpoint |
|---------|----------|
| POST | /devices |
| GET | /devices |

### Service Requests

| Metoda | Endpoint |
|---------|----------|
| POST | /service-requests |
| GET | /service-requests |
| GET | /service-requests/all |
| PATCH | /service-requests/{request_id}/status |

### Health

| Metoda | Endpoint |
|---------|----------|
| GET | /health |

## Korisničke uloge

### Customer

- kreiranje uređaja
- pregled vlastitih uređaja
- kreiranje servisnih zahtjeva
- pregled vlastitih servisnih zahtjeva

### Technician

- pregled svih servisnih zahtjeva
- promjena statusa servisnih zahtjeva

## Autor

Nikola Plemenčić