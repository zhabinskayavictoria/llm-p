from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import User

class UserRepository:
    """Репозиторий для работы с пользователями"""
    def __init__(self, session: AsyncSession):
        """Инициализирует репозиторий с сессией БД"""
        self.session = session

    async def get_by_email(self, email: str) -> User | None:
        """Возвращает пользователя по email или None"""
        result = await self.session.execute(
            select(User).where(User.email == email)
        )
        return result.scalar_one_or_none()

    async def get_by_id(self, user_id: int) -> User | None:
        """Возвращает пользователя по ID или None"""
        result = await self.session.execute(
            select(User).where(User.id == user_id)
        )
        return result.scalar_one_or_none()

    async def create(self, email: str, password_hash: str, role: str = "user") -> User:
        """Создает нового пользователя в БД и возвращает его"""
        user = User(email=email, password_hash=password_hash, role=role)
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user