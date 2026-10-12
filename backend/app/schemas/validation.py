from typing import TypeVar

from flask import Request
from pydantic import BaseModel, ValidationError as PydanticValidationError

from app.errors.exceptions import ValidationError as AppValidationError

SchemaT = TypeVar("SchemaT", bound=BaseModel)


def validate_request(
    request: Request,
    schema: type[SchemaT],
) -> SchemaT:
    if not request.is_json:
        raise AppValidationError(
            "Content-Type must be application/json"
        )

    try:
        data = request.get_json()
    except Exception as error:
        raise AppValidationError("Invalid JSON body") from error

    if data is None:
        raise AppValidationError("Request body is required")

    try:
        return schema.model_validate(data)
    except PydanticValidationError as error:
        raise AppValidationError(
            "Request validation failed"
        ) from error
