
def test_register_student_success(client):
    response = client.post(
        "/api/v1/auth/register",
        json={
            "full_name": "Test Student",
            "email": "student@example.com",
            "password": "TestPassword123",
        },
    )

    assert response.status_code == 201

    data = response.json["data"]
    assert data["full_name"] == "Test Student"
    assert data["email"] == "student@example.com"
    assert data["role"] == "student"
    assert "id" in data
    assert "created_at" in data
    assert "password" not in data
    assert "password_hash" not in data


def test_register_duplicate_email(client):
    payload = {
        "full_name": "Test Student",
        "email": "student@example.com",
        "password": "TestPassword123",
    }

    first_response = client.post(
        "/api/v1/auth/register",
        json=payload,
    )
    second_response = client.post(
        "/api/v1/auth/register",
        json=payload,
    )

    assert first_response.status_code == 201
    assert second_response.status_code == 400


def test_register_invalid_email(client):
    response = client.post(
        "/api/v1/auth/register",
        json={
            "full_name": "Test Student",
            "email": "not-an-email",
            "password": "TestPassword123",
        },
    )

    assert response.status_code == 400


def test_register_short_password(client):
    response = client.post(
        "/api/v1/auth/register",
        json={
            "full_name": "Test Student",
            "email": "student@example.com",
            "password": "short",
        },
    )

    assert response.status_code == 400


def test_register_rejects_admin_role(client):
    response = client.post(
        "/api/v1/auth/register",
        json={
            "full_name": "Test Admin",
            "email": "admin@example.com",
            "password": "TestPassword123",
            "role": "admin",
        },
    )

    assert response.status_code == 400


def test_login_success(client):
    client.post(
        "/api/v1/auth/register",
        json={
            "full_name": "Test Student",
            "email": "student@example.com",
            "password": "TestPassword123",
        },
    )

    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "student@example.com",
            "password": "TestPassword123",
        },
    )

    assert response.status_code == 200

    data = response.json["data"]
    assert isinstance(data["access_token"], str)
    assert data["access_token"]
    assert data["user"]["email"] == "student@example.com"
    assert data["user"]["role"] == "student"


def test_login_incorrect_password(client):
    client.post(
        "/api/v1/auth/register",
        json={
            "full_name": "Test Student",
            "email": "student@example.com",
            "password": "TestPassword123",
        },
    )

    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "student@example.com",
            "password": "WrongPassword123",
        },
    )

    assert response.status_code == 401
    assert response.json["error"]["message"] == "Invalid email or password"


def test_login_unknown_email(client):
    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "unknown@example.com",
            "password": "TestPassword123",
        },
    )

    assert response.status_code == 401
    assert response.json["error"]["message"] == "Invalid email or password"


def test_login_rejects_wrong_content_type(client):
    response = client.post(
        "/api/v1/auth/login",
        data='{"email":"student@example.com","password":"TestPassword123"}',
        content_type="text/plain",
    )

    assert response.status_code == 400


def test_password_is_stored_as_hash(client, app):
    from sqlalchemy import select

    from app.extensions import db
    from app.models.user import User

    password = "TestPassword123"

    response = client.post(
        "/api/v1/auth/register",
        json={
            "full_name": "Test Student",
            "email": "student@example.com",
            "password": password,
        },
    )

    assert response.status_code == 201

    with app.app_context():
        user = db.session.scalar(
            select(User).where(User.email == "student@example.com")
        )

        assert user is not None
        assert user.password_hash != password

        from werkzeug.security import check_password_hash

        assert check_password_hash(user.password_hash, password)


def test_registration_normalizes_email(client):
    response = client.post(
        "/api/v1/auth/register",
        json={
            "full_name": "Test Student",
            "email": "Student@Example.com",
            "password": "TestPassword123",
        },
    )

    assert response.status_code == 201
    assert response.json["data"]["email"] == "student@example.com"


def test_login_with_normalized_email(client):
    registration_response = client.post(
        "/api/v1/auth/register",
        json={
            "full_name": "Test Student",
            "email": "student@example.com",
            "password": "TestPassword123",
        },
    )

    assert registration_response.status_code == 201

    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "STUDENT@EXAMPLE.COM",
            "password": "TestPassword123",
        },
    )

    assert response.status_code == 200
    assert response.json["data"]["access_token"]


def test_login_malformed_json(client):
    response = client.post(
        "/api/v1/auth/login",
        data='{"email":',
        content_type="application/json",
    )

    assert response.status_code == 400
    assert response.json["error"]["message"] == "Invalid JSON body"


def test_password_whitespace_is_preserved(client):
    password = "  TestPassword123  "

    registration_response = client.post(
        "/api/v1/auth/register",
        json={
            "full_name": "Test Student",
            "email": "student@example.com",
            "password": password,
        },
    )

    assert registration_response.status_code == 201

    login_response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "student@example.com",
            "password": password,
        },
    )

    assert login_response.status_code == 200
    assert login_response.json["data"]["access_token"]


def test_get_current_user_with_valid_token(client):
    client.post(
        "/api/v1/auth/register",
        json={
            "full_name": "Test Student",
            "email": "student@example.com",
            "password": "TestPassword123",
        },
    )

    login_response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "student@example.com",
            "password": "TestPassword123",
        },
    )

    token = login_response.json["data"]["access_token"]

    response = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200

    data = response.json["data"]
    assert data["email"] == "student@example.com"
    assert data["full_name"] == "Test Student"
    assert data["role"] == "student"
    assert "password" not in data
    assert "password_hash" not in data


def test_get_current_user_without_token(client):
    response = client.get("/api/v1/auth/me")

    assert response.status_code == 401


def test_get_current_user_with_invalid_token(client):
    response = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": "Bearer invalid-token"},
    )

    assert response.status_code == 422
