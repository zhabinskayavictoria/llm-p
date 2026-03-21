class AppError(Exception):
    def __init__(self, message: str, status_code: int = 400, **kwargs):
        """Инициализирует исключение"""
        self.message = message
        self.status_code = status_code
        self.meta = kwargs
        super().__init__(self.message)

class ConflictError(AppError):
    """Ошибка конфликта (ресурс уже существует)"""
    def __init__(self, message: str = "Resource exists", **kwargs):
        """Инициализирует ошибку конфликта с кодом 409"""
        super().__init__(message, status_code=409, **kwargs)

class UnauthorizedError(AppError):
    """Ошибка авторизации (неверные учетные данные)"""
    def __init__(self, message: str = "Unauthorized", **kwargs):
        """Инициализирует ошибку авторизации с кодом 401"""
        super().__init__(message, status_code=401, **kwargs)

class ForbiddenError(AppError):
    """Ошибка доступа (недостаточно прав)"""
    def __init__(self, message: str = "Forbidden", **kwargs):
        """Инициализирует ошибку доступа с кодом 403"""
        super().__init__(message, status_code=403, **kwargs)

class NotFoundError(AppError):
    """Ошибка: ресурс не найден"""
    def __init__(self, message: str = "Not found", **kwargs):
        """Инициализирует ошибку с кодом 404"""
        super().__init__(message, status_code=404, **kwargs)

class ExternalServiceError(AppError):
    """Ошибка внешнего сервиса (OpenRouter)"""
    def __init__(self, message: str = "External service error", **kwargs):
        """Инициализирует ошибку с кодом 503"""
        super().__init__(message, status_code=503, **kwargs)