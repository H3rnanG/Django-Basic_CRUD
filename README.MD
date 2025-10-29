# Basic CRUD API (Django + DRF)

Production‑ready practice project exposing a CRUD API for Notes and Categories using Django and Django REST Framework (DRF). It includes JWT authentication, admin endpoints for Users/Groups/Permissions, filtering, full‑text search (PostgreSQL), ordering, and pagination.

## Features

- Authentication: JWT with access/refresh and blacklist (SimpleJWT).
- Notes and Categories: ViewSets routed via DRF router.
- Permissions by endpoint:
  - Notes: public read; create requires authentication; update/delete require owner or staff.
  - Categories: public read; create/update/delete guarded by Django model permissions.
- Accounts admin endpoints: Users, Groups, and Permissions (admin‑only).
- Filtering and search:
  - Filter notes by publication, user, category, date range.
  - Order by created date or category; full‑text search (PostgreSQL) across title/description.
- Pagination: page‑number pagination (configurable page size).
- DRF browsable API: quick navigation and session login at `/api-auth/`.
- CORS ready: allowlist empty by default.
- Docker setup with PostgreSQL.

## Tech Stack

- Python 3.12/3.13
- Django 5.1.x
- Django REST Framework 3.16.x
- SimpleJWT (+ blacklist)
- django-filter
- PostgreSQL (recommended; required for full‑text search). SQLite works for basic CRUD.

## Data Model

- Category
  - `title`: Char(50)
  - `description`: Char(100)
  - `created_at` / `updated_at`: auto Date
- Note
  - `title`: Char(200)
  - `description`: Text
  - `user`: FK to `auth.User` (assigned on create)
  - `category`: FK to `Category`
  - `is_published`: Bool (default False)
  - `created_at` / `updated_at`: auto DateTime

## Endpoints

Base URL: `http://<host>:8000/`

- Admin: `GET /admin/`
- DRF login (browsable): `GET /api-auth/login/`
- JWT
  - `POST /api/token/` (body: `username`, `password`)
  - `POST /api/token/refresh/` (body: `refresh`)
  - `POST /api/token/blacklist/` (body: `refresh`)
- Notes & Categories
  - `GET/POST /api/notes/`
  - `GET/PUT/PATCH/DELETE /api/notes/{id}/`
  - `GET /api/notes/my-notes/` (authenticated; returns your notes)
  - `GET/POST /api/categories/`
  - `GET/PUT/PATCH/DELETE /api/categories/{id}/`
- Accounts (admin‑only)
  - `GET/POST /api/users/`, `GET/PUT/PATCH/DELETE /api/users/{id}/`
  - `GET/POST /api/groups/`, `GET/PUT/PATCH/DELETE /api/groups/{id}/`
  - `GET/POST /api/permissions/`, `GET/PUT/PATCH/DELETE /api/permissions/{id}/`

## Authentication & Authorization

- JWT: Use SimpleJWT access token on requests: `Authorization: Bearer <access>`.
- Notes
  - List: public; if authenticated, you see your notes + published notes; otherwise only published notes.
  - Retrieve: published notes are public; private notes require owner or staff.
  - Create: requires authentication; the server assigns `user=request.user`.
  - Update/Delete: owner or staff only.
- Categories
  - Safe methods (GET/HEAD/OPTIONS): public.
  - Mutations: require Django model permissions (`add`, `change`, `delete`).
- Admin endpoints: `IsAdminUser` (staff) only.

## Filtering, Ordering, Search (Notes)

Query params for `GET /api/notes/`:

- `is_published` (bool): filter by publication status. Example: `?is_published=true`
- `user` (int): user id. Example: `?user=5`
- `category` (str): category title (case‑insensitive). Example: `?category=Work`
- `created_after` / `created_before` (ISO8601): creation date range. Example: `?created_after=2024-10-01T00:00:00Z`
- `ordering` (str): fields: `created_at`, `category`; prefix with `-` for descending. Example: `?ordering=-created_at`
- `search` (str): full‑text search on `title` + `description`. Example: `?search=django`

