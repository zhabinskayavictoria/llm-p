from app.core.errors import ConflictError, UnauthorizedError, NotFoundError
from app.core.security import hash_password, verify_password, create_access_token
from app.repositories.users import UserRepository


class AuthUseCase:
    """Бизнес-логика аутентификации"""
    def __init__(self, user_repo: UserRepository):
        """Инициализирует usecase с репозиторием пользователей"""
        self.user_repo = user_repo

    async def register(self, email: str, password: str) -> dict:
        """Регистрирует нового пользователя, возвращает его данные"""
        existing_user = await self.user_repo.get_by_email(email)
        if existing_user:
            raise ConflictError("User with this email exists")
        password_hash = hash_password(password)
        user = await self.user_repo.create(email, password_hash)
        return {"id": user.id, "email": user.email, "role": user.role}

    async def login(self, email: str, password: str) -> str:
        """Авторизует пользователя, возвращает JWT токен"""
        user = await self.user_repo.get_by_email(email)
        if not user:
            raise UnauthorizedError("Invalid email or password")
        if not verify_password(password, user.password_hash):
            raise UnauthorizedError("Invalid email or password")
        token = create_access_token(sub=str(user.id), role=user.role)
        return token

    async def get_profile(self, user_id: int) -> dict:
        """Возвращает профиль пользователя по ID"""
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise NotFoundError("User not found")
        return {"id": user.id, "email": user.email, "role": user.role}
    