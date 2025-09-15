from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import engine, SessionLocal
from app.services.user_service import UserService
from app.services.product_service import ProductService

# Создание таблиц при первом запуске
models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Зависимость для подключения к БД
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root():
    return {"message": "Hello, Sewing Production!"}


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
