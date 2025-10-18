# Basic CRUD API (Django + DRF)

Proyecto de práctica con Django y Django REST Framework que expone una API CRUD para notas y categorías, autenticación JWT y endpoints de administración para usuarios, grupos y permisos.

## Funcionalidades

- Autenticación JWT: emisión, refresco y blacklist de tokens.
- API REST para Notas y Categorías con DRF ViewSets y router.
- Permisos por endpoint:
  - Notas: lectura pública; crear requiere usuario autenticado; actualizar/eliminar restringido a dueño o admin.
  - Categorías: lectura pública; crear/actualizar/eliminar controlado por permisos de modelo (DjangoModelPermissions).
- Endpoints de administración (solo admin) para Usuarios, Grupos y Permisos.
- Navegación con DRF Browsable API (`/api-auth/` para login de sesión en el navegador).
- CORS preparado (lista de orígenes vacía de inicio).
- Dockerfile y docker-compose con Postgres.

## Modelos

- `Category`:
  - `title` (CharField, 50)
  - `description` (CharField, 100)
  - `created_at` (DateField auto)
  - `updated_at` (DateField auto)
- `Note`:
  - `title` (CharField, 200)
  - `description` (TextField)
  - `user` (FK a `auth.User`; se asigna automáticamente al crear)
  - `category` (FK a `Category`)
  - `is_published` (BooleanField, default False)
  - `created_at`/`updated_at` (DateTime auto)

## Serializers

- `NoteSerializer` (Hyperlinked): `fields='__all__'`; `user` es solo lectura y expone `user.id`.
- `CategorySerializer` (Hyperlinked): `fields='__all__'`.
- `UserSerializer` (Hyperlinked): campos de usuario + `password` (solo escritura), `groups`, `permissions`.
  - Sobrescribe `create` y `update` para hashear contraseña y asignar grupos/permisos.
- `GroupSerializer` (Hyperlinked): incluye `permissions`.
- `PermissionSerializer` (ModelSerializer): campos básicos.

## Permisos por vista

- `NoteViewSet`:
  - `GET/HEAD/OPTIONS`: `AllowAny` (público).
  - `POST`: `IsAuthenticated` (requiere JWT); `perform_create` asigna `user=request.user`.
  - `PUT/PATCH/DELETE`: `IsOwnerOrAdmin` (dueño del objeto o staff admin).
- `CategoryViewSet`:
  - `GET/HEAD/OPTIONS`: `AllowAny`.
  - Mutaciones: `DjangoModelPermissions` (requiere permisos de modelo asignados en Django).
- `UserViewSet`, `GroupViewSet`, `PermissionViewSet`: `IsAdminUser` (solo administradores).

## Endpoints

Base: `http://<host>:8000/`

- Admin: `GET /admin/`
- DRF Login (navegable): `GET /api-auth/login/`
- JWT:
  - `POST /api/token/`  (body: `username`, `password`)
  - `POST /api/token/refresh/`  (body: `refresh`)
  - `POST /api/token/blacklist/` (body: `refresh`)
- Notas y Categorías:
  - `GET/POST /api/notes/`
  - `GET/PUT/PATCH/DELETE /api/notes/{id}/`
  - `GET/POST /api/categories/`
  - `GET/PUT/PATCH/DELETE /api/categories/{id}/`
- Administración de cuentas (solo admin):
  - `GET/POST /api/users/`, `GET/PUT/PATCH/DELETE /api/users/{id}/`
  - `GET/POST /api/groups/`, `GET/PUT/PATCH/DELETE /api/groups/{id}/`
  - `GET/POST /api/permissions/`, `GET/PUT/PATCH/DELETE /api/permissions/{id}/`

## Configuración y entorno

- Django: `5.1.x`
- DRF: `3.16.x`
- JWT: `djangorestframework-simplejwt` con blacklist.
- DB: configurable por variables de entorno; docker-compose usa Postgres.
- CORS: `CORS_ALLOWED_ORIGINS = []` (ajustar para frontends).

Variables de entorno principales (`.env.copy` como referencia):

- `DJANGO_SECRET_KEY`, `DEBUG`, `DJANGO_ALLOWED_HOSTS`
- `DATABASE_ENGINE`, `DATABASE_NAME`, `DATABASE_USERNAME`, `DATABASE_PASSWORD`, `DATABASE_HOST`, `DATABASE_PORT`

## Ejecutar con Docker

1) Copiar `.env.copy` a `.env` y ajustar valores.
2) `docker compose up --build` (levanta Postgres y la app en `:8000`).

## Ejecutar local (sin Docker)

- Python 3.13 recomendado
- `python -m venv .venv && source .venv/bin/activate`
- `pip install -r requirements.txt`
- Exportar variables de entorno mínimas (o usar SQLite por defecto)
- `python manage.py migrate`
- `python manage.py createsuperuser`
- `python manage.py runserver`

## Uso básico

1) Crear superusuario y obtener token: `POST /api/token/`.
2) Autenticar peticiones con header `Authorization: Bearer <access>`.
3) Crear notas con `POST /api/notes/` (se asigna automáticamente el usuario autenticado).
4) Editar/eliminar notas propias o como admin.