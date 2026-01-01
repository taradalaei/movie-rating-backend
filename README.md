# 🎬 Movie Rating System

A RESTful backend service for managing movies and ratings, implemented in **three phases**:

1. Back-End API & Database
2. Logging & Observability
3. Docker & Containerization

---

## 👥 Team

* **Tara Dalaei**
* **Bita Zhian**

---

## 🛠 Tech Stack

* **Python 3.12**
* **FastAPI**
* **SQLAlchemy**
* **Alembic**
* **PostgreSQL**
* **Docker & Docker Compose**
* **Poetry**

---

## 📁 Project Structure

```
movie-rating-backend/
├── app/                # FastAPI application
│   ├── controller/     # API routes
│   ├── services/       # Business logic
│   ├── repositories/   # Database access
│   ├── schemas/        # Pydantic models
│   ├── db/             # DB config & dependencies
│   └── main.py         # App entrypoint
├── alembic/             # Database migrations
├── scripts/
│   └── seed.sql         # Seed data (optional)
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml
└── README.md
```

---

# 🚀 Phase 1 — Back-End (API & Database)

### Goal

Design and implement a clean RESTful backend for managing movies and user ratings.

### Key Features

* Layered architecture:
  **Controller → Service → Repository**
* Standardized API responses:

  * Success:

    ```json
    { "status": "success", "data": ... }
    ```
  * Failure:

    ```json
    { "status": "failure", "error": { "code": 404, "message": "Movie not found" } }
    ```
* Pagination for movie lists
* Filtering & search via query parameters
* Aggregated ratings (`average_rating`, `ratings_count`) included in responses

---

## 📌 Implemented Endpoints

### List movies (with pagination)

```
GET /api/v1/movies?page=1&page_size=10
```

### Search & filter movies

(Search is implemented **via query parameters on the same endpoint**, not a separate route)

```
GET /api/v1/movies?title=&genre=&release_year=&page=&page_size=
```

### Movie details

```
GET /api/v1/movies/{movie_id}
```

### Create rating

```
POST /api/v1/movies/{movie_id}/ratings
```

Request body:

```json
{ "score": 10 }
```

### Validation Rules

* `score` must be an integer between **1 and 10** → otherwise `422`
* Invalid `release_year` → `422`
* Non-existent movie → `404`

---

# 📊 Phase 2 — Logging

### Goal

Replace `print` statements with **structured logging** to improve observability and debuggability.

### What Was Implemented

* Python `logging` module used throughout the project
* Logger per module:

  ```python
  logger = logging.getLogger(__name__)
  ```
* Correct log levels:

  * **INFO**: normal operations (e.g. listing movies, successful rating)
  * **WARNING**: invalid user input (e.g. rating out of range)
  * **ERROR**: database or runtime failures (with stacktrace)

### Logging Strategy

* **Controllers**: log request entry (route + parameters)
* **Services**: log business results (success, warning, error)
* **Repositories**: no logging (single responsibility principle)

All logs work both **locally** and **inside Docker containers**.

---

# 🐳 Phase 3 — Docker

### Goal

Make the entire project **portable and reproducible** using Docker.

### Implemented Components

* **Dockerfile**

  * Python 3.12 slim image
  * Dependency installation via Poetry
  * Runs FastAPI with Uvicorn on `0.0.0.0:8000`
* **Docker Compose**

  * `app` service (FastAPI)
  * `db` service (PostgreSQL 16)
  * Shared network
  * Persistent database volume
  * Environment-based configuration

### Run with Docker

```bash
docker compose up --build
```

Open Swagger UI:

```
http://127.0.0.1:8000/docs
```

Stop services:

```bash
docker compose down
```

---

# ⚙️ Local Development Setup (Without Docker)

### 1) Install dependencies

```powershell
poetry install
```

### 2) Environment variables

Create a `.env` file (do NOT commit it):

```powershell
Copy-Item .\.env.example .\.env
```

### 3) Start PostgreSQL (Docker)

```powershell
docker compose up -d db
```

### 4) Run migrations

```powershell
$env:PYTHONPATH = (Get-Location).Path
poetry run alembic upgrade head
```

### 5) (Optional) Seed database

```powershell
Get-Content .\scripts\seed.sql | docker exec -i movie_rating_db psql -U movie_user -d movie_rating_db
```

### 6) Run server

```powershell
poetry run uvicorn app.main:app --reload
```

Swagger:

```
http://127.0.0.1:8000/docs
```

---

## ⚠️ Notes

* `cast` is a **reserved keyword** in PostgreSQL.
  In raw SQL scripts it must be quoted as `"cast"`.
* Seed script errors do **not** affect API functionality or Docker evaluation.

---

## ✅ Project Status

* ✔ Phase 1 — Back-End API
* ✔ Phase 2 — Logging
* ✔ Phase 3 — Docker

🎉 **Project is complete and ready for submission.**