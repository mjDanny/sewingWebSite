from sqlalchemy.orm import Session
from fastapi import HTTPException
from app import models, schemas
from .base_service import BaseService


class UserService(BaseService):

    def create(self, user: schemas.UserCreate):
        db_user = models.User(name=user.name, email=user.email)
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user
    
    def get_all(self):
        return self.db.query(models.User).all()


    def get_by_id(self, user_id:int):
        return self.db.query(models.User).filter(models.User.id == user_id).first()


    def update(self, user_id:int, user: schemas.UserCreate):
        db_user = self.get_by_id(user_id)
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")
        db_user.name = user.name
        db_user.email = user.email
        self.db.commit()
        self.db.refresh(db_user)
        return db_user
    
    def delete(self, user_id:int):
        db_user = self.get_by_id(user_id)
        if not db_user:
            raise HTTPException(status_code=404, detail = "User not found")
        self.db.delete(db_user)
        self.db.commit()
        return db_user
