from sqlalchemy import Column, Integer, String, Float
from .database import Base

class User(Base):
    __tablename__="users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email= Column(String, unique=True, index=True)


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, nullable=True)
    price = Column(Float)