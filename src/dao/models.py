import os
from sqlalchemy import Column, String, Boolean, DateTime, BigInteger, create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime, UTC

from dotenv import load_dotenv

load_dotenv()

Base = declarative_base()


class User(Base):
    __tablename__ = 'rubikjanbot_users'

    telegram_id = Column(BigInteger, primary_key=True)  # ID пользователя в Telegram
    username = Column(String(50), nullable=True)  # @username (может быть None, если скрыт)
    first_name = Column(String(50), nullable=False)  # Имя
    last_name = Column(String(50), nullable=True)  # Фамилия (может быть None)
    phone = Column(String(20), nullable=True)  # Телефон (если пользователь его предоставит)
    is_admin = Column(Boolean, default=False)  # Админ ли?
    is_active = Column(Boolean, default=True)  # Активен ли аккаунт?
    registered_at = Column(DateTime(timezone=True), default=datetime.now(tz=UTC))  # Дата регистрации

    def __repr__(self):
        return f"<User(id={self.telegram_id}, username='{self.username}')>"
    


engine = create_engine(
    os.getenv("RUBIKJANBOT_DATABASE_URL", "sqlite:///rubikjanbot.db"),
    echo=True)

AsyncSessionLocal = None


if RUBIKJANBOT_ASYNC_DATABASE_URL := os.getenv("RUBIKJANBOT_ASYNC_DATABASE_URL"):
    async_engine = create_async_engine(
        os.getenv("RUBIKJANBOT_ASYNC_DATABASE_URL", "sqlite+aiosqlite:///rubikjanbot.db"),
        echo=True
    )
    AsyncSessionLocal = sessionmaker (async_engine, class_=AsyncSession, expire_on_commit=False) 
