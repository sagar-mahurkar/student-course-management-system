from typing import Any

from flask import jsonify


def success_response(
    data: Any,
    status_code: int = 200,
):
    return jsonify({"data": data}), status_code
