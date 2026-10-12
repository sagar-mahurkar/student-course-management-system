
# API Design

## Base URL

Local development: `http://localhost:5000`

API prefix: `/api/v1`

## Common Response Formats

### Success

```json
{
  "data": {}
}
```

### Error

```json
{
  "error": {
    "message": "Error description"
  }
}
```

## Health

### Check API Health

- **Method:** GET
- **Path:** `/health`
- **Authentication:** Not required
- **Success:** `200 OK`

Example response:

```json
{
  "status": "ok"
}
```

## Authentication

### Register

- **Method:** POST
- **Path:** `/api/v1/auth/register`
- **Authentication:** Not required
- **Success:** `201 Created`

Request body:

```json
{
  "full_name": "Test Student",
  "email": "student@example.com",
  "password": "TestPassword123"
}
```

Successful response data includes `id`, `full_name`, `email`, `role`, and `created_at`.

The password is hashed before storage and is never returned.

New registrations receive the `student` role. Clients cannot assign their own role.

Common errors:

- `400 Bad Request`: Invalid request, validation failure, or duplicate email.

### Login

- **Method:** POST
- **Path:** `/api/v1/auth/login`
- **Authentication:** Not required
- **Success:** `200 OK`

Request body:

```json
{
  "email": "student@example.com",
  "password": "TestPassword123"
}
```

Successful response data:

```json
{
  "access_token": "<access-token>",
  "user": {
    "id": "<user-id>",
    "full_name": "Test Student",
    "email": "student@example.com",
    "role": "student"
  }
}
```

Common errors:

- `400 Bad Request`: Invalid request or validation failure.
- `401 Unauthorized`: Invalid email or password.

### Get Current User

- **Method:** GET
- **Path:** `/api/v1/auth/me`
- **Authentication:** Required
- **Success:** `200 OK`

Request header:

```http
Authorization: Bearer <access-token>
```

Successful response data includes `id`, `full_name`, `email`, and `role`.

Common errors:

- `401 Unauthorized`: Missing token or invalid user identity.
- `422 Unprocessable Entity`: Invalid JWT under the current JWT configuration.

## Validation Rules

- `full_name`: Required; 1–100 characters.
- `email`: Required; must be a valid email address.
- `password` during registration: Required; 8–128 characters.
- `password` during login: Required; 1–128 characters.
- Unknown request fields are rejected.
- Email addresses are normalized to lowercase by the authentication service.
- Password whitespace is preserved.

## Authentication and Security

- Passwords are stored as hashes, never as plaintext.
- JWT signing uses the `JWT_SECRET_KEY` environment variable.
- Protected endpoints validate JWTs before processing requests.
- User identity is derived from the authenticated JWT, not a client-supplied user ID.
- Passwords and password hashes are excluded from API responses.
