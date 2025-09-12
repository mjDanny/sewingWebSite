from pydantic import BaseModel, EmailStr


# Входные данные при создании пользователя
class UserCreate(BaseModel):
    name: str
    email: EmailStr


# То, что мы будем возвращать наружу
class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr

    class Config:
        from_attributes = True  # позволяет конвертировать SQLAlchemy -> Pydantic
