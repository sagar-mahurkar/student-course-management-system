
from flask import Blueprint, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required

from app.modules.enrollments import service

enrollments_bp = Blueprint(
    "enrollments",
    __name__,
    url_prefix="/api/v1/enrollments",
)


def _serialize_enrollment(enrollment) -> dict:
    return {
        "id": str(enrollment.id),
        "user_id": str(enrollment.user_id),
        "course_id": str(enrollment.course_id),
        "enrolled_at": enrollment.enrolled_at.isoformat(),
    }


@enrollments_bp.get("")
@jwt_required()
def list_my_enrollments():
    user_id = get_jwt_identity()
    enrollments = service.list_my_enrollments(user_id)

    return jsonify(
        {"data": [_serialize_enrollment(item) for item in enrollments]}
    )


@enrollments_bp.post("/<uuid:course_id>")
@jwt_required()
def enroll_in_course(course_id):
    user_id = get_jwt_identity()
    enrollment = service.enroll_in_course(user_id, course_id)

    return jsonify({"data": _serialize_enrollment(enrollment)}), 201


@enrollments_bp.delete("/<uuid:enrollment_id>")
@jwt_required()
def unenroll(enrollment_id):
    user_id = get_jwt_identity()
    service.unenroll(user_id, enrollment_id)

    return "", 204
