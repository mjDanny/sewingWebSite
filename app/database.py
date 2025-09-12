from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

#загружаем переменные окружения
load_dotenv()

DATABASE_URL =  os.getenv("DATABASE_URL")

#Создаем подключение
engine = create_engine(DATABASE_URL)

# Создаем сессию для работы с БД
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#Базовый класс для моделей
Base = declarative_base()