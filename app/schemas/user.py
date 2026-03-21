from pydantic import BaseModel, EmailStr

class UserPublic(BaseModel):
    """Публичная схема пользователя (без пароля)"""
    id: int
    email: EmailStr
    role: str

    model_config = {"from_attributes": True}