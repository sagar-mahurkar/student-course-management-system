from collections.abc import Mapping
from typing import Any

from sqlalchemy import select
from werkzeug.security import generate_password_hash

from app.extensions import db
from app.models.user import User


def seed_admin(config: Mapping[str, Any]) -> User | None:
    """Create the configured administrator once; never reset an existing account."""
    if not config.get("ADMIN_SEED_ENABLED", False):
        return None

    full_name = str(config.get("ADMIN_SEED_FULL_NAME") or "").strip()
    email = str(config.get("ADMIN_SEED_EMAIL") or "").strip().lower()
    password = config.get("ADMIN_SEED_PASSWORD")

    if not full_name or not email or not isinstance(password, str) or not password:
        raise RuntimeError(
            "ADMIN_SEED_ENABLED requires ADMIN_SEED_FULL_NAME, "
            "ADMIN_SEED_EMAIL, and ADMIN_SEED_PASSWORD"
        )

    if len(password) < 8:
        raise RuntimeError("ADMIN_SEED_PASSWORD must contain at least 8 characters")

    existing_user = db.session.scalar(
        select(User).where(User.email == email)
    )

    if existing_user is not None:
        if existing_user.role != "admin":
            raise RuntimeError(
                "The configured admin seed email belongs to a non-admin user"
            )
        return existing_user

    admin = User()
    admin.full_name = full_name
    admin.email = email
    admin.password_hash = generate_password_hash(password)
    admin.role = "admin"

    db.session.add(admin)

    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise

    return admin
