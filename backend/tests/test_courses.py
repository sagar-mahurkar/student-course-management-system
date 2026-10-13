from uuid import UUID, uuid4

from flask_jwt_extended import create_access_token
from sqlalchemy import func, select

from app.extensions import db
from app.models.course import Course
from app.models.enrollment import Enrollment
from app.models.user import User


COURSES_URL = "/api/v1/courses"
COURSE_PAYLOAD = {
    "title": "Python Fundamentals",
    "description": "Learn Python basics",
    "instructor_name": "Test Instructor",
    "duration_hours": 20,
}


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
        course.title = COURSE_PAYLOAD["title"]
        course.description = COURSE_PAYLOAD["description"]
        course.instructor_name = COURSE_PAYLOAD["instructor_name"]
        course.duration_hours = COURSE_PAYLOAD["duration_hours"]
        db.session.add(course)
        db.session.commit()
        return str(course.id)


def _auth_header(token):
    return {"Authorization": f"Bearer {token}"}


def _course_count(app):
    with app.app_context():
        return db.session.scalar(select(func.count()).select_from(Course))


def test_list_courses_requires_authentication(client):
    assert client.get(COURSES_URL).status_code == 401


def test_student_can_list_courses(client, app):
    token, _ = _create_user(app)
    _create_course(app)

    response = client.get(COURSES_URL, headers=_auth_header(token))

    assert response.status_code == 200
    data = response.json["data"]
    assert len(data) == 1
    assert data[0]["title"] == COURSE_PAYLOAD["title"]


def test_authenticated_admin_can_list_courses(client, app):
    token, _ = _create_user(app, role="admin")
    _create_course(app)

    response = client.get(COURSES_URL, headers=_auth_header(token))
    assert response.status_code == 200
    assert len(response.json["data"]) == 1


def test_get_course(client, app):
    token, _ = _create_user(app)
    course_id = _create_course(app)

    response = client.get(
        f"{COURSES_URL}/{course_id}",
        headers=_auth_header(token),
    )

    assert response.status_code == 200
    assert response.json["data"]["id"] == course_id


def test_get_missing_course_returns_404(client, app):
    token, _ = _create_user(app)
    response = client.get(
        f"{COURSES_URL}/{uuid4()}",
        headers=_auth_header(token),
    )
    assert response.status_code == 404


def test_admin_can_create_course_and_persist_it(client, app):
    token, _ = _create_user(app, role="admin")

    response = client.post(
        COURSES_URL,
        headers=_auth_header(token),
        json=COURSE_PAYLOAD,
    )

    assert response.status_code == 201
    assert response.json["data"]["title"] == COURSE_PAYLOAD["title"]
    assert _course_count(app) == 1


def test_student_cannot_create_course_and_no_record_is_created(client, app):
    token, _ = _create_user(app)
    before = _course_count(app)

    response = client.post(
        COURSES_URL,
        headers=_auth_header(token),
        json=COURSE_PAYLOAD,
    )

    assert response.status_code == 403
    assert _course_count(app) == before


def test_unauthenticated_user_cannot_create_course(client, app):
    before = _course_count(app)
    response = client.post(COURSES_URL, json=COURSE_PAYLOAD)

    assert response.status_code == 401
    assert _course_count(app) == before


def test_admin_create_rejects_missing_required_field(client, app):
    token, _ = _create_user(app, role="admin")
    payload = COURSE_PAYLOAD.copy()
    payload.pop("title")

    response = client.post(
        COURSES_URL,
        headers=_auth_header(token),
        json=payload,
    )
    assert response.status_code in (400, 422)



def test_admin_create_rejects_blank_required_strings(client, app):
    token, _ = _create_user(app, role="admin")

    for field in ("title", "instructor_name"):
        payload = {**COURSE_PAYLOAD, field: "   "}

        response = client.post(
            COURSES_URL,
            headers=_auth_header(token),
            json=payload,
        )

        assert response.status_code in (400, 422), (
            f"Expected blank '{field}' to be rejected, "
            f"but received {response.status_code}: {response.get_json()}"
        )

    # Verify that neither invalid course was persisted.
    with app.app_context():
        courses = db.session.scalars(
            select(Course).where(
                Course.title == "Python Fundamentals",
                Course.instructor_name == "Test Instructor",
            )
        ).all()

        assert len(courses) == 0


