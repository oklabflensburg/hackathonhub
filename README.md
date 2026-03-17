# Hackathon Dashboard

Hackathon Dashboard is a full-stack application for discovering hackathons, publishing projects, managing teams, and handling user activity such as comments, votes, notifications, and reports.

The repository currently contains:

- A Nuxt 4 frontend in `frontend3/`
- A FastAPI backend in `backend/`
- Docker assets for local multi-service development
- Alembic migrations for backend schema changes

## Current Stack

### Frontend

- Nuxt 4
- Vue 3
- TypeScript
- Pinia
- Tailwind CSS
- `@nuxtjs/i18n`
- Vitest

Primary frontend manifest:

- `frontend3/package.json`

Primary frontend config:

- `frontend3/nuxt.config.ts`
- `frontend3/eslint.config.mjs`
- `frontend3/vitest.config.ts`

### Backend

- FastAPI
- SQLAlchemy
- Alembic
- Pydantic Settings
- JWT / cookie-based auth
- SQLite by default, PostgreSQL supported and used in Docker Compose

Primary backend bootstrap and config:

- `backend/app/main.py`
- `backend/app/core/config.py`
- `backend/app/core/database.py`
- `backend/requirements.txt`
- `backend/alembic.ini`

## Repository Layout

```text
hackathon-dashboard/
├── backend/
│   ├── app/
│   │   ├── api/v1/              # FastAPI route modules
│   │   ├── core/                # Settings, auth, database, permissions
│   │   ├── domain/              # SQLAlchemy models and Pydantic schemas
│   │   ├── i18n/                # Localization middleware and helpers
│   │   ├── repositories/        # Data access layer
│   │   ├── services/            # Business logic
│   │   └── utils/               # Supporting helpers
│   ├── migrations/              # Alembic migrations
│   ├── templates/               # Email templates
│   ├── test_*.py                # Backend tests and scripts
│   ├── requirements.txt
│   └── Dockerfile
├── frontend3/
│   ├── app/
│   │   ├── app.vue              # Global app shell
│   │   ├── assets/
│   │   ├── components/          # Atomic and feature UI components
│   │   ├── composables/         # Frontend feature logic and API access
│   │   ├── middleware/          # Route/auth middleware
│   │   ├── pages/               # Nuxt file-based routes
│   │   ├── plugins/
│   │   ├── stores/              # Pinia stores
│   │   ├── types/
│   │   └── utils/               # API client and helpers
│   ├── i18n/
│   ├── public/
│   ├── tests/
│   ├── package.json
│   ├── pnpm-lock.yaml
│   └── Dockerfile
├── docker-compose.yml
└── README.md
```

## Architecture Notes

### Frontend Architecture

The frontend is organized around Nuxt pages, Pinia stores, and composables.

- `frontend3/app/app.vue` defines the global shell with header, sidebar, footer, mobile navigation, and notification mounting.
- `frontend3/app/pages/` contains route-level screens such as projects, hackathons, teams, notifications, settings, admin, and auth flows.
- `frontend3/app/composables/` is the main feature layer for client-side domain logic. This is where project, team, notification, report, auth, and hackathon operations are wrapped.
- `frontend3/app/stores/` holds shared state such as auth, UI notifications, teams, theme, preferences, and voting.
- `frontend3/app/utils/api-client.ts` is the central HTTP abstraction used by the composables and stores.
- `frontend3/app/middleware/auth.global.ts` and `frontend3/app/middleware/auth.ts` enforce authentication-aware routing.

In practice, most frontend changes are made in:

1. `frontend3/app/pages/...`
2. `frontend3/app/composables/...`
3. `frontend3/app/stores/...`
4. `frontend3/app/components/...`

### Backend Architecture

The backend follows a layered package layout.

- `backend/app/main.py` creates the FastAPI app, applies middleware, mounts uploads, and includes all API routers.
- `backend/app/api/v1/` contains route modules grouped by feature.
- `backend/app/services/` contains business logic.
- `backend/app/repositories/` contains data access code.
- `backend/app/domain/models/` contains SQLAlchemy models.
- `backend/app/domain/schemas/` contains request and response schemas.
- `backend/app/core/` contains configuration, auth, database setup, and permission helpers.
- `backend/app/i18n/` contains localization middleware and translation helpers.

Most backend feature work flows through:

1. `backend/app/api/v1/<feature>/routes.py`
2. `backend/app/services/<feature>_service.py`
3. `backend/app/repositories/<feature>_repository.py`
4. `backend/app/domain/models/...` and `backend/app/domain/schemas/...`

## Main Feature Areas

The repo currently has meaningful functionality in these areas:

