from sqlalchemy import select

from app.extensions import db
from app.models.user import User
from uuid import UUID

def find_user_by_email(email: str) -> User | None:
    statement = select(User).where(User.email == email)
    return db.session.scalar(statement)


def create_user(
    full_name: str,
    email: str,
    password_hash: str,
) -> User:
    user = User()

    user.full_name = full_name
    user.email = email
    user.password_hash = password_hash

    db.session.add(user)
    db.session.flush()

    return user

def find_user_by_id(user_id: str) -> User | None:
    try:
        parsed_user_id = UUID(user_id)
    except ValueError:
        return None

    statement = select(User).where(User.id == parsed_user_id)
    return db.session.scalar(statement)