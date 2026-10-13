# Software Project Playbook

> A reusable, project-agnostic operational guide for taking software
> projects from idea to deployment.
>
> This document is intentionally practical. Use it as an external
> memory: when you forget how to set something up, follow the relevant
> recipe instead of relying on memory.

--------------------------------------------------------------------------------

## 1. Purpose

This playbook is a project-agnostic reference for building and
maintaining software projects. It records reusable workflows, decision
rules, setup recipes, verification steps, and lessons that can be
applied to future projects.

It is not a specification for one application, and it must not prescribe
a fixed technical stack or architecture.

The goal is to keep the **engineering lifecycle consistent** while
allowing implementation depth to change with project size and
requirements.

### Core principle

> **Requirements determine architecture and technology. Do not introduce
> technology merely because it is available.**

--------------------------------------------------------------------------------

## 2. Project Classification

Classify the project before deciding how much infrastructure and process
it needs.

### 2.1 Small MVP

Typical characteristics:

- Limited features
- Small domain
- One backend
- One frontend
- Relational database
- Short implementation timeline

Priorities:

1. Scope control
2. Clean foundation
3. Core functionality
4. Validation and testing
5. Documentation

Avoid unnecessary:

- Redis
- background workers
- microservices
- complex deployment infrastructure
- premature optimization

--------------------------------------------------------------------------------

### 2.2 Medium Project

Typical characteristics:

- Multiple modules
- Authentication and authorization
- More complex APIs
- More frontend state
- More testing
- More users/data

Add where justified:

- stronger testing
- API documentation
- Docker
- CI
- migrations
- structured logging
- staging environment

--------------------------------------------------------------------------------

### 2.3 Complex Project

Typical characteristics:

- Large domain
- Many entities/modules
- concurrency
- complex business rules
- multiple workflows
- significant data integrity requirements
- potentially multiple developers

Use:

- Jira
- meaningful Sprints
- detailed requirements
- stronger architecture
- explicit concurrency strategy
- comprehensive testing
- Docker
- CI/CD
- observability
- deployment strategy

### Rule

Project size changes the **depth of each phase**, not the existence of
the lifecycle.

--------------------------------------------------------------------------------

## 3. Standard Project Lifecycle

Every project follows these phases.

    Phase Name
--------------------------------------------------------------------------------
        0 Git & Repository Setup
        1 Requirements & Scope
        2 Entity & Database Design
        3 Backend Setup
        4 Database Setup
        5 Backend Models
        6 API Foundation & Authentication
        7 Feature APIs
        8 Summary / Aggregation APIs
        9 Backend Testing & Hardening
       10 Frontend Setup
       11 Frontend UI
       12 Frontend--Backend Integration
       13 End-to-End Testing & Bug Fixing
       14 Documentation & Cleanup

Infrastructure and operations are introduced across these phases:

- migrations
- Docker
- Redis
- CI/CD
- deployment
- logging/monitoring
- environment management

Do not create unnecessary standalone phases merely for technology.

--------------------------------------------------------------------------------

## 4. Phase Timing

Track actual working time.

### Commands

### Start a phase

    Start Phase N

This starts the active-work timer.

### Take a break

    Taking a break

This pauses the active-work timer.

### Resume

    Resuming

This resumes the timer.

### Stop for the day

    Stopping for today

The phase remains incomplete.

### Resume on another day

    Resuming Phase N

### Complete

    Phase N done

Record:

- total elapsed time
- total break time
- effective working time

### Formula

    Effective work
    = Total elapsed time - Break time

The purpose is not to optimize blindly. It is to learn where project
time is actually being spent.

--------------------------------------------------------------------------------

## 5. Phase 0 --- Git & Repository Setup

Git is the **first project activity**.

Do not start application development before the repository exists.

### 5.1 What

Create:

- local Git repository
- GitHub repository
- initial project structure
- `.gitignore`
- initial commit

### 5.2 Why

Git provides:

- history
- rollback
- branches
- collaboration
- pull requests
- safe experimentation

### 5.3 How

    mkdir my-project
    cd my-project
    
    git init
    git branch -M main
    
    git remote add origin <github-repository-url>

Create the initial project files, then:

    # Stage only intended files after reviewing git status and git diff.
    git add <file1> <file2>
    git commit -m "chore: initialize project"
    git push -u origin main

### 5.4 Branching rule

For non-trivial work, use a feature branch rather than working directly
on `main`.

    main
      │
      ├── feature/requirements
      ├── feature/database-design
      ├── feature/backend-setup
      └── feature/authentication

Standard workflow:

    Create feature branch
            ↓
    Implement phase work
            ↓
    Commit meaningful changes
            ↓
    Push branch
            ↓
    Create Pull Request
            ↓
    Review
            ↓
    Merge into main
            ↓
    Delete branch

### 5.5 Feature branch

    git checkout -b feature/backend-setup

After work:

    git status
    git diff
    git diff --check
    
    # Stage only intended files after reviewing git status and git diff.
    git add <file1> <file2>
    git commit -m "feat: set up backend application"
    git push -u origin feature/backend-setup

After the PR is merged:

    git checkout main
    git pull origin main
    git branch -d feature/backend-setup

If the remote branch still exists:

    git push origin --delete feature/backend-setup

