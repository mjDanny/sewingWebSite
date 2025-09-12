from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from app import models
from app.database import engine, SessionLocal

# Создание таблиц при первом запуске
models.Base.metadata.create_all(bind=engine)

app=FastAPI()

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

@app.get("/users")
def get_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users