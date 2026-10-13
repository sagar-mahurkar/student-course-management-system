from uuid import UUID, uuid4

from flask_jwt_extended import create_access_token
from sqlalchemy import func, select

from app.extensions import db
from app.models.course import Course
from app.models.enrollment import Enrollment
from app.models.user import User


ENROLLMENTS_URL = "/api/v1/enrollments"


def _create_user(app, role="student"):
    with app.app_context():
        user = User()
        user.full_name = "Test Student"
        user.email = f"{uuid4().hex}@example.com"
        user.password_hash = "test-password-hash"
        user.role = role
        db.session.add(user)
        db.session.commit()

        user_id = str(user.id)
        token = create_access_token(
            identity=user_id,
            additional_claims={"role": role},
        )
        return token, user_id


def _create_course(app):
    with app.app_context():
        course = Course()
        course.title = "Python Fundamentals"
        course.description = "Learn Python basics"
        course.instructor_name = "Test Instructor"
        course.duration_hours = 20
        db.session.add(course)
        db.session.commit()
        return str(course.id)


def _auth_header(token):
    return {"Authorization": f"Bearer {token}"}


def _enrollment_count(app, user_id=None, course_id=None):
    with app.app_context():
        statement = select(func.count()).select_from(Enrollment)
        if user_id is not None:
            statement = statement.where(Enrollment.user_id == UUID(user_id))
        if course_id is not None:
            statement = statement.where(Enrollment.course_id == UUID(course_id))
        return db.session.scalar(statement)


def test_list_enrollments_requires_authentication(client):
    assert client.get(ENROLLMENTS_URL).status_code == 401


def test_student_can_enroll_and_enrollment_persists(client, app):
    token, user_id = _create_user(app)
    course_id = _create_course(app)

    response = client.post(
        f"{ENROLLMENTS_URL}/{course_id}",
        headers=_auth_header(token),
    )

    assert response.status_code == 201
    assert response.json["data"]["course_id"] == course_id
    assert _enrollment_count(app, user_id, course_id) == 1


def test_enrollment_requires_authentication(client, app):
    course_id = _create_course(app)
    response = client.post(f"{ENROLLMENTS_URL}/{course_id}")

    assert response.status_code == 401
    assert _enrollment_count(app, course_id=course_id) == 0


def test_duplicate_enrollment_is_rejected_without_duplicate_record(client, app):
    token, user_id = _create_user(app)
    course_id = _create_course(app)

    first = client.post(
        f"{ENROLLMENTS_URL}/{course_id}",
        headers=_auth_header(token),
    )
    second = client.post(
        f"{ENROLLMENTS_URL}/{course_id}",
        headers=_auth_header(token),
    )

    assert first.status_code == 201
    assert second.status_code == 400
    assert _enrollment_count(app, user_id, course_id) == 1


def test_enrollment_for_missing_course_returns_404(client, app):
    token, user_id = _create_user(app)
    response = client.post(
        f"{ENROLLMENTS_URL}/{uuid4()}",
        headers=_auth_header(token),
    )

    assert response.status_code == 404
    assert _enrollment_count(app, user_id) == 0


def test_student_with_no_enrollments_gets_empty_list(client, app):
    token, _ = _create_user(app)

    response = client.get(
        ENROLLMENTS_URL,
        headers=_auth_header(token),
    )

    assert response.status_code == 200
    assert response.json["data"] == []


def test_student_can_list_only_own_enrollments(client, app):
    first_token, first_user_id = _create_user(app)
    second_token, second_user_id = _create_user(app)
    first_course_id = _create_course(app)
    second_course_id = _create_course(app)

    first_enrollment = client.post(
        f"{ENROLLMENTS_URL}/{first_course_id}",
        headers=_auth_header(first_token),
    )
    second_enrollment = client.post(
        f"{ENROLLMENTS_URL}/{second_course_id}",
        headers=_auth_header(second_token),
    )
    assert first_enrollment.status_code == 201
    assert second_enrollment.status_code == 201

    response = client.get(
        ENROLLMENTS_URL,
        headers=_auth_header(first_token),
    )

    assert response.status_code == 200
    rows = response.json["data"]
    assert len(rows) == 1
    assert rows[0]["course_id"] == first_course_id
    assert all(row.get("user_id") != second_user_id for row in rows)
    assert _enrollment_count(app, first_user_id) == 1


def test_student_can_unenroll_from_own_enrollment(client, app):
    token, user_id = _create_user(app)
    course_id = _create_course(app)

    created = client.post(
        f"{ENROLLMENTS_URL}/{course_id}",
        headers=_auth_header(token),
    )
    assert created.status_code == 201
    enrollment_id = created.json["data"]["id"]

    response = client.delete(
        f"{ENROLLMENTS_URL}/{enrollment_id}",
        headers=_auth_header(token),
    )

    assert response.status_code == 204
    assert _enrollment_count(app, user_id, course_id) == 0


def test_student_cannot_delete_another_students_enrollment(client, app):
    owner_token, owner_id = _create_user(app)
    other_token, _ = _create_user(app)
    course_id = _create_course(app)

    created = client.post(
        f"{ENROLLMENTS_URL}/{course_id}",
        headers=_auth_header(owner_token),
    )
    assert created.status_code == 201
    enrollment_id = created.json["data"]["id"]

    response = client.delete(
        f"{ENROLLMENTS_URL}/{enrollment_id}",
        headers=_auth_header(other_token),
    )

    # 404 avoids disclosing whether another user's enrollment exists.
    assert response.status_code == 404
    assert _enrollment_count(app, owner_id, course_id) == 1


def test_unenrolling_allows_reenrollment(client, app):
    token, user_id = _create_user(app)
    course_id = _create_course(app)

    first = client.post(
        f"{ENROLLMENTS_URL}/{course_id}",
        headers=_auth_header(token),
    )
    assert first.status_code == 201

    deleted = client.delete(
        f"{ENROLLMENTS_URL}/{first.json['data']['id']}",
        headers=_auth_header(token),
    )
    second = client.post(
        f"{ENROLLMENTS_URL}/{course_id}",
        headers=_auth_header(token),
    )

    assert deleted.status_code == 204
    assert second.status_code == 201
    assert _enrollment_count(app, user_id, course_id) == 1


def test_student_cannot_unenroll_nonexistent_enrollment(client, app):
    token, _ = _create_user(app)

    response = client.delete(
        f"{ENROLLMENTS_URL}/{uuid4()}",
        headers=_auth_header(token),
    )
    assert response.status_code == 404


def test_unenrollment_requires_authentication(client, app):
    token, _ = _create_user(app)
    course_id = _create_course(app)
    created = client.post(
        f"{ENROLLMENTS_URL}/{course_id}",
        headers=_auth_header(token),
    )
    enrollment_id = created.json["data"]["id"]

    response = client.delete(f"{ENROLLMENTS_URL}/{enrollment_id}")
    assert response.status_code == 401
    assert _enrollment_count(app, course_id=course_id) == 1