### 5.6 Commit rules

Prefer meaningful commits:

    feat: add resource repository
    fix: correct date filtering
    test: add search regression test
    docs: document API authentication
    chore: configure pytest

Do not create meaningless commits such as:

    changes
    update
    final
    test

--------------------------------------------------------------------------------

## 6. Jira and Project Management

Use Jira for genuinely complex projects.

Do not create meaningless administrative Sprints just to say Jira was
used.

### Complex-project workflow

    Requirements
        ↓
    Epics
        ↓
    Stories / Tasks
        ↓
    Sprint planning
        ↓
    Development
        ↓
    PR
        ↓
    Review / Merge
        ↓
    Sprint completion

Git branches and Jira issues should be traceable.

Example:

    JIRA-123 Add resource filtering
            ↓
    feature/JIRA-123-resource-filtering
            ↓
    PR
            ↓
    Merge

For small MVPs, GitHub Issues or the project plan may be sufficient
unless Jira provides clear value.

--------------------------------------------------------------------------------

## 7. Phase 1 --- Requirements & Scope

Do not begin implementation before defining the MVP.

### 7.1 Define

- problem statement
- target users
- functional requirements
- non-functional requirements
- MVP features
- out-of-scope features
- acceptance criteria

### 7.2 MVP rule

An MVP is the smallest version that delivers the core user value.

It is **not** a badly implemented version of the full product.

### 7.3 Scope document

Create:

    docs/requirements.md

Recommended structure:

    # Requirements
    
    ## Problem Statement
    
    ## Users
    
    ## Functional Requirements
    
    ## Non-Functional Requirements
    
    ## MVP Scope
    
    ## Out of Scope
    
    ## Acceptance Criteria

### 7.4 Scope control

When a new idea appears:

    Is it required for the MVP?
           │
       ┌───┴───┐
       Yes     No
       │        │
    Implement  Defer
                ↓
           Out of Scope

Do not expand the MVP during implementation without an explicit reason.

--------------------------------------------------------------------------------

## 8. Phase 2 --- Entity & Database Design

Design the data model before writing ORM models.

### 8.1 Process

    Requirements
        ↓
    Identify entities
        ↓
    Identify attributes
        ↓
    Identify relationships
        ↓
    Define cardinality
        ↓
    Normalize
        ↓
    Define constraints
        ↓
    Define indexes from query patterns
        ↓
    Define transactions/concurrency needs

### 8.2 Document

Create:

    docs/database-design.md

Include:

- entities
- attributes
- primary keys
- foreign keys
- relationships
- constraints
- data types
- indexes
- delete/update behavior
- pending decisions

### 8.3 Database rules

Prefer database-enforced integrity where appropriate.

Examples:

- `PRIMARY KEY`
- `UNIQUE`
- `NOT NULL`
- `CHECK`
- `FOREIGN KEY`

Do not rely entirely on application validation for integrity that the
database can safely enforce.

### 8.4 Data type decisions

For PostgreSQL:

- UUID for identifiers where appropriate
- `NUMERIC(p,s)` for monetary values
- `DATE` for business dates
- `TIMESTAMPTZ` for timestamps

Example:

    amount NUMERIC(12,2) NOT NULL

Do not use floating-point types for money.

### 8.5 Indexing

Do not index every column.

Start from actual query patterns.

Example:

    CREATE INDEX idx_resources_user_date
    ON resources(user_id, created_at);

The index exists because the application frequently filters by user and
filters or orders records by creation date.

--------------------------------------------------------------------------------

## 9. Phase 3 --- Backend Setup

Choose the backend framework based on requirements and existing project
constraints.

Common options:

- Flask
- FastAPI
- Express + TypeScript

Do not choose a framework merely because it is fashionable.

### 9.1 Flask recipe

Typical dependencies:

    pip install Flask
    pip install Flask-SQLAlchemy
    pip install Flask-JWT-Extended
    pip install Flask-Cors
    pip install python-dotenv
    pip install psycopg

Development dependencies should be separated where appropriate.

Use:

    requirements.txt

and keep the environment reproducible.

Typical application structure:

    backend/
    ├── app/
    │   ├── __init__.py
    │   ├── config.py
    │   ├── extensions.py
    │   ├── models/
    │   └── modules/
    ├── tests/
    ├── requirements.txt
    └── run.py

Use the Flask application factory pattern.

### 9.2 Express + TypeScript recipe

Typical foundation:

    npm init -y
    npm install express
    npm install dotenv
    npm install cors
    npm install jsonwebtoken
    npm install bcrypt
    npm install typeorm
    npm install pg

Development tooling:

    npm install -D typescript
    npm install -D ts-node
    npm install -D @types/node
    npm install -D @types/express
    npm install -D @types/jsonwebtoken
    npm install -D @types/bcrypt

Use a `tsconfig.json` appropriate for the project and keep configuration
reproducible.

### 9.3 FastAPI

FastAPI is an available alternative when the project benefits from:

- Python
- automatic OpenAPI generation
- typed request/response models
- asynchronous endpoints where appropriate

Do not introduce FastAPI simply to have another framework.

--------------------------------------------------------------------------------

## 10. Environment & Configuration Management

Configuration must be explicit.

