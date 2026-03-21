from app.repositories.chat_messages import ChatMessageRepository
from app.services.openrouter_client import OpenRouterClient

class ChatUseCase:
    """Бизнес-логика чата с LLM"""
    def __init__(self, message_repo: ChatMessageRepository, llm_client: OpenRouterClient):
        """Инициализирует usecase с репозиторием и клиентом LLM"""
        self.message_repo = message_repo
        self.llm_client = llm_client
        
    async def ask(self, user_id: int, prompt: str, system: str | None = None, max_history: int = 10, temperature: float = 0.7) -> str:
        """Отправляет запрос к LLM, сохраняет диалог, возвращает ответ"""
        messages = []
        if system:
            messages.append({"role": "system", "content": system})

        history = await self.message_repo.get_last_n(user_id, max_history)
        for msg in history:
            messages.append({"role": msg.role, "content": msg.content})

        messages.append({"role": "user", "content": prompt})
        
        await self.message_repo.add_message(user_id=user_id, role="user", content=prompt)
        llm_answer = await self.llm_client.chat_completion(messages, temperature)
        await self.message_repo.add_message(user_id=user_id, role="assistant", content=llm_answer)
        
        return llm_answer

    async def get_history(self, user_id: int, limit: int = 50) -> list:
        """Возвращает историю сообщений пользователя"""
        return await self.message_repo.get_last_n(user_id, limit)

    async def clear_history(self, user_id: int):
        """Удаляет всю историю сообщений пользователя"""
        await self.message_repo.delete_all_for_user(user_id)
        
