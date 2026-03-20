from pydantic import BaseModel, Field

class ChatRequest(BaseModel):
    prompt: str = Field(min_length=1, description="Текст запроса пользователя")
    system: str | None = Field(None, description="Системная инструкция для модели")
    max_history: int = Field(10, ge=1, le=50, description="Количество последних сообщений из истории")
    temperature: float = Field(0.7, ge=0.0, le=2.0, description="Температура модели (креативность)")

class ChatResponse(BaseModel):
    answer: str