### 10.1 Local environment

Use:

    .env
    .env.example

Example:

    DATABASE_HOST=localhost
    DATABASE_PORT=5432
    DATABASE_NAME=app_db
    DATABASE_USER=postgres
    DATABASE_PASSWORD=your_password
    
    JWT_SECRET_KEY=replace_me
    FRONTEND_ORIGIN=http://localhost:5173

Never commit real secrets.

### 10.2 `.env.example`

Commit safe placeholders:

    DATABASE_HOST=
    DATABASE_PORT=
    DATABASE_NAME=
    DATABASE_USER=
    DATABASE_PASSWORD=
    JWT_SECRET_KEY=
    FRONTEND_ORIGIN=

### 10.3 Rules

- `.env` → ignored by Git
- `.env.example` → tracked
- production secrets → supplied by deployment environment/secret
    manager
- do not hard-code secrets
- keep configuration separate from business logic

--------------------------------------------------------------------------------

## 11. Phase 4 --- Database Setup

Database provisioning and schema creation are different concerns.

### 11.1 Database lifecycle

    Application initialization
            ↓
    Read database configuration
            ↓
    Connect to PostgreSQL server
            ↓
    Check application database
            ↓
    Create database if missing
            ↓
    Connect application to database
            ↓
    Apply schema/migrations
            ↓
    Verify connection

Automatic database provisioning is a reusable setup option, especially
for local development and disposable test environments. Keep it separate
from schema migration and make its behavior environment-aware.

### 11.2 Important distinction

    Database creation
    ≠
    Schema creation
    ≠
    ORM models
    ≠
    Database migrations

- Database provisioning creates the PostgreSQL database.
- Schema defines tables, constraints, indexes, etc.
- ORM models represent database structures in application code.
- Migrations track and apply schema changes over time.

--------------------------------------------------------------------------------

## 12. Database Migrations

Migrations are the standard mechanism for controlled schema evolution.

### 12.1 Why

Without migrations, changing production schema becomes manual and
difficult to reproduce.

A migration records:

    Schema version N
          ↓
    Migration
          ↓
    Schema version N+1

### 12.2 Flask

Use Alembic/Flask-Migrate when appropriate.

Typical workflow:

    flask db init
    flask db migrate -m "create users table"
    flask db upgrade

Inspect generated migrations before applying them.

### 12.3 TypeORM

Typical workflow:

    npx typeorm migration:generate ./src/migrations/InitialSchema
    npx typeorm migration:run

Exact commands depend on the TypeORM project configuration.

### 12.4 Migration rules

- Review generated migrations.
- Do not edit production schema manually when a migration should
    represent the change.
- Keep migrations in Git.
- Test migrations on a clean database.
- Consider rollback strategy.
- Do not confuse migrations with seed data.

--------------------------------------------------------------------------------

## 13. Database Initialization and Seed Data

### Database Initialization

For projects that require automatic local database setup, distinguish
these operations:

1. **Database provisioning:** Create the database if it does not exist.
2. **Schema initialization:** Create or migrate database tables.
3. **Seed data:** Insert required initial records.

These operations serve different purposes and must not be treated as
interchangeable.

- Initialize the database connection and ORM before schema operations.
- Ensure all models are registered before schema creation or
    migration.
- Use migrations for controlled schema evolution once a migration
    workflow is established.
- Keep provisioning controlled by explicit configuration and
    environment.
- Use least-privilege credentials; the runtime application account
    should not receive database-server privileges it does not need.
- Never run destructive schema operations automatically against an
    existing database.
- In production, prefer a deliberate provisioning/deployment step over
    silently creating databases at application startup.

### Administrator Seed Data

When an application requires an initial administrator, provide a
controlled seeding mechanism.

- Read initial administrator credentials from environment variables or
    another approved secret source.
- Never hardcode real credentials in source control.
- Hash passwords using the application's existing password-hashing
    mechanism.
- Create the administrator only when the configured account does not
    already exist.
- Make seeding idempotent: repeated execution must not create
    duplicate accounts or reset an existing password.
- Do not allow public registration to assign privileged roles.
- Keep administrator provisioning separate from ordinary user
    registration.
- Document required environment variables in `.env.example` using
    non-secret placeholders.
- Test both initial creation and repeated execution.

### Startup Sequence

Database startup should follow the appropriate sequence for the project:

Database provisioning → ORM initialization → Model registration → Schema
initialization → Required seed data → Application ready

Use migrations instead of automatic table creation when a migration
workflow has been established.

--------------------------------------------------------------------------------

## 14. Phase 5 --- Backend Models

Create ORM models from the approved database design.

For each model verify:

- table name
- columns
- data types
- primary key
- foreign keys
- relationships
- constraints
- indexes
- timestamps
- delete behavior

After implementation:

    Database design
          ↓
    ORM model
          ↓
    Migration/schema
          ↓
    Database

The model should represent the database design; it should not silently
redefine business requirements.

--------------------------------------------------------------------------------

## 15. Backend Architecture

Use layering when it creates clear responsibilities.

A proven pattern:

    Request
       ↓
    Route / Controller
       ↓
    Schema / Validation
       ↓
    Service
       ↓
    Repository
       ↓
    ORM
       ↓
    PostgreSQL

