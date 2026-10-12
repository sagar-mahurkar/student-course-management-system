# Student Course Management System — Database Design

## 1. Overview

This document defines the database schema for the Student Course Management System (SCMS).

**Database:** PostgreSQL  
**ORM:** SQLAlchemy  
**Naming convention:** `snake_case`  
**Primary key strategy:** UUID  
**Timestamp convention:** `TIMESTAMPTZ`

The database design supports student authentication, course catalog management, course enrollment, and the student dashboard.

## 2. Entities

The MVP requires three entities:

| Entity | Purpose |
| --- | --- |
| `users` | Stores student and administrator accounts. |
| `courses` | Stores course catalog information. |
| `enrollments` | Records student enrollments in courses. |

## 3. Entity Relationships

```text
users
  |
  | 1
  |
  | N
enrollments
  |
  | N
  |
  | 1
courses
```

Relationships:

- One user can have multiple enrollments.
- One course can have multiple enrollments.
- Each enrollment belongs to exactly one user and one course.
- A user can enroll in multiple courses.
- A course can have multiple students enrolled.
- A user-course pair must be unique in the enrollment table.

The `enrollments` table implements the many-to-many relationship between users and courses.

## 4. Table Definitions

### 4.1 `users`

Stores registered student and administrator accounts.

| Column | PostgreSQL type | Constraints | Description |
| --- | --- | --- | --- |
| `id` | UUID | Primary key, not null | Unique user identifier |
| `full_name` | VARCHAR(100) | Not null | User's full name |
| `email` | VARCHAR(255) | Unique, not null | User's email address |
| `password_hash` | VARCHAR(255) | Not null | Hashed password |
| `role` | VARCHAR(20) | Not null, default `'student'` | User authorization role |
| `created_at` | TIMESTAMPTZ | Not null, default current timestamp | Record creation time |
| `updated_at` | TIMESTAMPTZ | Not null, default current timestamp | Last record update time |

**Role values:**

- `student`
- `admin`

**Design decisions:**

- Passwords must never be stored in plaintext.
- Email addresses must be normalized to lowercase before storage and lookup.
- The database enforces email uniqueness.
- Public registration must always assign the `student` role. Administrator accounts must be provisioned through a controlled mechanism.
- `updated_at` must be updated when a user record changes.

### 4.2 `courses`

Stores the course catalog managed by administrators.

| Column | PostgreSQL type | Constraints | Description |
| --- | --- | --- | --- |
| `id` | UUID | Primary key, not null | Unique course identifier |
| `title` | VARCHAR(150) | Not null | Course title |
| `description` | TEXT | Not null | Course description |
| `instructor_name` | VARCHAR(100) | Not null | Instructor's display name |
| `duration_hours` | INTEGER | Not null, check greater than zero | Course duration in hours |
| `created_at` | TIMESTAMPTZ | Not null, default current timestamp | Record creation time |
| `updated_at` | TIMESTAMPTZ | Not null, default current timestamp | Last record update time |

**Design decisions:**

- Only administrators can create, update, or delete courses.
- Students and other authenticated users can view the course catalog.
- All existing courses are available for enrollment in this MVP; separate publication or availability statuses are out of scope.
- Course duration must be a positive integer.
- `updated_at` must be updated when a course changes.

### 4.3 `enrollments`

Associates students with courses and records when enrollment occurs.

| Column | PostgreSQL type | Constraints | Description |
| --- | --- | --- | --- |
| `id` | UUID | Primary key, not null | Unique enrollment identifier |
| `user_id` | UUID | Foreign key to `users.id`, not null | Enrolled student's identifier |
| `course_id` | UUID | Foreign key to `courses.id`, not null | Enrolled course identifier |
| `enrolled_at` | TIMESTAMPTZ | Not null, default current timestamp | Enrollment creation time |

**Design decisions:**

- A student cannot enroll in the same course more than once.
- The combination of `user_id` and `course_id` must be unique.
- Only the authenticated student can view or remove their own enrollments.
- The backend derives `user_id` from the authenticated identity rather than trusting a client-supplied owner ID.
- Removing an enrollment deletes the corresponding enrollment record.
- Re-enrollment after unenrolling is permitted.

## 5. Primary Keys and Foreign Keys

### Primary keys

Each table has a UUID primary key:

- `users.id`
- `courses.id`
- `enrollments.id`

UUIDs provide unique identifiers without requiring sequential integer IDs.

### Foreign keys

| Foreign key | References | Purpose |
| --- | --- | --- |
| `enrollments.user_id` | `users.id` | Ensures the enrolled user exists. |
| `enrollments.course_id` | `courses.id` | Ensures the enrolled course exists. |

Foreign keys use `ON DELETE RESTRICT` so a user or course cannot be deleted while related enrollments exist.

This preserves referential integrity and supports the requirement that courses with enrollments cannot be deleted.

## 6. Constraints

The following constraints must be enforced at the database level wherever applicable.

