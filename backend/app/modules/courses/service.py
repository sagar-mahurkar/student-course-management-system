
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.extensions import db
from app.errors.exceptions import NotFoundError, ValidationError
from app.models.course import Course
from app.models.enrollment import Enrollment
from app.modules.courses import repository


def _parse_course_id(course_id: str | UUID) -> UUID:
    try:
        return UUID(str(course_id))
    except (ValueError, TypeError, AttributeError):
        raise ValidationError("Invalid course ID")


def list_courses() -> list[Course]:
    return repository.list_courses()


def get_course(course_id: str | UUID) -> Course:
    parsed_id = _parse_course_id(course_id)
    course = repository.find_course_by_id(parsed_id)

    if course is None:
        raise NotFoundError("Course not found")

    return course


def create_course(data: dict) -> Course:
    try:
        course = repository.create_course(
            title=data["title"],
            description=data["description"],
            instructor_name=data["instructor_name"],
            duration_hours=data["duration_hours"],
        )
        db.session.commit()
        return course
    except Exception:
        db.session.rollback()
        raise


def update_course(course_id: str | UUID, updates: dict) -> Course:
    course = get_course(course_id)

    try:
        repository.update_course(course, updates)
        db.session.commit()
        return course
    except Exception:
        db.session.rollback()
        raise


def delete_course(course_id: str | UUID) -> None:
    course = get_course(course_id)

    enrollment_exists = db.session.scalar(
        select(Enrollment.id)
        .where(Enrollment.course_id == course.id)
        .limit(1)
    )

    if enrollment_exists is not None:
        raise ValidationError(
            "Cannot delete a course that has existing enrollments"
        )

    try:
        repository.delete_course(course)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        raise ValidationError(
            "Cannot delete a course that has existing enrollments"
        )
    except Exception:
        db.session.rollback()
        raise
