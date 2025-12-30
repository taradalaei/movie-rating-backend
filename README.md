# Movie Rating System — Phase 1 (Back-End)

## Team
- Tara Dalaei
- Bita Zhian

## Tech Stack
- Python 3.12
- FastAPI
- SQLAlchemy
- Alembic
- PostgreSQL (Docker)
- Poetry

## Project Structure
- `app/` main application
- `alembic/` migrations
- `scripts/seed.sql` seed data

## Setup (Windows PowerShell)

### 1) Install dependencies
```powershell
poetry install
````

### 2) Environment variables

Create a `.env` file (do NOT commit it). You can copy from `.env.example`.

```powershell
Copy-Item .\.env.example .\.env
```

### 3) Start PostgreSQL via Docker

```powershell
docker compose up -d
```

### 4) Run migrations

```powershell
$env:PYTHONPATH = (Get-Location).Path
poetry run alembic upgrade head
```

### 5) Seed database

```powershell
Get-Content .\scripts\seed.sql | docker exec -i movie_rating_db psql -U movie_user -d movie_rating_db
```

### 6) Run server

```powershell
poetry run uvicorn app.main:app --reload
```

Open Swagger:

* [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## Implemented Endpoints

### Movies list

* `GET /api/v1/movies?page=1&page_size=10`

### Movies search & filter

* `GET /api/v1/movies/search?q=&director=&genre=&year_from=&year_to=&page=&page_size=`

### Movie detail

* `GET /api/v1/movies/{movie_id}`

### Create rating

* `POST /api/v1/movies/{movie_id}/ratings`
  Body:

```json
{ "score": 10 }
```

## Notes

* Column name `"cast"` is reserved in PostgreSQL; in SQL scripts it must be quoted as `"cast"`.
