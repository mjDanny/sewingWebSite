from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import RedirectResponse, HTMLResponse
from sqlalchemy.orm import Session
from passlib.hash import bcrypt

from app.database import get_db
from app import models
from app.schemas import UserCreate

from fastapi.templating import Jinja2Templates

# Роутер
router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


# Регистрация (форма + обработка)


@router.get("/register", response_class=HTMLResponse)
def register_form(request: Request):
    # Отображение страницы с регистрацией
    return templates.TemplateResponse("register.html", {"request": request})


@router.post("/register")
def register_user(
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    """
    Обрабатывает отправку формы регистрации:
    - проверяет, нет ли пользователя с таким email
    - хэширует пароль
    - сохраняет пользователя в БД
    """
    existing_user = db.query(models.User).filter(models.User.email == email).first()
    if existing_user:
        return templates.TemplateResponse(
            "register.html",
            {"request": request, "error": "Пользователь с таким email уже существует"},
        )
    hashed_password = bcrypt.hash(password)
    new_user = models.User(name=name, email=email, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return RedirectResponse("/login", status_code=303)

# Авторизация (форма + обработка)

@router.get("/login", response_class=HTMLResponse)
def login_form(request: Request):
    # Страница с формой входа
    return templates.TemplateResponse("login.html", {"request": request})

@router.post("/login")
def login_user(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    """
    Обрабатывает отправку формы логина:
    - проверяет, есть ли пользователь с email
    - сверяет пароль с хэшем
    - сохраняет user_id в сессии
    """
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user or not bcrypt.verify(password, user.password):
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "error": "Неверный email или пароль"}
        )
    # Сохраняем user_id в сессии
    request.session["user_id"]= user.id

    return RedirectResponse("/products.html", status_code=303)


# Логаут


@router.get("/logout")
def logout(request: Request):
    """
    Завершает сессию пользователя (очищает куки).
    """
    request.session.clear()
    return RedirectResponse("/login", status_code=303)