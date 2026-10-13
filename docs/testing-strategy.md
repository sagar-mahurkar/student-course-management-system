# SCMS Testing Strategy

## 1. Scope

Testing covers backend API behavior, validation and authorization, database integrity, and critical frontend-to-backend user journeys.

## 2. Backend automated tests

Run from the backend directory:

```bash
python -m pytest -v
```

The project test suite covers health, authentication, course management, enrollment behavior, and administrator seeding.

Important cases include:

- Successful registration and login.
- Duplicate email and invalid credential rejection.
- Missing or invalid JWTs.
- Admin-only course mutation endpoints.
- Course request validation, including blank required strings.
- Course-not-found and duplicate-enrollment behavior.
- Enrollment ownership on listing and deletion.
- Refusal to delete courses that have enrollments.
- Dashboard enrollment count.
- Safe initial administrator provisioning.

Phase 12/13 verification was reported as **58 tests passing**. Re-run the suite from `backend/` to verify the current checkout; test results can vary with environment and dependency setup.

## 3. Frontend build verification

Run from `frontend/`:

```bash
npm run build
```

This command runs Vue/TypeScript project checks and creates the Vite production build.

## 4. End-to-end manual scenarios

The student and administrator workflows were manually tested through the frontend.

### Student workflow

- [x] Register a student account.
- [x] Log in and access protected pages.
- [x] Browse the course catalog and open course details.
- [x] Enroll in a course.
- [x] Verify the enrollment appears in the student's enrollment view/dashboard count.
- [x] Unenroll and verify the UI reflects the change.
- [x] Verify duplicate enrollment and invalid operations are handled.
- [x] Verify logout and protected-route behavior.

### Administrator workflow

- [x] Log in with a provisioned administrator account.
- [x] View the course catalog.
- [x] Create a course.
- [x] Update course details.
- [x] Delete a course without enrollments.
- [x] Verify a non-admin cannot perform admin-only course mutations.
- [x] Verify a course with enrollments cannot be deleted.

These checkboxes record the user-reported manual verification. They are not a substitute for an automated browser E2E suite.

## 5. Final regression checklist

- [ ] Re-run the backend test suite from `backend/`.
- [ ] Run `npm run build` from `frontend/`.
- [ ] Review environment examples and ensure no real secrets are committed.
- [ ] Review `git diff --check`.
- [ ] Confirm only intended documentation/configuration changes are staged.
- [ ] Confirm the working tree is clean after merge and synchronization.

## 6. Known testing boundary

No automated browser test framework is listed in the frontend dependencies. Manual E2E verification is recorded; browser-driven E2E automation is outside the current MVP unless separately added.
