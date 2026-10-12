from flask import Blueprint, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required

from app.modules.enrollments import service as enrollment_service

dashboard_bp = Blueprint(
    "dashboard",
    __name__,
    url_prefix="/api/v1/dashboard",
)


@dashboard_bp.get("/summary")
@jwt_required()
def get_dashboard_summary():
    user_id = get_jwt_identity()
    enrolled_course_count = enrollment_service.count_my_enrollments(user_id)

    return jsonify(
        {
            "data": {
                "enrolled_course_count": enrolled_course_count,
            }
        }
    )
