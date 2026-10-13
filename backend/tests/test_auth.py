from sqlalchemy import select
from werkzeug.security import check_password_hash

from app.extensions import db
from app.models.user import User


REGISTER_URL = "/api/v1/auth/register"
LOGIN_URL = "/api/v1/auth/login"
ME_URL = "/api/v1/auth/me"

VALID_REGISTRATION = {
    "full_name": "Test Student",
    "email": "student@example.com",
    "password": "TestPassword123",
}


def register(client, payload=None):
    return client.post(
        REGISTER_URL,
        json=payload if payload is not None else VALID_REGISTRATION.copy(),
    )


def login(client, email="student@example.com", password="TestPassword123"):
    return client.post(
        LOGIN_URL,
        json={"email": email, "password": password},
    )


def test_register_student_success(client):
    response = register(client)

    assert response.status_code == 201
    data = response.json["data"]
    assert data["full_name"] == "Test Student"
    assert data["email"] == "student@example.com"
    assert data["role"] == "student"
    assert data.get("id")
    assert data.get("created_at")
    assert "password" not in data
    assert "password_hash" not in data


def test_register_duplicate_email_is_rejected(client):
    assert register(client).status_code == 201
    response = register(client)

    assert response.status_code == 400


def test_register_email_is_case_normalized(client):
    response = register(
        client,
        {
            **VALID_REGISTRATION,
            "email": "Student@Example.com",
        },
    )

    assert response.status_code == 201
    assert response.json["data"]["email"] == "student@example.com"


def test_register_case_variant_of_existing_email_is_rejected(client):
    assert register(client).status_code == 201
    response = register(
        client,
        {
            **VALID_REGISTRATION,
            "email": "STUDENT@EXAMPLE.COM",
        },
    )

    assert response.status_code == 400


def test_register_invalid_email_is_rejected(client):
    response = register(client, {**VALID_REGISTRATION, "email": "not-an-email"})
    assert response.status_code == 400


def test_register_short_password_is_rejected(client):
    response = register(client, {**VALID_REGISTRATION, "password": "short"})
    assert response.status_code == 400


def test_register_missing_required_field_is_rejected(client):
    payload = VALID_REGISTRATION.copy()
    payload.pop("full_name")

    response = register(client, payload)
    assert response.status_code == 400


def test_public_registration_cannot_assign_admin_role(client, app):
    response = register(
        client,
        {
            **VALID_REGISTRATION,
            "role": "admin",
            "email": "attempted-admin@example.com",
        },
    )

    # This API contract rejects unknown/protected registration fields.
    assert response.status_code == 400

    with app.app_context():
        user = db.session.scalar(
            select(User).where(User.email == "attempted-admin@example.com")
        )
        assert user is None


def test_password_is_stored_as_a_hash(client, app):
    password = VALID_REGISTRATION["password"]
    response = register(client)
    assert response.status_code == 201

    with app.app_context():
        user = db.session.scalar(
            select(User).where(User.email == VALID_REGISTRATION["email"])
        )
        assert user is not None
        assert user.password_hash != password
        assert check_password_hash(user.password_hash, password)


def test_login_success_returns_access_token_and_user(client):
    assert register(client).status_code == 201

    response = login(client)
    assert response.status_code == 200

    data = response.json["data"]
    assert isinstance(data["access_token"], str) and data["access_token"]
    assert data["user"]["email"] == "student@example.com"
    assert data["user"]["role"] == "student"
    assert "password_hash" not in data["user"]


def test_login_wrong_password_is_rejected(client):
    assert register(client).status_code == 201

    response = login(client, password="WrongPassword123")
    assert response.status_code == 401
    assert response.json["error"]["message"] == "Invalid email or password"


def test_login_unknown_email_is_rejected(client):
    response = login(client, email="unknown@example.com")
    assert response.status_code == 401
    assert response.json["error"]["message"] == "Invalid email or password"


def test_login_accepts_case_normalized_email(client):
    assert register(client).status_code == 201

    response = login(client, email="STUDENT@EXAMPLE.COM")
    assert response.status_code == 200
    assert response.json["data"]["access_token"]


def test_login_rejects_wrong_content_type(client):
    response = client.post(
        LOGIN_URL,
        data='{"email":"student@example.com","password":"TestPassword123"}',
        content_type="text/plain",
    )
    assert response.status_code == 400


def test_login_rejects_malformed_json(client):
    response = client.post(
        LOGIN_URL,
        data='{"email":',
        content_type="application/json",
    )
    assert response.status_code == 400
    assert response.json["error"]["message"] == "Invalid JSON body"


def test_password_whitespace_is_preserved(client):
    password = "  TestPassword123  "
    payload = {**VALID_REGISTRATION, "password": password}

    assert register(client, payload).status_code == 201
    response = login(client, password=password)
    assert response.status_code == 200


def test_get_current_user_returns_safe_user_data(client):
    assert register(client).status_code == 201
    token = login(client).json["data"]["access_token"]

    response = client.get(
        ME_URL,
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    data = response.json["data"]
    assert data["email"] == "student@example.com"
    assert data["full_name"] == "Test Student"
    assert data["role"] == "student"
    assert "password" not in data
    assert "password_hash" not in data


def test_get_current_user_requires_authentication(client):
    response = client.get(ME_URL)
    assert response.status_code == 401


def test_get_current_user_rejects_invalid_token(client):
    response = client.get(
        ME_URL,
        headers={"Authorization": "Bearer invalid-token"},
    )
    # Flask-JWT-Extended's default invalid-token status is 422.
    assert response.status_code in (401, 422)
