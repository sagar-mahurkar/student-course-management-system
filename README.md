# Student Course Management System (SCMS)

A full-stack MVP for students to discover courses and manage enrollments, and for administrators to manage the course catalog.

## MVP capabilities

- Student registration and login using JWT authentication.
- Controlled administrator provisioning; public registration always creates a student account.
- Authenticated course catalog and course detail views.
- Admin-only course creation, update, and deletion.
- Student enrollment, enrollment listing, and unenrollment.
- Student dashboard with enrollment count.
- PostgreSQL persistence.
- Flask REST API and Vue 3 frontend.

## Technology stack

| Area | Technology |
|---|---|
| Backend | Python, Flask, Flask-JWT-Extended |
| Validation | Pydantic |
| ORM / database | SQLAlchemy, PostgreSQL, psycopg 3 |
| Frontend | Vue 3, TypeScript, Vite |
| Client state / routing | Pinia, Vue Router |
| HTTP client / styling | Axios, Bootstrap |
| Backend tests | pytest |

## Repository layout

```text
.
├── backend/
│   ├── app/
│   │   ├── config/          # Environment-backed settings
│   │   ├── database/        # PostgreSQL database initializer
│   │   ├── errors/          # Application errors and handlers
│   │   ├── extensions/      # SQLAlchemy, JWT, and CORS extensions
│   │   ├── models/          # User, Course, Enrollment
│   │   ├── modules/         # Auth, courses, enrollments, dashboard, health
│   │   └── seeders/         # Optional initial administrator seeder
│   ├── tests/
│   ├── requirements.txt
│   └── run.py
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── layouts/
│   │   ├── pages/
│   │   ├── router/
│   │   ├── services/
│   │   └── stores/
│   └── package.json
└── docs/
    ├── api-design.md
    ├── database-design.md
    ├── git-workflow-conventions.md
    ├── project-playbook.md
    ├── requirements.md
    └── testing-strategy.md
```

## Prerequisites

- Python version compatible with the pinned backend dependencies.
- Node.js and npm compatible with the installed Vite toolchain.
- PostgreSQL running locally.
- A PostgreSQL role with permission to connect to the maintenance database and create the application database on first startup.

## Local setup

### 1. Configure the backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Edit `backend/.env` and set a strong local `JWT_SECRET_KEY` and valid PostgreSQL credentials. The application reads the environment configuration and can create the configured application database if it does not exist. The PostgreSQL role therefore needs the required database-creation privilege.

To provision an initial administrator, intentionally set `ADMIN_SEED_ENABLED=true` and provide `ADMIN_SEED_FULL_NAME`, `ADMIN_SEED_EMAIL`, and `ADMIN_SEED_PASSWORD`. Keep this disabled unless you are provisioning the administrator. Do not commit `.env` or real secrets.

Start the backend from the `backend/` directory:

```bash
python run.py
```

The local API base is `http://localhost:5000`; the health endpoint is `http://localhost:5000/health`.

### 2. Configure the frontend

In a second terminal:

```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

The default frontend URL is `http://localhost:5173`. `VITE_API_BASE_URL` defaults to `http://localhost:5000/api/v1`.

### 3. Verify the application

Backend tests:

```bash
cd backend
python -m pytest -v
```

Frontend type-check and production build:

```bash
cd frontend
npm run build
```

The backend test suite was reported as passing **58 tests** during Phase 12/13 work. Full student and administrator workflows were also manually tested through the frontend. Run the commands above in the current environment when you need a fresh verification result.

## API documentation

See [`docs/api-design.md`](docs/api-design.md) for endpoints, payloads, authentication, and response formats.

## Database documentation

See [`docs/database-design.md`](docs/database-design.md) for entities, relationships, constraints, indexes, and integrity rules.

## MVP scope boundaries

The MVP does not include instructor-specific accounts, assignments, grading, attendance, payments, email verification, password reset, notifications, course-content uploads, advanced search/filtering/pagination, Docker, CI/CD, or production deployment.

## Database schema lifecycle note

The current application initializes the database and creates tables through SQLAlchemy metadata (`db.create_all()`). A versioned migration workflow is not currently present in the repository. For environments where schema evolution and production deployment matter, add and review a migration tool/workflow before making schema changes.

## Project status

- Phase 12 — Frontend–Backend Integration: complete.
- Phase 13 — End-to-End Testing & Bug Fixing: complete; backend suite reported at 58 passing tests and student/admin workflows manually tested through the frontend.
- Phase 14 — Documentation & Cleanup: documentation pack prepared; perform the final repository review and verification before marking the phase complete.
