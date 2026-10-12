
from uuid import UUID

from sqlalchemy.exc import IntegrityError

from app.extensions import db
from app.errors.exceptions import NotFoundError, ValidationError
from app.models.enrollment import Enrollment
from app.modules.courses import service as course_service
from app.modules.enrollments import repository


def _parse_uuid(value: str | UUID, field_name: str) -> UUID:
    try:
        return UUID(str(value))
    except (ValueError, TypeError, AttributeError):
        raise ValidationError(f"Invalid {field_name}")


def list_my_enrollments(user_id: str | UUID) -> list[Enrollment]:
    parsed_user_id = _parse_uuid(user_id, "user ID")
    return repository.list_enrollments_by_user(parsed_user_id)


def enroll_in_course(
    user_id: str | UUID,
    course_id: str | UUID,
) -> Enrollment:
    parsed_user_id = _parse_uuid(user_id, "user ID")
    parsed_course_id = _parse_uuid(course_id, "course ID")

    course_service.get_course(parsed_course_id)

    existing = repository.find_enrollment_by_user_and_course(
        parsed_user_id,
        parsed_course_id,
    )
    if existing is not None:
        raise ValidationError("Already enrolled in this course")

    try:
        enrollment = repository.create_enrollment(
            parsed_user_id,
            parsed_course_id,
        )
        db.session.commit()
        return enrollment
    except IntegrityError:
        db.session.rollback()
        raise ValidationError("Already enrolled in this course")
    except Exception:
        db.session.rollback()
        raise


def unenroll(
    user_id: str | UUID,
    enrollment_id: str | UUID,
) -> None:
    parsed_user_id = _parse_uuid(user_id, "user ID")
    parsed_enrollment_id = _parse_uuid(enrollment_id, "enrollment ID")

    enrollment = repository.find_enrollment_by_id(parsed_enrollment_id)

    if enrollment is None or enrollment.user_id != parsed_user_id:
        raise NotFoundError("Enrollment not found")

    try:
        repository.delete_enrollment(enrollment)
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise
