from uuid import uuid4

from sqlalchemy import UUID
from sqlalchemy.orm import DeclarativeBase, declared_attr, Mapped, mapped_column


class Base(DeclarativeBase):
    @declared_attr.directive
    def __tablename__(cls) -> str:
        """Метод по названию всех таблиц, принадлежащих Base"""
        return f'{cls.__name__.lower()}s'


class DefaultFieldsMixin:
    """Класс по созданию полей во время создания таблиц"""
    id: Mapped[UUID] = mapped_column(UUID, primary_key=True, default=uuid4, comment='Идентификатор')
