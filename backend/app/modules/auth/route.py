from flask import Blueprint, request

from flask_jwt_extended import get_jwt_identity, jwt_required
from app.errors.exceptions import UnauthorizedError
from app.modules.auth.repository import find_user_by_id
from app.modules.auth.schema import LoginRequest, RegisterRequest
from app.modules.auth.service import login_user, register_user
from app.schemas.response import success_response
from app.schemas.validation import validate_request

auth_bp = Blueprint(
    "auth",
    __name__,
    url_prefix="/api/v1/auth",
)


@auth_bp.post("/register")
def register():
    request_data = validate_request(
        request,
        RegisterRequest,
    )

    user = register_user(
        full_name=request_data.full_name,
        email=str(request_data.email),
        password=request_data.password,
    )

    return success_response(
        {
            "id": str(user.id),
            "full_name": user.full_name,
            "email": user.email,
            "role": user.role,
            "created_at": user.created_at.isoformat(),
        },
        status_code=201,
    )


@auth_bp.post("/login")
def login():
    request_data = validate_request(
        request,
        LoginRequest,
    )

    user, access_token = login_user(
        email=str(request_data.email),
        password=request_data.password,
    )

    return success_response(
        {
            "access_token": access_token,
            "user": {
                "id": str(user.id),
                "full_name": user.full_name,
                "email": user.email,
                "role": user.role,
            },
        }
    )


@auth_bp.get("/me")
@jwt_required()
def get_current_user():
    user_id = get_jwt_identity()
    user = find_user_by_id(user_id)

    if user is None:
        raise UnauthorizedError("Invalid authentication token")

    return success_response(
        {
            "id": str(user.id),
            "full_name": user.full_name,
            "email": user.email,
            "role": user.role,
        }
    )
