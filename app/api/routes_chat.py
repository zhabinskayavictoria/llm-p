from fastapi import APIRouter, Depends, HTTPException, status

from app.schemas.chat import ChatRequest, ChatResponse
from app.usecases.chat import ChatUseCase
from app.core.errors import ExternalServiceError
from app.api.deps import get_chat_usecase, get_current_user_id

router = APIRouter(prefix="/chat", tags=["chat"])

@router.post("", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    user_id: int = Depends(get_current_user_id),
    usecase: ChatUseCase = Depends(get_chat_usecase),
):
    """Отправляет сообщение модели и возвращает ответ"""
    try:
        answer = await usecase.ask(
            user_id=user_id,
            prompt=request.prompt,
            system=request.system,
            max_history=request.max_history,
            temperature=request.temperature,
        )
        return ChatResponse(answer=answer)
    except ExternalServiceError as e:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(e))
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Server error")

@router.get("/history", response_model=list)
async def get_history(
    user_id: int = Depends(get_current_user_id),
    usecase: ChatUseCase = Depends(get_chat_usecase),
):
    """Возвращает историю сообщений пользователя"""
    history = await usecase.get_history(user_id)
    return [
        {
            "id": msg.id,
            "role": msg.role,
            "content": msg.content,
            "created_at": msg.created_at
        }
        for msg in history
    ]

@router.delete("/history", status_code=status.HTTP_204_NO_CONTENT)
async def clear_history(
    user_id: int = Depends(get_current_user_id),
    usecase: ChatUseCase = Depends(get_chat_usecase),
):
    """Удаляет всю историю сообщений пользователя"""
    await usecase.clear_history(user_id)
