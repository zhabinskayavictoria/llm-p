from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import AsyncSessionLocal
from app.core.security import decode_access_token
from app.repositories.users import UserRepository
from app.repositories.chat_messages import ChatMessageRepository
from app.services.openrouter_client import OpenRouterClient
from app.usecases.auth import AuthUseCase
from app.usecases.chat import ChatUseCase
import httpx

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login", auto_error=False)

async def get_db() -> AsyncSession:
    """Предоставляет сессию базы данных"""
    async with AsyncSessionLocal() as session:
        yield session

async def get_user_repo(db: AsyncSession = Depends(get_db)) -> UserRepository:
    """Предоставляет репозиторий пользователей"""
    return UserRepository(db)

async def get_chat_message_repo(db: AsyncSession = Depends(get_db)) -> ChatMessageRepository:
    """Предоставляет репозиторий сообщений чата"""
    return ChatMessageRepository(db)

async def get_http_client() -> httpx.AsyncClient:
    """Предоставляет HTTP-клиент"""
    async with httpx.AsyncClient() as client:
        yield client

async def get_openrouter_client(http_client: httpx.AsyncClient = Depends(get_http_client)) -> OpenRouterClient:
    """Предоставляет клиент OpenRouter"""
    return OpenRouterClient(http_client)

async def get_auth_usecase(user_repo: UserRepository = Depends(get_user_repo)) -> AuthUseCase:
    """Предоставляет usecase для аутентификации"""
    return AuthUseCase(user_repo)

async def get_chat_usecase(
    message_repo: ChatMessageRepository = Depends(get_chat_message_repo),
    llm_client: OpenRouterClient = Depends(get_openrouter_client),
) -> ChatUseCase:
    """Предоставляет usecase для чата"""
    return ChatUseCase(message_repo, llm_client)

async def get_current_user_id(token: str = Depends(oauth2_scheme)) -> int:
    """Получает ID текущего пользователя из JWT токена"""
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user_id_str = payload.get("sub")
    if user_id_str is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        return int(user_id_str)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user ID in token",
            headers={"WWW-Authenticate": "Bearer"},
        )