# Student Course Management System — Requirements

## 1. Problem Statement

The Student Course Management System provides a simple platform for students to discover available courses and manage their enrollments. Administrators can maintain the course catalog.

## 2. Users

### Student

- Register and log in.
- Browse available courses.
- Enroll in a course.
- View enrolled courses.
- Unenroll from a course.

### Admin

- Log in to the system.
- Create, view, update, and delete courses.
- Manage the course catalog.

Admin accounts must be provisioned through a controlled mechanism. Public registration must not allow users to assign themselves the admin role.

## 3. Functional Requirements

### FR-01: Authentication

- Users can register with their name, email, and password.
- Email addresses must be unique.
- Passwords must be securely hashed.
- Users can log in and receive a JWT access token.
- Protected endpoints require valid authentication.

### FR-02: Course Catalog

- Students can view available courses.
- Users can view course details.
- Course details include title, description, instructor name, and course duration.

### FR-03: Course Management

- Admins can create, view, update, and delete courses.
- Only admins can modify the course catalog.
- Course deletion must be rejected when enrollments exist for that course.

### FR-04: Enrollment

- Authenticated students can enroll in available courses.
- A student cannot enroll in the same course more than once.
- Students can view their own enrollments.
- Students can unenroll from their own courses.
- Students cannot access or modify another student's enrollments.

### FR-05: Dashboard

- Students can view their enrolled courses.
- The dashboard displays the total number of enrolled courses.

## 4. Non-Functional Requirements

- **Security:** Hash passwords, protect JWT signing secrets, and enforce backend authorization.
- **Data integrity:** Use primary keys, foreign keys, unique constraints, and appropriate non-null constraints.
- **Validation:** Validate incoming data and return consistent error responses.
- **Maintainability:** Follow the existing Expense Tracker architecture and naming conventions.
- **Configuration:** Use environment variables and maintain a safe `.env.example`.
- **Usability:** Provide clear loading, success, error, and empty states in the frontend.

## 5. MVP Scope

The MVP includes:

- Student registration and login.
- Admin authentication and course management.
- Course listing and details.
- Student enrollment and unenrollment.
- Student dashboard with enrollment count.
- PostgreSQL persistence.
- Vue frontend integrated with Flask REST APIs.
- Essential backend and end-to-end tests.

## 6. Out of Scope

- Instructor-specific accounts and permissions.
- Assignments, examinations, quizzes, and grading.
- Attendance tracking.
- Payments and subscriptions.
- Email verification and password reset.
- Notifications and messaging.
- Course content uploads and video streaming.
- Advanced search, filtering, pagination, and analytics.
- Docker, CI/CD, and production deployment.

## 7. Acceptance Criteria

1. A student can register and log in successfully.
2. Invalid credentials and duplicate email registrations are rejected.
3. Students can browse courses and view course details.
4. Admins can create, update, and delete eligible courses.
5. Non-admin users cannot modify courses.
6. A student can enroll in a course only once.
7. A student can view and remove their own enrollments.
8. Students cannot access another student's enrollment data.
9. The dashboard displays the correct enrollment count.
10. Data persists in PostgreSQL.
11. Core frontend-to-backend workflows pass verification.
12. Required configuration and setup instructions are documented.
