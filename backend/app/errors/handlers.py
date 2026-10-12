from flask import Flask, jsonify

from app.errors.exceptions import AppError


def register_error_handlers(app: Flask) -> None:
    @app.errorhandler(AppError)
    def handle_app_error(error: AppError):
        return (
            jsonify({
                "error": {
                    "message": error.message,
                }
            }),
            error.status_code,
        )

    @app.errorhandler(404)
    def handle_not_found(error):
        return (
            jsonify({
                "error": {
                    "message": "Resource not found",
                }
            }),
            404,
        )

    @app.errorhandler(405)
    def handle_method_not_allowed(error):
        return (
            jsonify({
                "error": {
                    "message": "Method not allowed",
                }
            }),
            405,
        )

    @app.errorhandler(500)
    def handle_internal_server_error(error):
        return (
            jsonify({
                "error": {
                    "message": "Internal server error",
                }
            }),
            500,
        )
