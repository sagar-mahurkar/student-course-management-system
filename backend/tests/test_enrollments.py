
from uuid import uuid4

from flask_jwt_extended import create_access_token

from app.extensions import db
from app.models.course import Course
from app.models.user import User


def _create_user(app):
    with app.app_context():
        user = User()
        user.full_name = "Test Student"
        user.email = f"{uuid4().hex}@example.com"
        user.password_hash = "test-password-hash"
        user.role = "student"

        db.session.add(user)
        db.session.commit()

        user_id = str(user.id)
        token = create_access_token(identity=user_id)
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


def test_list_enrollments_requires_authentication(client):
    response = client.get("/api/v1/enrollments")

    assert response.status_code == 401


def test_student_can_enroll_in_course(client, app):
    token, _ = _create_user(app)
    course_id = _create_course(app)

    response = client.post(
        f"/api/v1/enrollments/{course_id}",
        headers=_auth_header(token),
    )

    assert response.status_code == 201
    assert response.get_json()["data"]["course_id"] == course_id


def test_duplicate_enrollment_is_rejected(client, app):
    token, _ = _create_user(app)
    course_id = _create_course(app)

    first_response = client.post(
        f"/api/v1/enrollments/{course_id}",
        headers=_auth_header(token),
    )
    second_response = client.post(
        f"/api/v1/enrollments/{course_id}",
        headers=_auth_header(token),
    )

    assert first_response.status_code == 201
    assert second_response.status_code == 400


def test_enrollment_for_missing_course_returns_404(client, app):
    token, _ = _create_user(app)

    response = client.post(
        f"/api/v1/enrollments/{uuid4()}",
        headers=_auth_header(token),
    )

    assert response.status_code == 404


def test_student_can_list_own_enrollments(client, app):
    token, _ = _create_user(app)
    course_id = _create_course(app)

    client.post(
        f"/api/v1/enrollments/{course_id}",
        headers=_auth_header(token),
    )

    response = client.get(
        "/api/v1/enrollments",
        headers=_auth_header(token),
    )

    assert response.status_code == 200
    enrollments = response.get_json()["data"]
    assert len(enrollments) == 1
    assert enrollments[0]["course_id"] == course_id


def test_student_can_unenroll(client, app):
    token, _ = _create_user(app)
    course_id = _create_course(app)

    enrollment_response = client.post(
        f"/api/v1/enrollments/{course_id}",
        headers=_auth_header(token),
    )
    enrollment_id = enrollment_response.get_json()["data"]["id"]

    response = client.delete(
        f"/api/v1/enrollments/{enrollment_id}",
        headers=_auth_header(token),
    )

    assert response.status_code == 204


def test_student_cannot_delete_another_students_enrollment(client, app):
    owner_token, _ = _create_user(app)
    other_token, _ = _create_user(app)
    course_id = _create_course(app)

    enrollment_response = client.post(
        f"/api/v1/enrollments/{course_id}",
        headers=_auth_header(owner_token),
    )
    enrollment_id = enrollment_response.get_json()["data"]["id"]

    response = client.delete(
        f"/api/v1/enrollments/{enrollment_id}",
        headers=_auth_header(other_token),
    )

    assert response.status_code == 404


def test_unenrolling_allows_reenrollment(client, app):
    token, _ = _create_user(app)
    course_id = _create_course(app)

    first = client.post(
        f"/api/v1/enrollments/{course_id}",
        headers=_auth_header(token),
    )
    enrollment_id = first.get_json()["data"]["id"]

    deleted = client.delete(
        f"/api/v1/enrollments/{enrollment_id}",
        headers=_auth_header(token),
    )
    second = client.post(
        f"/api/v1/enrollments/{course_id}",
        headers=_auth_header(token),
    )

    assert deleted.status_code == 204
    assert second.status_code == 201
