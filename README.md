# Computer Service System

Backend aplikacije za praćenje servisnih zahtjeva računalne opreme. Korisnik
(`customer`) prijavljuje svoje uređaje i otvara servisne zahtjeve za njih, a
tehničar (`technician`) vidi sve zahtjeve i vodi ih kroz statuse.

Projekt je izrađen u sklopu kolegija Programiranje za web (1. dio: backend).
Repozitorij: https://github.com/nplemencic/computer-service-system

## Tehnologije

FastAPI, Pydantic, SQLAlchemy 2, Alembic, PostgreSQL 16 (Docker), bcrypt,
python-jose (JWT), pytest, ruff.

## Struktura

```text
docker-compose.yml        baza (PostgreSQL)
api/
├── alembic/              migracije
├── app/
│   ├── core/             konfiguracija, sigurnost, ovisnosti, pogreške
│   ├── models/           SQLAlchemy modeli
│   ├── schemas/          Pydantic sheme (unos, izmjena, odgovor)
│   ├── repositories/     upiti nad bazom
│   ├── services/         poslovna pravila
│   ├── routers/          HTTP rute
│   ├── main.py           sastavljanje aplikacije
│   └── seed.py           početni podatci
├── tests/
├── requirements.txt
└── .env.example
```

Ruta prima zahtjev i vraća odgovor, poslovno pravilo stoji u servisu, a upit
nad bazom samo u repozitoriju.

## Pokretanje

Naredbe su za Windows PowerShell; na Linuxu/macOS-u aktivacija okoline je
`source .venv/bin/activate`.

```bash
# 1. repozitorij
git clone https://github.com/nplemencic/computer-service-system.git
cd computer-service-system

# 2. baza u kontejneru (iz korijena repozitorija)
docker compose up -d

# 3. virtualno okruženje i paketi
cd api
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt

# 4. konfiguracija
copy .env.example .env

# 5. migracije i početni podatci
alembic upgrade head
python -m app.seed

# 6. poslužitelj
uvicorn app.main:app --reload
```

Provjera: http://127.0.0.1:8000/health/ vraća `{"status": "ok"}`, a popis ruta
je na http://127.0.0.1:8000/docs.

Ako se pri pokretanju javi `Connection refused` na portu 5432, baza nije
pokrenuta: uključite Docker Desktop i ponovite `docker compose up -d`.

### Konfiguracija (`api/.env`)

| Varijabla | Značenje |
|---|---|
| `DATABASE_URL` | veza prema PostgreSQL-u |
| `JWT_SECRET` | tajni ključ za potpis tokena (u produkciji se mijenja) |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | vijek access tokena (zadano 30) |
| `REFRESH_TOKEN_EXPIRE_DAYS` | vijek refresh tokena (zadano 7) |
| `ENV` | `dev` ili `prod` |

Datoteka `.env` nije u repozitoriju; predložak je `api/.env.example`.

### Početni podatci

`python -m app.seed` smije se pokrenuti više puta; ne stvara ponovno ono što
već postoji. Upisuje korisnike (lozinka svih je `test123`):

| Korisničko ime | Uloga |
|---|---|
| `technician` | technician |
| `customer1` | customer (uređaji Dell i HP) |
| `customer2` | customer (uređaj Lenovo) |

## Testovi

```bash
cd api
pytest
```

Testovi rade nad zasebnom bazom `<ime baze>_test` koja se sama stvara na
istom poslužitelju (potrebna je pokrenuta baza iz koraka 2). Svaki test radi
u transakciji koja se poništava, pa razvojna baza ostaje netaknuta. Pokriveni
su prijava i obnova tokena, uloge, vlasništvo nad zapisima, poslovno pravilo,
straničenje i oblik pogrešaka.

Statička analiza: `ruff format .` i `ruff check .`

## Krajnje točke

