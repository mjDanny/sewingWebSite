from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas, crud
from app.database import engine, SessionLocal

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
    return crud.get_users(db)


@app.post("/users", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, user)


@app.put("/users/{user_id}", response_model=schemas.UserResponse)
def update_user_endpoint(user_id: int, user: schemas.UserCreate, db: Session = Depends(get_db)):
    updated_user = crud.update_users(db, user_id, user)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user

@app.delete("/users/{user_id}", response_model=schemas.UserResponse)
def delete_user_endpoint(user_id: int, db: Session = Depends(get_db)):
    deleted_user= crud.delete_user(db, user_id)
    if not deleted_user:
        raise HTTPException(status_code=404, detail="User not found")
    return deleted_user