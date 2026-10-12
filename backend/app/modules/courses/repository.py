
from uuid import UUID

from sqlalchemy import select

from app.extensions import db
from app.models.course import Course


def list_courses() -> list[Course]:
    statement = select(Course).order_by(Course.title, Course.id)
    return list(db.session.scalars(statement).all())


def find_course_by_id(course_id: UUID) -> Course | None:
    statement = select(Course).where(Course.id == course_id)
    return db.session.scalar(statement)


def create_course(
    title: str,
    description: str,
    instructor_name: str,
    duration_hours: int,
) -> Course:
    course = Course()
    course.title = title
    course.description = description
    course.instructor_name = instructor_name
    course.duration_hours = duration_hours

    db.session.add(course)
    db.session.flush()

    return course


def update_course(
    course: Course,
    updates: dict,
) -> Course:
    for field, value in updates.items():
        setattr(course, field, value)

    db.session.flush()
    return course


def delete_course(course: Course) -> None:
    db.session.delete(course)
    db.session.flush()
