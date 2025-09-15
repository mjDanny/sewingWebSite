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


# Для товаров
class ProductCreate(BaseModel):
    name: str
    description: str | None = None
    price: float


class ProductResponse(BaseModel):
    id: int
    name: str
    description: str | None = None
    price: float

    class Config:
        from_attributes = True