### Route

Responsible for:

- HTTP route
- request extraction
- invoking validation
- invoking service
- returning HTTP response

Routes should not contain business logic or direct database queries.

### Schema / Validation

Responsible for:

- request structure
- types
- boundary validation
- response structures where useful

Validation happens before business logic.

### Service

Responsible for:

- business rules
- orchestration
- application logic
- coordinating repository operations
- transaction boundaries where required

Services should not depend on HTTP request/response objects.

### Repository

Responsible for:

- database queries
- persistence
- SQLAlchemy/TypeORM operations

Repositories should not contain business rules.

### Model

Responsible for:

- table representation
- relationships
- database constraints
- ORM mapping

Models should not contain HTTP flow logic.

--------------------------------------------------------------------------------

## 16. Phase 6 --- API Foundation & Authentication

Build common API infrastructure before feature APIs.

### 16.1 API base path

Use a versioned API path for non-trivial APIs:

    /api/v1

Example:

    GET /api/v1/resources

### 16.2 Health endpoint

Create:

    GET /health

Minimum purpose:

- application is running

As infrastructure matures, it can also verify required dependencies such
as the database.

--------------------------------------------------------------------------------

## 17. Authentication

Recommended basic flow:

    Register
       ↓
    Hash password
       ↓
    Store user

Then:

    Login
       ↓
    Verify password
       ↓
    Issue JWT
       ↓
    Client stores access token
       ↓
    Protected request
       ↓
    JWT verification
       ↓
    Authenticated identity

### Passwords

Never store plaintext passwords.

Use an established password hashing library.

### JWT

Keep the signing secret outside source code.

Example environment variable:

    JWT_SECRET_KEY=...

Protected requests:

    Authorization: Bearer <access-token>

--------------------------------------------------------------------------------

## 18. User Isolation

For multi-user applications, user identity must come from authenticated
context.

Do not trust:

    {
      "user_id": "some-other-user"
    }

from the client to determine ownership.

Use:

    JWT
     ↓
    Authenticated identity
     ↓
    Service/repository user scope
     ↓
    Database query

Every user-owned query should enforce the authenticated user's scope.

--------------------------------------------------------------------------------

## 19. Authorization

Authentication answers:

> Who are you?

Authorization answers:

> What are you allowed to do?

Examples:

- member
- administrator
- operator

Keep authorization checks close to the business operation rather than
relying only on frontend visibility.

--------------------------------------------------------------------------------

## 20. API Design

Document the API in:

    docs/api-design.md

Document:

- endpoint
- HTTP method
- authentication
- request body
- query parameters
- response
- status codes
- validation errors
- authorization rules

### Consistent success response

Example:

    {
      "data": {
        "id": "uuid",
        "name": "Example"
      }
    }

### Consistent error response

Example:

    {
      "error": {
        "code": "VALIDATION_ERROR",
        "message": "Invalid request data"
      }
    }

--------------------------------------------------------------------------------

## 21. API Documentation / OpenAPI / Swagger

For non-trivial APIs, maintain an OpenAPI contract/documentation.

It should make it possible to understand:

- available endpoints
- parameters
- request schemas
- response schemas
- authentication
- status codes

If the chosen framework generates OpenAPI automatically, use that
capability.

Do not maintain documentation that contradicts the implementation.

When an endpoint changes:

    Implementation change
           ↓
    API documentation update
           ↓
    Tests

--------------------------------------------------------------------------------

## 22. Phase 7 --- Feature APIs

Implement one feature/module at a time.

Recommended order:

    Foundation
       ↓
    Authentication
       ↓
    Core CRUD
       ↓
    Relationships
       ↓
    Filtering/Search
       ↓
    Pagination
       ↓
    Business-specific operations

For each feature:

1. Define endpoint.
2. Define request schema.
3. Define response.
4. Define service behavior.
5. Define repository operations.
6. Add validation.
7. Add authorization/user scope.
8. Add tests.
9. Verify manually where useful.
10. Update API documentation.

--------------------------------------------------------------------------------

## 23. Filtering, Search and Pagination

Implement based on actual requirements.

Common query parameters:

    ?page=1
    &per_page=20
    &search=food
    &type=example
    &start_date=2026-10-01
    &end_date=2026-10-31

Keep parameter names consistent between frontend and backend.

For every filter verify:

- backend parameter
- frontend parameter
- validation
- query behavior
- user scope
- pagination behavior
- test coverage

--------------------------------------------------------------------------------

## 24. Phase 8 --- Summary / Aggregation APIs

Aggregation APIs should be implemented separately from ordinary CRUD
when they have different behavior.

Examples:

    GET /summary
    GET /dashboard
    GET /reports

Typical operations:

- `SUM`
- `COUNT`
- grouping
- date-based aggregation
- category aggregation

Keep aggregation logic in the service/repository layers rather than
routes.

--------------------------------------------------------------------------------

## 25. Transactions and Concurrency

Use database transactions when multiple operations must succeed or fail
together.

Example:

    Begin transaction
        ↓
    Validate
        ↓
    Update A
        ↓
    Update B
        ↓
    Commit

If an operation cannot safely be partially applied:

    Rollback

For complex systems, explicitly identify concurrency risks.

Possible strategies include:

