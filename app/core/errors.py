class AppError(Exception):
    def __init__(self, message: str, status_code: int = 400, **kwargs):
        self.message = message
        self.status_code = status_code
        self.meta = kwargs
        super().__init__(self.message)

class ConflictError(AppError):
    def __init__(self, message: str = "Resource exists", **kwargs):
        super().__init__(message, status_code=409, **kwargs)

class UnauthorizedError(AppError):
    def __init__(self, message: str = "Unauthorized", **kwargs):
        super().__init__(message, status_code=401, **kwargs)

class ForbiddenError(AppError):
    def __init__(self, message: str = "Forbidden", **kwargs):
        super().__init__(message, status_code=403, **kwargs)

class NotFoundError(AppError):
    def __init__(self, message: str = "Not found", **kwargs):
        super().__init__(message, status_code=404, **kwargs)

class ExternalServiceError(AppError):
    def __init__(self, message: str = "External service error", **kwargs):
        super().__init__(message, status_code=503, **kwargs)