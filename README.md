# Student Course Management System (SCMS)

## 1. Project Overview

The Student Course Management System (SCMS) is a full-stack MVP that allows students to discover courses and manage their enrollments. Administrators can maintain the course catalog.

## 2. MVP Features

### Student

- Register and log in.
- Browse the course catalog and view course details.
- Enroll in a course.
- View personal enrollments and the dashboard enrollment count.
- Unenroll from a course.

### Administrator

- Log in using a provisioned administrator account.
- Create, view, update, and delete courses.
- Manage the course catalog.
- Delete a course only when it has no enrollments.

### Security and Data Integrity

- JWT-based authentication for protected endpoints.
- Password hashing; passwords are never returned by the API.
- Public registration always assigns the `student` role.
- Backend authorization restricts course mutations to administrators.
- Database constraints prevent duplicate emails and duplicate user-course enrollments.
- Enrollment ownership is enforced by the backend.

## 3. Technology Stack

- **Backend:** Python, Flask, Flask-JWT-Extended
- **Validation:** Pydantic
- **ORM:** SQLAlchemy
- **Database:** PostgreSQL
- **Database driver:** psycopg 3
- **Frontend:** Vue 3, TypeScript, Vite
- **Routing:** Vue Router
- **State management:** Pinia
- **HTTP client:** Axios
- **Styling:** Bootstrap
- **Backend testing:** pytest

## 4. Repository Structure

```text
.
├── backend/
│   ├── app/
│   │   ├── config/
│   │   ├── database/
│   │   ├── errors/
│   │   ├── extensions/
│   │   ├── models/
│   │   ├── modules/
│   │   └── seeders/
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

## 5. Prerequisites

- Python compatible with the backend dependencies.
- Node.js and npm compatible with the frontend dependencies.
- PostgreSQL running locally.
- A PostgreSQL role with permission to connect to the maintenance database and create the configured application database if it does not already exist.

## 6. Local Setup

### 6.1 Backend

From the repository root:

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Configure `backend/.env` with the correct PostgreSQL connection settings and a strong local `JWT_SECRET_KEY`.

To provision an initial administrator, enable the project's administrator seeding configuration and provide the required administrator name, email, and password. Keep seeding disabled unless it is intentionally needed. Never commit `.env` or real credentials.

Start the backend from `backend/`:

```bash
python run.py
```

- Backend base URL: `http://localhost:5000`
- Health endpoint: `http://localhost:5000/health`
- API prefix: `/api/v1`

### 6.2 Frontend

Open a second terminal:

```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

Configure the frontend API base URL to point to `http://localhost:5000/api/v1`.

- Default frontend URL: `http://localhost:5173`
- Do not put private secrets in `VITE_*` variables; these values are exposed to the browser.

## 7. Verification Commands

### Backend tests

Run from `backend/`:

```bash
python -m pytest -v
```

### Frontend production build

Run from `frontend/`:

```bash
npm run build
```

### Git review

Run from the repository root:

```bash
git status
git diff
git diff --check
```

The Phase 12–13 session reported 58 passing backend tests and manual testing of student and administrator workflows through the frontend. Re-run the commands above to obtain fresh results for the current checkout.

## 8. Documentation

- [Requirements and MVP scope](docs/requirements.md)
- [Database design](docs/database-design.md)
- [API design](docs/api-design.md)
- [Testing strategy](docs/testing-strategy.md)
- [Git workflow conventions](docs/git-workflow-conventions.md)
- [Project playbook](docs/project-playbook.md)

## 9. MVP Scope Boundaries

The following are outside the current MVP:

- Instructor-specific accounts and permissions.
- Assignments, examinations, quizzes, and grading.
- Attendance tracking.
- Payments and subscriptions.
- Email verification and password reset.
- Notifications and messaging.
- Course content uploads and video streaming.
- Advanced search, filtering, pagination, and analytics.
- Docker, CI/CD, and production deployment.

## 10. Database Schema Lifecycle

The current project documentation describes SQLAlchemy metadata-based table creation (`db.create_all()`). A versioned migration workflow is not documented as implemented. Before introducing schema changes in a persistent or production environment, add and review a migration workflow rather than relying on metadata creation alone.

## 11. Project Phase Status

The following status reflects the recorded project progression. For phases where a precise duration or independent verification result was not recorded, this README does not infer one.

| Phase | Description | Status |
| --- | --- | --- |
| 0 | Git & Repository Setup | Complete |
| 1 | Requirements & Scope | Complete |
| 2 | Entity & Database Design | Complete |
| 3 | Backend Setup | Complete |
| 4 | Database Setup | Complete |
| 5 | Backend Models | Complete |
| 6 | API Foundation & Authentication | Complete |
| 7 | Feature APIs | Complete |
| 8 | Summary / Aggregation APIs | Complete |
| 9 | Backend Testing & Hardening | Complete |
| 10 | Frontend Setup | Complete |
| 11 | Frontend UI | Complete |
| 12 | Frontend–Backend Integration | Complete |
| 13 | End-to-End Testing & Bug Fixing | Complete |
| 14 | Documentation & Cleanup | Complete |
