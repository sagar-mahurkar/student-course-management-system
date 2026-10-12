class AppError(Exception):
    """Base class for application-level errors."""

    def __init__(
        self,
        message: str,
        status_code: int = 500,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.status_code = status_code


class ValidationError(AppError):
    """Raised when request data is invalid."""

    def __init__(self, message: str) -> None:
        super().__init__(message, status_code=400)


class UnauthorizedError(AppError):
    """Raised when authentication fails."""

    def __init__(self, message: str = "Authentication failed") -> None:
        super().__init__(message, status_code=401)


class ForbiddenError(AppError):
    """Raised when the user lacks permission."""

    def __init__(self, message: str = "Permission denied") -> None:
        super().__init__(message, status_code=403)


class NotFoundError(AppError):
    """Raised when a requested resource does not exist."""

    def __init__(self, message: str = "Resource not found") -> None:
        super().__init__(message, status_code=404)
