from fastapi import FastAPI, Depends, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import engine, SessionLocal
from app.services.user_service import UserService
from app.services.product_service import ProductService
from app.routers import users, products, auth
# Создание таблиц при первом запуске
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Sewing Website",
    description="Сайт швейного производства",
    version="1.0.0"
)

# Подключение роутеров
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(products.router, prefix="/products", tags=["Products"])
app.include_router(auth.router, tags=["Auth"])
# Middleware для работы сессий
app.add_middleware(SessionMiddleware, secret_key="mega-secret-key")

# Статика и шаблоны
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")


# Зависимость для подключения к БД
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Главная страница
@app.get("/")
def index(request: Request, db: Session = Depends(get_db)):
    products = ProductService(db).get_all()
    return templates.TemplateResponse(
        "index.html", {"request": request, "products": products}
    )


# Авторизация
@app.get("/login")
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


# Регистрация
@app.get("/register")
def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


# Профиль
@app.get("/profile")
def profile_page(request: Request, db: Session = Depends(get_db)):
    service = UserService(db)
    user = service.get_all()[0] if service.get_all() else None
    return templates.TemplateResponse(
        "profile.html", {"request": request, "user": user}
    )


# Страница товара
@app.get("/products/{product_id}")
def product_detail(request: Request, product_id: int, db: Session = Depends(get_db)):
    product = ProductService(db).get(product_id)
    if not product:
        return templates.TemplateResponse(
            "product_detail.html", {"request": request, "product": None}
        )
    return templates.TemplateResponse(
        "product_detail.html",
        {"request": request, "product": product, "can_edit": False},
    )


@app.get("/users", response_model=list[schemas.UserResponse])
def read_users(db: Session = Depends(get_db)):
    service = UserService(db)
    return service.get_all()


@app.post("/users", response_model=schemas.UserResponse)
def create_user_endpoint(user: schemas.UserCreate, db: Session = Depends(get_db)):
    service = UserService(db)
    return service.create(user)


@app.put("/users/{user_id}", response_model=schemas.UserResponse)
def update_user_endpoint(
    user_id: int, user: schemas.UserCreate, db: Session = Depends(get_db)
):
    service = UserService(db)
    return service.update(user_id, user)


@app.delete("/user/{user_id}", response_model=schemas.UserResponse)
def delete_user_enddpoint(user_id: int, db: Session = Depends(get_db)):
    service = UserService(db)
    return service.delete(user_id)


@app.get("/products", response_model=list[schemas.ProductResponse])
def read_products(db: Session = Depends(get_db)):
    service = ProductService(db)
    return service.get_all()


@app.post("/products", response_model=schemas.ProductResponse)
def create_product_endpoint(
    product: schemas.ProductCreate, db: Session = Depends(get_db)
):
    service = ProductService(db)
    return service.create(product)


@app.put("/products/{product_id}", response_model=schemas.ProductResponse)
def update_product_endpoint(
    product_id: int, product: schemas.ProductCreate, db: Session = Depends(get_db)
):
    service = ProductService(db)
    return service.update(product_id, product)


@app.delete("/products/{product_id}", response_model=schemas.ProductResponse)
def delete_product_endpoint(product_id: int, db: Session = Depends(get_db)):
    service = ProductService(db)
    return service.delete(product_id)


@app.get("/users/html")
def users_page(request: Request, db: Session = Depends(get_db)):
    service = UserService(db)
    users = service.get_all()
    return templates.TemplateResponse(
        "users.html", {"request": request, "users": users}
    )