def test_admin_create_rejects_non_positive_duration(client, app):
    token, _ = _create_user(app, role="admin")

    for duration in (0, -1):
        response = client.post(
            COURSES_URL,
            headers=_auth_header(token),
            json={**COURSE_PAYLOAD, "duration_hours": duration},
        )
        assert response.status_code in (400, 422)


def test_admin_create_rejects_non_integer_duration(client, app):
    token, _ = _create_user(app, role="admin")
    response = client.post(
        COURSES_URL,
        headers=_auth_header(token),
        json={**COURSE_PAYLOAD, "duration_hours": 1.5},
    )
    assert response.status_code in (400, 422)


def test_admin_can_update_course(client, app):
    token, _ = _create_user(app, role="admin")
    course_id = _create_course(app)

    response = client.patch(
        f"{COURSES_URL}/{course_id}",
        headers=_auth_header(token),
        json={"title": "Advanced Python"},
    )

    assert response.status_code == 200
    assert response.json["data"]["title"] == "Advanced Python"


def test_student_cannot_update_course_and_record_is_unchanged(client, app):
    token, _ = _create_user(app)
    course_id = _create_course(app)

    response = client.patch(
        f"{COURSES_URL}/{course_id}",
        headers=_auth_header(token),
        json={"title": "Unauthorized Update"},
    )

    assert response.status_code == 403
    with app.app_context():
        course = db.session.get(Course, UUID(course_id))
        assert course is not None
        assert course.title == COURSE_PAYLOAD["title"]


def test_unauthenticated_user_cannot_update_course(client, app):
    course_id = _create_course(app)
    response = client.patch(
        f"{COURSES_URL}/{course_id}",
        json={"title": "Unauthorized Update"},
    )
    assert response.status_code == 401


def test_admin_update_missing_course_returns_404(client, app):
    token, _ = _create_user(app, role="admin")
    response = client.patch(
        f"{COURSES_URL}/{uuid4()}",
        headers=_auth_header(token),
        json={"title": "Advanced Python"},
    )
    assert response.status_code == 404


def test_admin_can_delete_course_without_enrollments(client, app):
    token, _ = _create_user(app, role="admin")
    course_id = _create_course(app)

    response = client.delete(
        f"{COURSES_URL}/{course_id}",
        headers=_auth_header(token),
    )

    assert response.status_code == 204
    assert _course_count(app) == 0


def test_student_cannot_delete_course_and_record_remains(client, app):
    token, _ = _create_user(app)
    course_id = _create_course(app)

    response = client.delete(
        f"{COURSES_URL}/{course_id}",
        headers=_auth_header(token),
    )

    assert response.status_code == 403
    assert _course_count(app) == 1


def test_unauthenticated_user_cannot_delete_course(client, app):
    course_id = _create_course(app)
    response = client.delete(f"{COURSES_URL}/{course_id}")

    assert response.status_code == 401
    assert _course_count(app) == 1


def test_admin_delete_missing_course_returns_404(client, app):
    token, _ = _create_user(app, role="admin")
    response = client.delete(
        f"{COURSES_URL}/{uuid4()}",
        headers=_auth_header(token),
    )
    assert response.status_code == 404


def test_course_with_enrollments_cannot_be_deleted(client, app):
    token, _ = _create_user(app, role="admin")
    _, student_id = _create_user(app)
    course_id = _create_course(app)

    with app.app_context():
        enrollment = Enrollment()
        enrollment.user_id = UUID(student_id)
        enrollment.course_id = UUID(course_id)
        db.session.add(enrollment)
        db.session.commit()

    response = client.delete(
        f"{COURSES_URL}/{course_id}",
        headers=_auth_header(token),
    )

    assert response.status_code == 400
    assert _course_count(app) == 1
