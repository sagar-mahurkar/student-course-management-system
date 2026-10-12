
from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt, jwt_required

from app.errors.exceptions import ForbiddenError
from app.schemas.validation import validate_request
from app.modules.courses import service
from app.modules.courses.schema import (
    CreateCourseRequest,
    UpdateCourseRequest,
)

courses_bp = Blueprint("courses", __name__, url_prefix="/api/v1/courses")


def _require_admin() -> None:
    if get_jwt().get("role") != "admin":
        raise ForbiddenError("Administrator access required")


def _serialize_course(course) -> dict:
    return {
        "id": str(course.id),
        "title": course.title,
        "description": course.description,
        "instructor_name": course.instructor_name,
        "duration_hours": course.duration_hours,
        "created_at": course.created_at.isoformat(),
        "updated_at": course.updated_at.isoformat(),
    }


@courses_bp.get("")
@jwt_required()
def list_courses():
    courses = service.list_courses()
    return jsonify({"data": [_serialize_course(course) for course in courses]})


@courses_bp.get("/<uuid:course_id>")
@jwt_required()
def get_course(course_id):
    course = service.get_course(course_id)
    return jsonify({"data": _serialize_course(course)})


@courses_bp.post("")
@jwt_required()
def create_course():
    _require_admin()
    data = validate_request(request=request, schema=CreateCourseRequest)
    course = service.create_course(data.model_dump())
    return jsonify({"data": _serialize_course(course)}), 201


@courses_bp.patch("/<uuid:course_id>")
@jwt_required()
def update_course(course_id):
    _require_admin()
    data = validate_request(request=request, schema=UpdateCourseRequest)
    updates = data.model_dump(exclude_unset=True)
    course = service.update_course(course_id, updates)
    return jsonify({"data": _serialize_course(course)})


@courses_bp.delete("/<uuid:course_id>")
@jwt_required()
def delete_course(course_id):
    _require_admin()
    service.delete_course(course_id)
    return "", 204