- optimistic locking
- pessimistic locking
- unique constraints
- atomic database operations
- transaction isolation

Do not introduce locking mechanisms without identifying the race
condition they solve.

This is especially important when concurrent operations can update the
same resource or violate a business invariant.

--------------------------------------------------------------------------------

## 26. Redis

Redis is an **optional infrastructure component**.

Do not add Redis merely because it is popular.

Introduce it when a concrete requirement exists.

Common uses:

- caching
- rate limiting
- sessions
- temporary state
- queues
- background-job coordination

Typical flow:

    Client
      ↓
    API
      ↓
    Redis cache?
      ├── hit → return
      └── miss
           ↓
        Database
           ↓
        Cache result

Rules:

- Define cache invalidation behavior.
- Define TTL where appropriate.
- Do not treat Redis as the source of truth when PostgreSQL is the
    source of persistent data.
- Measure whether caching actually helps.

--------------------------------------------------------------------------------

## 27. Background Jobs

Use asynchronous/background processing only when the workload justifies
it.

Examples:

- email sending
- report generation
- large imports
- notifications
- scheduled processing

Typical architecture:

    API
     ↓
    Queue
     ↓
    Worker
     ↓
    Long-running task

Redis can serve as infrastructure for some queue systems, but Redis does
not automatically imply that a worker system is required.

--------------------------------------------------------------------------------

## 28. Phase 9 --- Backend Testing & Hardening

Testing depth scales with:

- risk
- complexity
- criticality
- time

Do not chase arbitrary 100% coverage.

### Flask

Typical stack:

    pytest

Run:

    cd backend
    python -m pytest -v

Use a dedicated test database.

A useful pattern:

    Test starts
        ↓
    Create/recreate test schema
        ↓
    Run test
        ↓
    Clean up

Keep test secrets separate from development/production secrets.

### Node/Express

Use:

- Jest
- Supertest

Typical categories:

- unit tests
- API/integration tests
- authentication tests
- authorization tests
- validation tests
- database behavior tests

--------------------------------------------------------------------------------

## 29. Regression Testing

Whenever a bug is found:

    Bug
     ↓
    Fix
     ↓
    Add regression test
     ↓
    Run complete relevant suite

Example:

    def test_resource_search(auth_client, resource):
        response = auth_client.get("/api/v1/resources?search=example")
        assert response.status_code == 200

The test prevents the same defect from silently returning later.

--------------------------------------------------------------------------------

## 30. Phase 10 --- Frontend Setup

Choose frontend technology based on project requirements.

### React

Typical foundation:

- Vite
- React
- TypeScript
- React Router
- Axios/fetch
- state management when needed

### Vue

Typical foundation:

- Vite
- Vue 3
- TypeScript
- Vue Router
- Pinia when shared state requires it
- Axios/fetch
- Bootstrap or another UI system when appropriate

Do not add state management merely because the framework supports it.

--------------------------------------------------------------------------------

## 31. Frontend Architecture

A clean frontend can use:

    frontend/src/
    ├── assets/
    ├── components/
    ├── layouts/
    ├── pages/
    ├── router/
    ├── services/
    ├── stores/
    ├── types/
    ├── App.*
    ├── main.*
    └── style.css

Responsibilities:

### Pages

Page-level composition and user flow.

### Components

Reusable UI behavior.

### Services

API communication.

### Stores

Shared application state.

### Router

Navigation and route protection.

### Types

Shared frontend data contracts.

--------------------------------------------------------------------------------

## 32. Frontend Authentication

Typical flow:

    Login
     ↓
    API
     ↓
    JWT
     ↓
    Store token
     ↓
    API client attaches token
     ↓
    Protected routes

API client should handle:

- base URL
- authorization header
- common errors
- 401 handling where appropriate

Frontend route guards improve UX, but backend authorization remains
authoritative.

--------------------------------------------------------------------------------

## 33. Phase 11 --- Frontend UI

Implement pages in priority order:

1. Authentication
2. Application shell/layout
3. Core feature pages
4. Forms
5. Lists/tables
6. Filtering/search
7. Summary/dashboard
8. Error/loading/empty states
9. Responsive behavior

Reuse components when there is genuine repeated behavior.

Avoid premature component abstraction.

--------------------------------------------------------------------------------

## 34. Phase 12 --- Frontend--Backend Integration

Integration is a separate engineering phase.

Verify:

- API base URL
- CORS
- environment variables
- authentication token
- request payloads
- query parameters
- response mapping
- error handling
- loading states
- empty states

Example:

    Frontend
       ↓
    API Client
       ↓
    HTTP
       ↓
    Backend Route
       ↓
    Service
       ↓
    Database

A feature is not complete merely because the backend endpoint works.

--------------------------------------------------------------------------------

## 35. Phase 13 --- End-to-End Testing & Bug Fixing

Test real user journeys.

Example:

    Login
     ↓
    Application home
     ↓
    Create resource
     ↓
    Verify resource
     ↓
    Update resource
     ↓
    Verify update
     ↓
    Delete resource
     ↓
    Verify deletion
     ↓
    Logout

Test:

- happy paths
- validation failures
- authorization
- filters
- search
- pagination
- refresh behavior
- critical integration paths