| Constraint | Table | Purpose |
| --- | --- | --- |
| Primary key | All tables | Uniquely identifies each record. |
| Unique email | `users` | Prevents duplicate email addresses. |
| Role check | `users` | Restricts roles to `student` and `admin`. |
| Positive duration check | `courses` | Requires `duration_hours > 0`. |
| User foreign key | `enrollments` | Requires an existing user. |
| Course foreign key | `enrollments` | Requires an existing course. |
| Unique user-course pair | `enrollments` | Prevents duplicate enrollments. |
| Not-null constraints | Required columns | Prevents missing mandatory values. |

Application-level validation is also required. Database constraints are the final integrity safeguard, not a replacement for request validation.

## 7. Indexes

Indexes are selected according to expected MVP query patterns.

| Index | Table | Columns | Reason |
| --- | --- | --- | --- |
| Unique email index | `users` | `email` | Enforces uniqueness and supports login lookups. |
| Primary key indexes | All tables | `id` | Supports primary key lookups. |
| Unique enrollment index | `enrollments` | `(user_id, course_id)` | Prevents duplicate enrollments and supports checking a student's enrollment. |
| Course enrollment index | `enrollments` | `course_id` | Supports course enrollment lookups and related integrity checks. |

PostgreSQL automatically creates indexes for primary key and unique constraints. These indexes should not be duplicated.

No additional indexes are planned until actual query patterns justify them.

## 8. Delete and Update Behavior

| Operation | Behavior |
| --- | --- |
| Delete a course without enrollments | Allowed for an administrator. |
| Delete a course with enrollments | Rejected. |
| Delete a user with enrollments | Rejected while related enrollments exist. |
| Delete an enrollment | Allowed for the owner under the enrollment rules. |
| Update course details | Allowed for an administrator. |
| Update a user's role | Restricted to a controlled administrative process. |
| Update primary keys | Not supported through application workflows. |

Foreign key restrictions prevent deleting parent records that still have dependent enrollments.

## 9. Data Types and Defaults

### UUID generation

UUIDs should be generated using PostgreSQL's `gen_random_uuid()` default or the project's established SQLAlchemy UUID generation pattern.

The implementation must choose one consistent strategy rather than generating identifiers independently in multiple layers.

### Timestamps

Use `TIMESTAMPTZ` for timestamps so stored times represent unambiguous instants.

- `created_at` defaults to the current timestamp.
- `updated_at` defaults to the current timestamp and changes on record updates.
- `enrolled_at` defaults to the current timestamp.

### String and numeric validation

- `email` must contain a valid email address, validated by the API.
- `full_name`, `title`, and `instructor_name` must not be blank.
- `duration_hours` must be greater than zero.
- `description` must not be blank.

Request-level validation and database constraints should be used together.

## 10. Normalization

The schema follows basic relational normalization principles.

### First Normal Form (1NF)

Each column stores a single value. Repeating course IDs or multiple enrolled courses are not stored in a single user column.

### Second Normal Form (2NF)

Enrollment data is stored in its own table. Each enrollment has a unique identifier and references one user and one course.

### Third Normal Form (3NF)

User information, course information, and enrollment information are stored separately. Course details are not duplicated in every enrollment record.

This structure reduces redundant data and update anomalies.

## 11. Transaction Requirements

The following operations must be handled safely:

### Student enrollment

1. Authenticate the student.
2. Verify that the course exists.
3. Check enrollment eligibility.
4. Insert the enrollment.
5. Commit the transaction.

The unique constraint on `(user_id, course_id)` remains necessary even when the application checks for existing enrollments. It prevents duplicate records under concurrent requests.

### Student unenrollment

1. Authenticate the student.
2. Identify the enrollment belonging to that student and course.
3. Delete the matching enrollment.
4. Commit the transaction.

A student must not be able to delete another student's enrollment.

### Course deletion

1. Verify administrator authorization.
2. Check whether enrollments exist.
3. Delete the course only when no enrollments reference it.
4. Commit the transaction.

The foreign key restriction protects data integrity if concurrent operations affect enrollment records.

## 12. Schema Summary

| Table | Primary key | Relationships |
| --- | --- | --- |
| `users` | `id` | One-to-many with `enrollments` |
| `courses` | `id` | One-to-many with `enrollments` |
| `enrollments` | `id` | Many-to-one with `users` and `courses` |

Total tables: **3**

## 13. Out of Scope

The following are not included in this MVP database design:

- Instructor accounts and instructor-specific permissions.
- Course prerequisites and course schedules.
- Course capacity and enrollment limits.
- Grades, assignments, quizzes, and attendance.
- Payment records.
- Course reviews and ratings.
- Enrollment history after an enrollment is deleted.
- Soft deletion and audit logs.

These features can be introduced later if requirements change.

## 14. Implementation Checklist

Before proceeding to ORM model implementation, verify:

- [ ] All entities correspond to the agreed requirements.
- [ ] Primary keys and foreign keys are defined.
- [ ] Column types and nullability are specified.
- [ ] Unique and check constraints are documented.
- [ ] Indexes are justified by expected queries.
- [ ] Delete behavior protects enrollment integrity.
- [ ] Timestamp and UUID generation strategies are consistent.
- [ ] Enrollment ownership and duplicate prevention are addressed.
- [ ] Out-of-scope features are excluded.
