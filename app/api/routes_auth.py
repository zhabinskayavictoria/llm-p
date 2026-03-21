from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.schemas.auth import RegisterRequest, TokenResponse
from app.schemas.user import UserPublic
from app.usecases.auth import AuthUseCase
from app.core.errors import ConflictError, UnauthorizedError, NotFoundError
from app.api.deps import get_auth_usecase, get_current_user_id

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserPublic)
async def register(
    request: RegisterRequest,
    usecase: AuthUseCase = Depends(get_auth_usecase),
):
    """Регистрирует нового пользователя"""
    try:
        user_dict = await usecase.register(request.email, request.password)
        return UserPublic(**user_dict)
    except ConflictError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))

@router.post("/login", response_model=TokenResponse)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    usecase: AuthUseCase = Depends(get_auth_usecase),
):
    """Авторизует пользователя и возвращает JWT токен"""
    try:
        token = await usecase.login(form_data.username, form_data.password)
        return TokenResponse(access_token=token)
    except UnauthorizedError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )

@router.get("/me", response_model=UserPublic)
async def get_me(
    user_id: int = Depends(get_current_user_id),
    usecase: AuthUseCase = Depends(get_auth_usecase),
):
    """Возвращает профиль текущего пользователя"""
    try:
        user_dict = await usecase.get_profile(user_id)
        return UserPublic(**user_dict)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))