- Authentication: email/password, GitHub OAuth, Google OAuth, refresh tokens, 2FA
- Projects: CRUD, voting, comments, reporting, engagement stats
- Hackathons: list/detail flows plus related project and report screens
- Teams: creation, membership, invitations, team reports
- Notifications: in-app preferences, registry, delivery, push support, email templates
- User settings and admin user management

Backend router entrypoints are collected in:

- `backend/app/main.py`

Some of the most central backend route files are:

- `backend/app/api/v1/auth/routes.py`
- `backend/app/api/v1/projects/routes.py`
- `backend/app/api/v1/hackathons/routes.py`
- `backend/app/api/v1/teams/routes.py`
- `backend/app/api/v1/notifications/routes.py`
- `backend/app/api/v1/team_reports/routes.py`
- `backend/app/api/v1/reports/routes.py`

Some of the most central frontend files are:

- `frontend3/app/app.vue`
- `frontend3/app/stores/auth.ts`
- `frontend3/app/composables/useProjects.ts`
- `frontend3/app/composables/useTeams.ts`
- `frontend3/app/composables/useNotifications.ts`
- `frontend3/app/utils/api-client.ts`

## Local Development

### Prerequisites

- Python 3.12 recommended for the backend
- Node.js 20 recommended for the frontend
- `pnpm` for frontend package management
- PostgreSQL if you want to mirror the Docker setup locally

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file in `backend/` with at least the values you need for your environment. The backend reads settings from:

- `backend/app/core/config.py`

Common variables include:

- `DATABASE_URL`
- `SECRET_KEY`
- `DEBUG`
- `GITHUB_CLIENT_ID`
- `GITHUB_CLIENT_SECRET`
- `GITHUB_CALLBACK_URL`
- `GOOGLE_CLIENT_ID`
- `GOOGLE_CLIENT_SECRET`
- `GOOGLE_CALLBACK_URL`
- `FRONTEND_URL`
- `VAPID_PUBLIC_KEY`
- `VAPID_PRIVATE_KEY`

Run database migrations:

```bash
cd backend
alembic upgrade head
```

Run the API locally:

```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Setup

```bash
cd frontend3
pnpm install
```

Create a frontend `.env` file if needed. The main runtime variable is:

- `NUXT_PUBLIC_API_URL`

Run the frontend locally:

```bash
cd frontend3
pnpm dev
```

The frontend config is in:

- `frontend3/nuxt.config.ts`

## Docker Development

Docker Compose is available at:

- `docker-compose.yml`

It defines:

- `backend`
- `frontend`
- `db` (PostgreSQL 15)

Typical usage:

```bash
docker compose up --build
```

## Testing and Linting

### Frontend

Lint:

```bash
cd frontend3
pnpm lint
```

Build:

```bash
cd frontend3
pnpm build
```

Vitest is configured, but there is currently no explicit `test` script in `frontend3/package.json`. You can run it directly:

```bash
cd frontend3
pnpm exec vitest
```

Relevant files:

- `frontend3/vitest.config.ts`
- `frontend3/tests/setup.ts`

### Backend

The backend has multiple test files in `backend/`, including both `unittest`-style and `pytest`-style tests, but there is no single repo-level pytest configuration file.

Examples:

- `backend/test_notification_api.py`
- `backend/test_notification_email_templates.py`
- `backend/test_rbac_team_reports.py`

Run a backend test file explicitly, for example:

```bash
cd backend
python -m pytest test_notification_email_templates.py
```

or:

```bash
cd backend
python test_rbac_team_reports.py
```

## Migrations

Alembic configuration lives in:

- `backend/alembic.ini`
- `backend/migrations/env.py`

Common commands:

```bash
cd backend
alembic upgrade head
alembic downgrade -1
alembic history
```

There is additional migration documentation in:

- `backend/README_ALEMBIC.md`

## Uploads and Email Templates

Uploaded files are exposed by the backend under `/static/uploads` and are backed by:

- `backend/uploads/`

Email templates live in:

- `backend/templates/emails/`

These templates are tied into the notification and email orchestration services under:

- `backend/app/services/`
- `backend/app/utils/template_registry.py`

## Notes for Contributors

- The backend README references in older documentation may describe a flatter structure that no longer matches the code. The active backend code is under `backend/app/`.
- Frontend business logic is concentrated in composables and stores rather than in page files alone.
- The notifications, teams, reports, and auth flows are substantial subsystems and are likely to be touched by cross-cutting changes.

## Useful File References

- `backend/app/main.py`
- `backend/app/core/config.py`
- `backend/app/core/database.py`
- `backend/app/api/v1/`
- `backend/app/services/`
- `backend/app/repositories/`
- `backend/app/domain/models/`
- `frontend3/nuxt.config.ts`
- `frontend3/app/app.vue`
- `frontend3/app/pages/`
- `frontend3/app/composables/`
- `frontend3/app/stores/`
- `frontend3/app/utils/api-client.ts`
