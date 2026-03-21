from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import ChatMessage

class ChatMessageRepository:
    """Репозиторий для работы с сообщениями чата"""
    def __init__(self, session: AsyncSession):
        """Инициализирует репозиторий с сессией БД"""
        self.session = session

    async def add_message(self, user_id: int, role: str, content: str) -> ChatMessage:
        """Добавляет новое сообщение в БД и возвращает его"""
        message = ChatMessage(user_id=user_id, role=role, content=content)
        self.session.add(message)
        await self.session.commit()
        await self.session.refresh(message)
        return message

    async def get_last_n(self, user_id: int, limit: int) -> list[ChatMessage]:
        """Возвращает последние N сообщений пользователя в хронологическом порядке"""
        result = await self.session.execute(
            select(ChatMessage)
            .where(ChatMessage.user_id == user_id)
            .order_by(ChatMessage.id.desc())
            .limit(limit)
        )
        return list(reversed(result.scalars().all()))

    async def delete_all_for_user(self, user_id: int) -> None:
        """Удаляет все сообщения пользователя"""
        await self.session.execute(
            delete(ChatMessage).where(ChatMessage.user_id == user_id)
        )
        await self.session.commit()