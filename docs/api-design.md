
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

## Course APIs

All course endpoints require a valid JWT access token.

### List Courses

- **Method:** `GET`
- **Endpoint:** `/api/v1/courses`
- **Access:** Authenticated users
- **Success:** `200 OK`

Returns the course catalog.

### Get Course Details

- **Method:** `GET`
- **Endpoint:** `/api/v1/courses/{course_id}`
- **Access:** Authenticated users
- **Success:** `200 OK`
- **Failure:** `404 Not Found`

Returns the details of a specific course.

### Create Course

- **Method:** `POST`
- **Endpoint:** `/api/v1/courses`
- **Access:** Admin only
- **Success:** `201 Created`
- **Failure:** `400 Bad Request`, `403 Forbidden`

Request body:

```json
{
  "title": "Python Fundamentals",
  "description": "Learn Python basics",
  "instructor_name": "Test Instructor",
  "duration_hours": 20
}
```

### Update Course

- **Method:** `PATCH`
- **Endpoint:** `/api/v1/courses/{course_id}`
- **Access:** Admin only
- **Success:** `200 OK`
- **Failure:** `400 Bad Request`, `403 Forbidden`, `404 Not Found`

Only supplied fields are updated.

### Delete Course

- **Method:** `DELETE`
- **Endpoint:** `/api/v1/courses/{course_id}`
- **Access:** Admin only
- **Success:** `204 No Content`
- **Failure:** `400 Bad Request`, `403 Forbidden`, `404 Not Found`

Courses with existing enrollments cannot be deleted.

## Enrollment APIs

All enrollment endpoints require a valid JWT access token. The user ID is derived from the authenticated JWT identity.

### List My Enrollments

- **Method:** `GET`
- **Endpoint:** `/api/v1/enrollments`
- **Access:** Authenticated user
- **Success:** `200 OK`

Returns only the authenticated user's enrollments.

### Enroll in a Course

- **Method:** `POST`
- **Endpoint:** `/api/v1/enrollments/{course_id}`
- **Access:** Authenticated user
- **Success:** `201 Created`
- **Failure:** `400 Bad Request`, `404 Not Found`

Creates an enrollment for the authenticated user. Duplicate enrollments are rejected.

### Unenroll from a Course

- **Method:** `DELETE`
- **Endpoint:** `/api/v1/enrollments/{enrollment_id}`
- **Access:** Enrollment owner
- **Success:** `204 No Content`
- **Failure:** `404 Not Found`

Deletes the enrollment only if it belongs to the authenticated user.

## Response Format

Successful JSON responses use the standard wrapper:

```json
{
  "data": {}
}
```

List endpoints return an array inside `data`. Delete endpoints return `204 No Content` without a response body.

### Get Dashboard Summary

- **Method:** `GET`
- **Endpoint:** `/api/v1/dashboard/summary`
- **Authentication:** Required (JWT)

**Success Response — `200 OK`**

```json
{
  "data": {
    "enrolled_course_count": 3
  }
}
```

**Description:** Returns the total number of courses in which the authenticated student is currently enrolled.

Error Responses:

- `401 Unauthorized` — Missing or invalid authentication token.
