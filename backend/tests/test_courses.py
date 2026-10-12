
from uuid import UUID, uuid4

from flask_jwt_extended import create_access_token

from app.extensions import db
from app.models.course import Course
from app.models.enrollment import Enrollment
from app.models.user import User


def _create_user(app, role="student"):
    with app.app_context():
        user = User()
        user.full_name = "Test User"
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


def test_list_courses_requires_authentication(client):
    response = client.get("/api/v1/courses")

    assert response.status_code == 401


def test_list_courses(client, app):
    token, _ = _create_user(app)
    _create_course(app)

    response = client.get(
        "/api/v1/courses",
        headers=_auth_header(token),
    )

    assert response.status_code == 200
    data = response.get_json()["data"]
    assert len(data) == 1
    assert data[0]["title"] == "Python Fundamentals"


def test_get_course(client, app):
    token, _ = _create_user(app)
    course_id = _create_course(app)

    response = client.get(
        f"/api/v1/courses/{course_id}",
        headers=_auth_header(token),
    )

    assert response.status_code == 200
    assert response.get_json()["data"]["id"] == course_id


def test_get_missing_course_returns_404(client, app):
    token, _ = _create_user(app)

    response = client.get(
        f"/api/v1/courses/{uuid4()}",
        headers=_auth_header(token),
    )

    assert response.status_code == 404


def test_student_cannot_create_course(client, app):
    token, _ = _create_user(app)

    response = client.post(
        "/api/v1/courses",
        headers=_auth_header(token),
        json={
            "title": "Python Fundamentals",
            "description": "Learn Python basics",
            "instructor_name": "Test Instructor",
            "duration_hours": 20,
        },
    )

    assert response.status_code == 403


def test_admin_can_create_course(client, app):
    token, _ = _create_user(app, role="admin")

    response = client.post(
        "/api/v1/courses",
        headers=_auth_header(token),
        json={
            "title": "Python Fundamentals",
            "description": "Learn Python basics",
            "instructor_name": "Test Instructor",
            "duration_hours": 20,
        },
    )

    assert response.status_code == 201
    assert response.get_json()["data"]["title"] == "Python Fundamentals"


def test_admin_can_update_course(client, app):
    token, _ = _create_user(app, role="admin")
    course_id = _create_course(app)

    response = client.patch(
        f"/api/v1/courses/{course_id}",
        headers=_auth_header(token),
        json={"title": "Advanced Python"},
    )

    assert response.status_code == 200
    assert response.get_json()["data"]["title"] == "Advanced Python"


def test_student_cannot_update_course(client, app):
    token, _ = _create_user(app)
    course_id = _create_course(app)

    response = client.patch(
        f"/api/v1/courses/{course_id}",
        headers=_auth_header(token),
        json={"title": "Unauthorized Update"},
    )

    assert response.status_code == 403


def test_admin_can_delete_course_without_enrollments(client, app):
    token, _ = _create_user(app, role="admin")
    course_id = _create_course(app)

    response = client.delete(
        f"/api/v1/courses/{course_id}",
        headers=_auth_header(token),
    )

    assert response.status_code == 204


def test_course_with_enrollments_cannot_be_deleted(client, app):
    token, admin_id = _create_user(app, role="admin")
    _, student_id = _create_user(app)
    course_id = _create_course(app)

    with app.app_context():
        enrollment = Enrollment()
        enrollment.user_id = UUID(student_id)
        enrollment.course_id = UUID(course_id)

        db.session.add(enrollment)
        db.session.commit()

    response = client.delete(
        f"/api/v1/courses/{course_id}",
        headers=_auth_header(token),
    )

    assert response.status_code == 400
