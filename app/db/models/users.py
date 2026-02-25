from enum import Enum

from sqlalchemy import String, Enum as SQLEnum, text, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base, DefaultFieldsMixin


class UserRole(Enum):
    """Роли пользователей"""
    admin = 'admin'
    manager = 'manager'


class User(Base, DefaultFieldsMixin):
    """Таблица пользователей (users)"""
    first_name: Mapped[str] = mapped_column(String(100), nullable=False, comment='Имя')
    last_name: Mapped[str] = mapped_column(String(100), nullable=False, comment='Фамилия')
    surname: Mapped[str] = mapped_column(String(100), nullable=False, comment='Отчество')
    email: Mapped[str] = mapped_column(String(255), index=True, unique=True, nullable=False, comment='Почта')
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False, comment='Пароль')
    role: Mapped[UserRole] = mapped_column(SQLEnum(UserRole), default=UserRole.manager, server_default=text("'manager'"), nullable=False, comment='Роль')
    is_deleted: Mapped[bool] = mapped_column(Boolean(), default=False, server_default=text("'false'"), nullable=False, comment='Удален ли пользователь')