When a defect is found:

    Reproduce
     ↓
    Identify layer
     ↓
    Fix root cause
     ↓
    Add regression test if appropriate
     ↓
    Run relevant suite
     ↓
    Run full suite
     ↓
    Repeat E2E flow

--------------------------------------------------------------------------------

## 36. Docker

Docker provides reproducible application environments.

### 36.1 Basic structure

Typical project:

    Dockerfile
    .dockerignore
    docker-compose.yml

For a full-stack project:

    Frontend container
    Backend container
    PostgreSQL container
    Redis container (only if required)

### 36.2 Dockerfile

A Dockerfile should:

1. Start from an appropriate base image.
2. Set working directory.
3. Install dependencies.
4. Copy application code.
5. Configure runtime.
6. Expose the required port.
7. Start the application.

### 36.3 Docker Compose

Use Compose for local multi-service development.

Example conceptual topology:

    frontend
       │
    backend
       │
       ├── postgres
       └── redis

### 36.4 Volumes

Use persistent volumes for development database data when appropriate.

Remember:

> A Docker volume is not a backup strategy.

### 36.5 Verification

    docker compose build
    docker compose up
    docker compose ps

Verify:

- containers are running
- backend health endpoint works
- database connection works
- frontend reaches backend
- logs contain no startup errors

--------------------------------------------------------------------------------

## 37. CI/CD

CI/CD should be introduced progressively.

### Level 1 --- Continuous Integration

On push/PR:

    Install dependencies
          ↓
    Format/lint checks
          ↓
    Type checking
          ↓
    Tests
          ↓
    Build

### Level 2 --- Docker CI

    CI
     ↓
    Build Docker image
     ↓
    Verify image

### Level 3 --- Continuous Deployment

    Merge to main
          ↓
    CI
          ↓
    Build image
          ↓
    Push image
          ↓
    Deploy
          ↓
    Run migrations
          ↓
    Health check
          ↓
    Smoke test

### GitHub Actions

A typical repository can use:

    .github/
    └── workflows/
        ├── ci.yml
        └── cd.yml

Start simple. Add complexity only when deployment requirements justify
it.

--------------------------------------------------------------------------------

## 38. Deployment

Deployment is the transition from local development to a running
environment.

### Basic deployment sequence

    Build
     ↓
    Configure environment
     ↓
    Provision database
     ↓
    Apply migrations
     ↓
    Deploy backend
     ↓
    Deploy frontend
     ↓
    Health check
     ↓
    Smoke test

### Production configuration

Verify:

- production environment variables
- secrets
- database URL
- CORS origin
- frontend API URL
- JWT secret
- HTTPS
- migrations
- logging
- health check

Do not copy a development `.env` into production blindly.

--------------------------------------------------------------------------------

## 39. Logging

Logging should answer:

- What happened?
- When did it happen?
- Where did it happen?
- Why did it fail?

Useful levels:

- DEBUG
- INFO
- WARNING
- ERROR
- CRITICAL

Avoid logging:

- passwords
- JWT secrets
- sensitive personal data
- database credentials

Development logs can be more verbose than production logs.

--------------------------------------------------------------------------------

## 40. Monitoring and Observability

Start simple.

Minimum operational visibility:

    Health check
    +
    Application logs
    +
    Error visibility

As the system grows, add:

- metrics
- dashboards
- alerting
- error tracking
- log aggregation
- distributed tracing where genuinely needed

Do not build a full observability platform for a small MVP without a
reason.

--------------------------------------------------------------------------------

## 41. Security Checklist

Before completion, verify:

- passwords are hashed
- secrets are not committed
- JWT secret is externalized
- protected endpoints verify authentication
- authorization is enforced
- user-owned data is scoped to the authenticated user
- input is validated
- database constraints are present
- SQL is parameterized/ORM-based
- CORS is intentional
- production uses HTTPS
- error responses do not leak sensitive internals
- dependencies are reviewed for known vulnerabilities

--------------------------------------------------------------------------------

## 42. Code Quality

Use appropriate tooling for the chosen language.

Configure pre-commit hooks when they prevent recurring mistakes. Keep
the same checks available as explicit local commands and in CI; hooks
are a convenience, not a substitute for CI.

Typical checks:

    Formatter
       ↓
    Linter
       ↓
    Type checker
       ↓
    Tests
       ↓
    Build

Examples:

### Python

Possible tools:

- Ruff
- Black
- mypy

### TypeScript

Possible tools:

- ESLint
- Prettier
- TypeScript compiler

Use only tools that provide real value for the project.

--------------------------------------------------------------------------------

## 43. Dependency Management

Before adding a package ask:

1. Is there a real requirement?
2. Does the standard library already solve it?
3. Is the dependency maintained?
4. Does it introduce significant complexity?
5. Is it required in production or only development?

Keep dependency versions reproducible using the ecosystem's lockfile or
equivalent dependency-pinning mechanism.

Review dependency changes in Git. Periodically run the ecosystem's
vulnerability audit and investigate findings; do not blindly apply
breaking upgrades.

--------------------------------------------------------------------------------

## 44. API Rate Limiting and Caching

These are optional capabilities.

Introduce rate limiting when abuse or high request volume is a realistic
concern.

Introduce caching when:

