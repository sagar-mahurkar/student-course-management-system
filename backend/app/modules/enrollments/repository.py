
from uuid import UUID

from sqlalchemy import func, select

from app.extensions import db
from app.models.enrollment import Enrollment


def list_enrollments_by_user(user_id: UUID) -> list[Enrollment]:
    statement = (
        select(Enrollment)
        .where(Enrollment.user_id == user_id)
        .order_by(Enrollment.enrolled_at.desc())
    )
    return list(db.session.scalars(statement).all())


def find_enrollment_by_id(enrollment_id: UUID) -> Enrollment | None:
    statement = select(Enrollment).where(Enrollment.id == enrollment_id)
    return db.session.scalar(statement)


def find_enrollment_by_user_and_course(
    user_id: UUID,
    course_id: UUID,
) -> Enrollment | None:
    statement = select(Enrollment).where(
        Enrollment.user_id == user_id,
        Enrollment.course_id == course_id,
    )
    return db.session.scalar(statement)


def create_enrollment(user_id: UUID, course_id: UUID) -> Enrollment:
    enrollment = Enrollment()
    enrollment.user_id = user_id
    enrollment.course_id = course_id

    db.session.add(enrollment)
    db.session.flush()

    return enrollment


def delete_enrollment(enrollment: Enrollment) -> None:
    db.session.delete(enrollment)
    db.session.flush()

def count_enrollments_by_user(user_id: UUID) -> int:
    statement = (
        select(func.count())
        .select_from(Enrollment)
        .where(Enrollment.user_id == user_id)
    )
    return db.session.scalar(statement) or 0