Notes:
- Full‑text search requires PostgreSQL (`SearchVector`, `SearchQuery`). Not available on SQLite.

## Pagination

- Strategy: Page Number pagination (DRF).
- Page size: `20` by default.
- Param: `page`. Example: `GET /api/notes/?page=2`.
- Response shape: `{ count, next, previous, results: [...] }`.

## Configuration

- Django settings (relevant):
  - `REST_FRAMEWORK.DEFAULT_AUTHENTICATION_CLASSES = [JWTAuthentication]`
  - `REST_FRAMEWORK.DEFAULT_PERMISSION_CLASSES = [AllowAny]`
  - `REST_FRAMEWORK.DEFAULT_FILTER_BACKENDS = [DjangoFilterBackend]`
  - `REST_FRAMEWORK.DEFAULT_PAGINATION_CLASS = PageNumberPagination`
  - `REST_FRAMEWORK.PAGE_SIZE = 20`
  - `SIMPLE_JWT.ACCESS_TOKEN_LIFETIME = 5m`, `REFRESH_TOKEN_LIFETIME = 1d`
- CORS: `CORS_ALLOWED_ORIGINS = []` (configure for your frontend domains).

### Environment Variables (.env)

- `DJANGO_SECRET_KEY`, `DEBUG`, `DJANGO_ALLOWED_HOSTS`
- `DATABASE_ENGINE` (e.g. `postgresql` or `sqlite3`)
- `DATABASE_NAME`, `DATABASE_USERNAME`, `DATABASE_PASSWORD`, `DATABASE_HOST`, `DATABASE_PORT`

## Running Locally

Prereqs: Python 3.12+ and virtualenv.

1) Create and activate venv
   - `python -m venv .venv && source .venv/bin/activate`
2) Install dependencies
   - `pip install -r requirements.txt`
3) Configure environment
   - Copy `.env.copy` to `.env` and adjust values (or rely on SQLite defaults).
4) Migrate and create admin
   - `python manage.py migrate`
   - `python manage.py createsuperuser`
5) Run server
   - `python manage.py runserver`

## Running with Docker

1) Copy `.env.copy` to `.env` and set DB creds.
2) Build and start services
   - `docker compose up --build`
3) App runs at `http://localhost:8000/` (PostgreSQL provided by compose).

## Quick Usage Examples (curl)

- Obtain token
  - `curl -X POST http://localhost:8000/api/token/ -d 'username=admin&password=secret'`
- List published notes, ordered desc, page 2
  - `curl "http://localhost:8000/api/notes/?ordering=-created_at&page=2"`
- Full‑text search (Postgres)
  - `curl "http://localhost:8000/api/notes/?search=backend"`
- Filter by category and date
  - `curl "http://localhost:8000/api/notes/?category=Work&created_after=2024-10-01T00:00:00Z"`
- Create a note (authenticated)
  - `curl -X POST http://localhost:8000/api/notes/ \`
    `-H "Authorization: Bearer <access>" -H "Content-Type: application/json" \`
    `-d '{"title":"Hello","description":"World","category":1,"is_published":true}'`
- Get my notes
  - `curl -H "Authorization: Bearer <access>" http://localhost:8000/api/notes/my-notes/`

## Project Structure (high level)

```
basiccrud/            Django project settings and URLs
notes/                Notes & Categories app (models, views, filters, serializers)
accounts/             Admin endpoints for Users, Groups, Permissions
Dockerfile, compose.yml  Containerized dev setup with PostgreSQL
```

## Notes and Caveats

- Full‑text search is implemented using PostgreSQL features. If you run on SQLite, use filters/ordering but omit `search`.
- The browsable API at `/api-auth/` is useful for manual testing with session login.

---

This repository represents my first project built with Django and DRF.