- the same expensive data is requested repeatedly
- data can tolerate temporary staleness
- profiling indicates database/API work is a bottleneck

Do not cache merely to make the architecture look advanced.

--------------------------------------------------------------------------------

## 45. Performance

Performance work should be evidence-driven.

Check first:

- database query patterns
- missing/incorrect indexes
- N+1 queries
- excessive API requests
- large response payloads
- unnecessary frontend rendering

Then optimize.

Rule:

> **Measure first. Optimize second.**

--------------------------------------------------------------------------------

## 46. Database Backup & Recovery

For deployed systems:

- establish backups
- understand retention
- test restoration
- document recovery procedure

Important:

    Migration ≠ Backup
    Docker volume ≠ Backup

A migration describes schema evolution.

A backup protects data.

--------------------------------------------------------------------------------

## 47. Graceful Shutdown and Failure Handling

Production services should handle shutdown cleanly.

Consider:

- active requests
- database connections
- background workers
- queued work
- container termination

Also define sensible:

- request timeouts
- retries
- error handling

Do not blindly retry every failure.

--------------------------------------------------------------------------------

## 48. Final Documentation

At the end of the project, verify documentation.

Recommended set:

    docs/
    ├── requirements.md
    ├── database-design.md
    ├── api-design.md
    ├── frontend-design.md
    ├── testing-strategy.md
    └── project-playbook.md

Not every project needs every file. Use the documents that provide
value.

### Documentation principle

Document decisions and operational knowledge.

Do not document obvious code line-by-line.

--------------------------------------------------------------------------------

## 49. Phase 14 --- Documentation & Cleanup

Final checklist:

    [ ] Requirements reflect final MVP
    [ ] Out-of-scope items remain clear
    [ ] Database design is current
    [ ] Migrations are committed
    [ ] API documentation is current
    [ ] Frontend documentation is current
    [ ] Testing strategy is current
    [ ] Backend tests pass
    [ ] Frontend build succeeds
    [ ] E2E critical flows pass
    [ ] No accidental debug code
    [ ] No secrets committed
    [ ] .env.example is current
    [ ] README is current
    [ ] Docker configuration works if applicable
    [ ] CI passes
    [ ] Deployment documentation is current if deployed
    [ ] Git diff reviewed
    [ ] Git status clean

--------------------------------------------------------------------------------

## 50. Definition of Done

A phase is not complete merely because the code was written.

Use:

    Implementation
        ↓
    Verification
        ↓
    Documentation
        ↓
    Git review
        ↓
    Commit
        ↓
    Push
        ↓
    Pull Request
        ↓
    Review
        ↓
    Merge
        ↓
    Branch cleanup

For each phase, define the expected deliverable and acceptance criteria
before implementation. Mark the phase complete only after its checks
pass.

For each phase:

    [ ] Requirements satisfied
    [ ] Implementation complete
    [ ] Relevant tests complete
    [ ] Verification complete
    [ ] Documentation updated
    [ ] Git diff reviewed
    [ ] Commit(s) created
    [ ] Branch pushed
    [ ] PR reviewed/approved
    [ ] PR merged
    [ ] Branch deleted

--------------------------------------------------------------------------------

## 51. Troubleshooting Method

Do not jump immediately to workarounds.

Use:

    Symptom
      ↓
    Read exact error
      ↓
    Identify failing layer
      ↓
    Check configuration
      ↓
    Check dependencies
      ↓
    Check inputs
      ↓
    Check logs/stack trace
      ↓
    Fix root cause
      ↓
    Verify

Avoid hacks such as:

- arbitrary `PYTHONPATH` changes
- import hacks
- proxy hacks
- unexplained environment overrides
- disabling validation
- bypassing type checks
- weakening database constraints just to make an error disappear

If configuration is wrong, fix the project configuration.

--------------------------------------------------------------------------------

## 52. Technology Selection Rules

Choose technology according to the requirement.

### Backend

| Requirement | Possible choice |
| --- | --- |
| Lightweight Python API | Flask |
| Typed Python API / OpenAPI-heavy API | FastAPI |
| TypeScript backend | Express + TypeScript |

### Frontend

| Requirement | Possible choice |
| --- | --- |
| React ecosystem | React |
| Vue ecosystem | Vue |

### Database

Use PostgreSQL when a relational database is appropriate.

### Redis

Optional. Introduce only when its capabilities solve a real requirement.

### Docker

Prefer reproducible containerization as project maturity increases.

### CI/CD

CI should become standard engineering practice; CD depth depends on
deployment requirements.

--------------------------------------------------------------------------------

## 53. Project Maturity Model

Use this to decide how much infrastructure to introduce.

### Stage 1 --- Basic MVP

    Git
    Requirements
    Database
    Backend
    Frontend
    Tests
    Documentation

### Stage 2 --- Professional Development

    +
    Migrations
    API documentation
    Docker
    CI
    Environment management
    Logging

### Stage 3 --- Deployable Application

    +
    CD
    Production deployment
    Health checks
    Monitoring
    Backups
    Security hardening

### Stage 4 --- Scaled Application

Only when justified:

    +
    Redis
    Background workers
    Advanced caching
    Queueing
    Load balancing
    Advanced observability
    Scaling strategies

