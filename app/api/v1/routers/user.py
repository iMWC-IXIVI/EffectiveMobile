from fastapi import APIRouter, status, Depends, exceptions

from sqlalchemy.ext.asyncio import AsyncSession

from db import get_db
from db.shemas import UserRegistration, Success
from db.models import User
from core import hash_password


user_router = APIRouter(prefix='/user', tags=['Пользователь', ])


@user_router.post('/registration', summary='Регистрация пользователя', status_code=status.HTTP_201_CREATED)
async def registration(data: UserRegistration, connection: AsyncSession = Depends(get_db)):
    pwd_1 = data.password
    pwd_2 = data.accept_password

    if pwd_1 != pwd_2:
        raise exceptions.HTTPException(detail={'message': 'Error'}, status_code=status.HTTP_400_BAD_REQUEST)

    pwd_hash = hash_password(password=pwd_1)

    user = User(
        first_name=data.first_name,
        last_name=data.last_name,
        surname=data.surname,
        email=data.email,
        password_hash=pwd_hash
    )

    connection.add(user)

    try:
        await connection.commit()
    except Exception:
        raise exceptions.HTTPException(detail={'message': 'Error'}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    await connection.refresh(user)

    return Success()