| Metoda | Putanja | Pristup | Opis |
|---|---|---|---|
| GET | `/health/` | javno | provjera stanja |
| POST | `/auth/login` | javno | prijava, vraća access i refresh token |
| POST | `/auth/refresh` | refresh token | novi par tokena |
| GET | `/auth/me` | prijavljen | podatci o prijavljenom korisniku |
| GET | `/devices` | prijavljen | vlastiti uređaji (`limit`, `offset`) |
| GET | `/devices/{id}` | vlasnik | jedan uređaj |
| POST | `/devices` | prijavljen | novi uređaj (201) |
| POST | `/service-requests` | vlasnik uređaja | novi zahtjev za vlastiti uređaj (201) |
| GET | `/service-requests` | prijavljen | zahtjevi za vlastite uređaje (`limit`, `offset`) |
| GET | `/service-requests/all` | technician | svi zahtjevi (`limit`, `offset`) |
| GET | `/service-requests/{id}` | technician ili vlasnik uređaja | jedan zahtjev |
| PATCH | `/service-requests/{id}/status` | technician | promjena statusa |

Tokeni se šalju zaglavljem `Authorization: Bearer <access_token>`. Access token
vrijedi 30 minuta, refresh token 7 dana; refresh token ne prolazi kao access
token ni obrnuto.

Svi popisi primaju `limit` (zadano 20, najviše 100) i `offset` (zadano 0), a
poredani su po oznaci.

## Uloge i vlasništvo

- **customer** vidi i mijenja samo svoje uređaje i zahtjeve za njih.
- **technician** vidi sve zahtjeve i mijenja im status.

Vlasništvo provjerava backend. Tuđi zapis izgleda isto kao nepostojeći
(`404 not_found`), pa se ne odaje koji zapisi postoje.

## Poslovna pravila

1. **Prijelazi statusa servisnog zahtjeva.** Status se mijenja samo redom
   OPEN → IN_PROGRESS → COMPLETED. COMPLETED je završno stanje, a povratak
   unatrag i ponavljanje istog statusa nisu dopušteni
   (`400 invalid_status_transition`). Nepoznat status odbija shema (`422`).

   | iz \ u | OPEN | IN_PROGRESS | COMPLETED |
   |---|---|---|---|
   | OPEN | ne | da | ne |
   | IN_PROGRESS | ne | ne | da |
   | COMPLETED | ne | ne | ne |

2. **Vlasništvo pri otvaranju zahtjeva.** Zahtjev se može otvoriti samo za
   vlastiti uređaj.
3. **Jedinstven serijski broj uređaja.** Jedinstvenost provodi baza, a pri
   dupliciranju API vraća `409 duplicate`.

## Oblik pogrešaka

Svaki neuspjeh vraća tijelo istog oblika:

```json
{"code": "invalid_status_transition", "message": "Prijelaz iz OPEN u COMPLETED nije dopušten"}
```

`code` je stalan i namijenjen klijentskom kodu, `message` je namijenjen čovjeku
i smije se mijenjati. Odgovor `422` uz to nosi `errors` s popisom polja koja
nisu prošla provjeru:

```json
{
  "code": "validation_error",
  "message": "Neispravni podatci u zahtjevu",
  "errors": [{"field": "serial_number", "message": "Field required"}]
}
```

| code | Status | Kada |
|---|---|---|
| `validation_error` | 422 | tijelo ili parametri ne odgovaraju shemi |
| `invalid_credentials` | 401 | kriva prijava; token nedostaje, neispravan je ili je krive vrste; račun nije aktivan |
| `token_expired` | 401 | pristupni token je istekao |
| `forbidden` | 403 | uloga ne dopušta radnju |
| `not_found` | 404 | zapis ne postoji ili nije vidljiv korisniku; nepostojeća ruta |
| `method_not_allowed` | 405 | metoda nije podržana nad tom putanjom |
| `duplicate` | 409 | zapis bi prekršio jedinstvenost (serijski broj) |
| `invalid_status_transition` | 400 | prijelaz statusa nije dopušten |
| `http_error` | razno | ostale pogreške frameworka |

Kriva lozinka, nepostojeće korisničko ime i deaktiviran račun vraćaju isti
odgovor (`401 invalid_credentials`).

## Autor

Nikola Plemenčić