--------------------------------------------------------------------------------

## 54. Reusable Engineering Lessons

- Keep MVP scope explicit and defer nonessential features.
- Treat database provisioning, schema initialization, migrations, and
    seed data as separate operations.
- Make ownership and authorization rules explicit for multi-user
    systems.
- Use layered architecture only when each layer has a clear
    responsibility.
- Backend tests, frontend tests, integration tests, and end-to-end
    tests detect different classes of defects.
- Keep API contracts and parameter names consistent across frontend
    and backend.
- Add regression tests for defects that could recur.
- Increase domain modeling, transaction design, and concurrency
    controls as business rules and data-integrity risks become more
    complex.
- Use project-management tooling only when it improves planning,
    traceability, and delivery.

--------------------------------------------------------------------------------

## 55. Operational Recipe Format

Whenever adding a new technology or project procedure to this playbook,
prefer this format:

### What

What is being configured?

### Why

Why does the project need it?

### Where

Which files/directories are involved?

### How

Give:

- dependencies
- commands
- configuration
- file contents/patterns
- implementation sequence

### Verify

Give an explicit verification step.

Example:

    What → Docker
    Why → reproducible environment
    Where → Dockerfile, compose file
    How → build and run
    Verify → container status + health endpoint + logs

This format is especially important for technologies that are easy to
forget.

--------------------------------------------------------------------------------

## 56. Reusable Project Startup Checklist

Before writing application code:

    [ ] Create Git repository
    [ ] Create .gitignore and initial commit
    [ ] Push initial repository
    [ ] Classify project size
    [ ] Create project structure
    [ ] Decide whether Jira is needed
    [ ] Define requirements
    [ ] Define MVP
    [ ] Define out of scope
    [ ] Design entities
    [ ] Design database
    [ ] Choose backend
    [ ] Choose frontend
    [ ] Decide infrastructure requirements

--------------------------------------------------------------------------------

## 57. Reusable Backend Checklist

    [ ] Backend initialized
    [ ] Configuration loaded
    [ ] Environment variables defined
    [ ] Database provisioning implemented
    [ ] Database connection verified
    [ ] Migrations configured
    [ ] Models created
    [ ] Health endpoint created
    [ ] Error handling configured
    [ ] Validation configured
    [ ] Authentication implemented
    [ ] Authorization implemented
    [ ] User isolation verified
    [ ] Feature APIs implemented
    [ ] Aggregation APIs implemented
    [ ] API documentation updated
    [ ] Tests implemented
    [ ] Tests passing

--------------------------------------------------------------------------------

## 58. Reusable Frontend Checklist

    [ ] Frontend initialized
    [ ] Environment configuration created
    [ ] Router configured
    [ ] API client configured
    [ ] Authentication state configured
    [ ] Protected routes configured
    [ ] Layout created
    [ ] Core pages created
    [ ] Forms created
    [ ] Loading states handled
    [ ] Error states handled
    [ ] Empty states handled
    [ ] API integration complete
    [ ] Responsive behavior checked
    [ ] Build succeeds

--------------------------------------------------------------------------------

## 59. Reusable Infrastructure Checklist

    [ ] Environment configuration
    [ ] .env ignored
    [ ] .env.example committed
    [ ] Docker added if justified
    [ ] PostgreSQL container/configuration verified
    [ ] Redis added if justified
    [ ] CI configured
    [ ] CD configured if deployment requires it
    [ ] Health check available
    [ ] Logging configured
    [ ] Monitoring configured where needed
    [ ] Deployment procedure documented
    [ ] Database migrations run during deployment
    [ ] Backup/recovery strategy defined for production

--------------------------------------------------------------------------------

## 60. Reusable Git Completion Checklist

    [ ] Working tree reviewed
    [ ] git diff --check
    [ ] Tests pass
    [ ] Build passes
    [ ] Documentation updated
    [ ] Meaningful commit(s)
    [ ] Branch pushed
    [ ] PR created
    [ ] PR reviewed
    [ ] PR approved
    [ ] PR merged
    [ ] Branch deleted
    [ ] Main updated locally

--------------------------------------------------------------------------------

## 61. Future Improvement Rule

This document is intentionally a living playbook.

After every project:

1. Identify what was difficult to remember.
2. Identify what caused avoidable mistakes.
3. Identify what took longer than expected.
4. Identify new infrastructure that was actually used.
5. Identify useful patterns that proved themselves.
6. Remove advice that did not provide value.
7. Update the relevant recipe.
8. Keep the lifecycle stable unless there is a strong reason to change
    it.

Do not add technology to the playbook merely because it was encountered.

Add it when:

- it solved a real problem,
- it is likely to be reused,
- or it represents a deliberate future capability worth learning.

--------------------------------------------------------------------------------

## 62. Final Principle

The objective of this playbook is not to make every project large.

The objective is to make every project **predictable**.

    Requirements
        ↓
    Design
        ↓
    Build
        ↓
    Verify
        ↓
    Integrate
        ↓
    Test
        ↓
    Document
        ↓
    Deploy
        ↓
    Observe
        ↓
    Learn
        ↓
    Improve the playbook

Use the smallest architecture and infrastructure that correctly solves
the project's requirements.

Then increase sophistication when the requirements demand it.
