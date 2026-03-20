from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from jose import JWTError

from app.db.session import AsyncSessionLocal
from app.core.security import decode_access_token
from app.core.errors import UnauthorizedError
from app.repositories.users import UserRepository
from app.repositories.chat_messages import ChatMessageRepository
from app.services.openrouter_client import OpenRouterClient
from app.usecases.auth import AuthUseCase
from app.usecases.chat import ChatUseCase
import httpx

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session

async def get_user_repo(db: AsyncSession = Depends(get_db)) -> UserRepository:
    return UserRepository(db)

async def get_chat_message_repo(db: AsyncSession = Depends(get_db)) -> ChatMessageRepository:
    return ChatMessageRepository(db)

async def get_http_client() -> httpx.AsyncClient:
    async with httpx.AsyncClient() as client:
        yield client

async def get_openrouter_client(http_client: httpx.AsyncClient = Depends(get_http_client)) -> OpenRouterClient:
    return OpenRouterClient(http_client)

async def get_auth_usecase(user_repo: UserRepository = Depends(get_user_repo)) -> AuthUseCase:
    return AuthUseCase(user_repo)

async def get_chat_usecase(
    message_repo: ChatMessageRepository = Depends(get_chat_message_repo),
    llm_client: OpenRouterClient = Depends(get_openrouter_client),
) -> ChatUseCase:
    return ChatUseCase(message_repo, llm_client)

async def get_current_user_id(token: str = Depends(oauth2_scheme)) -> int:
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
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