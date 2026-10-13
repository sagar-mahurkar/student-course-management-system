from sqlalchemy import select
from werkzeug.security import check_password_hash

from app.extensions import db
from app.models.user import User
from app.seeders.admin_seeder import seed_admin


def _admin_config(**overrides):
    config = {
        "ADMIN_SEED_ENABLED": True,
        "ADMIN_SEED_FULL_NAME": "Initial Administrator",
        "ADMIN_SEED_EMAIL": "admin@example.com",
        "ADMIN_SEED_PASSWORD": "AdminPassword123",
    }
    config.update(overrides)
    return config


def test_seed_admin_creates_admin_with_hashed_password(app):
    with app.app_context():
        admin = seed_admin(_admin_config())

        assert admin is not None
        assert admin.full_name == "Initial Administrator"
        assert admin.email == "admin@example.com"
        assert admin.role == "admin"
        assert admin.password_hash != "AdminPassword123"
        assert check_password_hash(admin.password_hash, "AdminPassword123")


def test_seed_admin_is_idempotent_and_does_not_reset_password(app):
    with app.app_context():
        config = _admin_config()
        first_admin = seed_admin(config)
        first_id = first_admin.id
        original_hash = first_admin.password_hash

        second_admin = seed_admin(
            _admin_config(ADMIN_SEED_PASSWORD="A different password 123")
        )

        assert second_admin.id == first_id
        assert second_admin.password_hash == original_hash

        admins = db.session.scalars(
            select(User).where(User.email == "admin@example.com")
        ).all()
        assert len(admins) == 1


def test_seed_admin_is_disabled_by_default(app):
    with app.app_context():
        assert seed_admin({"ADMIN_SEED_ENABLED": False}) is None

        admin = db.session.scalar(
            select(User).where(User.email == "admin@example.com")
        )
        assert admin is None


def test_seed_admin_requires_configuration_when_enabled(app):
    with app.app_context():
        try:
            seed_admin({"ADMIN_SEED_ENABLED": True})
        except RuntimeError as error:
            assert "ADMIN_SEED_FULL_NAME" in str(error)
        else:
            raise AssertionError("Expected missing admin seed configuration to fail")


def test_seed_admin_rejects_email_owned_by_non_admin_user(app):
    with app.app_context():
        student = User()
        student.full_name = "Existing Student"
        student.email = "admin@example.com"
        student.password_hash = "existing-hash"
        student.role = "student"
        db.session.add(student)
        db.session.commit()

        try:
            seed_admin(_admin_config())
        except RuntimeError as error:
            assert "non-admin user" in str(error)
        else:
            raise AssertionError("Expected conflicting seed email to fail")

        assert student.role == "student"
